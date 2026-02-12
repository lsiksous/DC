"""
Showcase Manager - Handle multiple showcase variants
"""

import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

SHOWCASES_DIR = Path("showcases")
BASELINE_NAME = "baseline"

def ensure_showcases_dir():
    """Ensure showcases directory exists"""
    SHOWCASES_DIR.mkdir(exist_ok=True)

def list_showcases() -> List[str]:
    """List all available showcase names (without .yaml extension)"""
    ensure_showcases_dir()
    showcases = []
    for file in SHOWCASES_DIR.glob("*.yaml"):
        showcases.append(file.stem)
    return sorted(showcases, key=lambda x: (x != BASELINE_NAME, x))  # baseline first

def get_showcase_path(name: str) -> Path:
    """Get full path to showcase file"""
    return SHOWCASES_DIR / f"{name}.yaml"

def showcase_exists(name: str) -> bool:
    """Check if showcase exists"""
    return get_showcase_path(name).exists()

def load_showcase(name: str) -> Optional[Dict]:
    """Load a showcase by name"""
    path = get_showcase_path(name)
    if not path.exists():
        return None
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading showcase {name}: {e}")
        return None

def save_showcase(name: str, data: Dict) -> bool:
    """Save showcase data"""
    ensure_showcases_dir()
    path = get_showcase_path(name)
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, 
                     default_flow_style=False, width=float('inf'))
        return True
    except Exception as e:
        print(f"Error saving showcase {name}: {e}")
        return False

def create_variant(source_name: str, variant_name: str, description: str = "") -> bool:
    """Create a new showcase variant from an existing one"""
    # Validate names
    if not source_name or not variant_name:
        return False
    
    # Check source exists
    source_path = get_showcase_path(source_name)
    if not source_path.exists():
        return False
    
    # Check variant doesn't already exist
    variant_path = get_showcase_path(variant_name)
    if variant_path.exists():
        return False
    
    try:
        # Copy the showcase
        shutil.copy2(source_path, variant_path)
        
        # Add metadata about variant creation
        data = load_showcase(variant_name)
        if data:
            if '_variant_info' not in data:
                data['_variant_info'] = {}
            data['_variant_info']['created_from'] = source_name
            data['_variant_info']['created_at'] = datetime.now().isoformat()
            data['_variant_info']['description'] = description
            save_showcase(variant_name, data)
        
        return True
    except Exception as e:
        print(f"Error creating variant: {e}")
        return False

def delete_showcase(name: str) -> bool:
    """Delete a showcase (cannot delete baseline)"""
    if name == BASELINE_NAME:
        return False  # Protect baseline
    
    path = get_showcase_path(name)
    if not path.exists():
        return False
    
    try:
        path.unlink()
        return True
    except Exception as e:
        print(f"Error deleting showcase {name}: {e}")
        return False

def get_showcase_info(name: str) -> Dict:
    """Get metadata about a showcase"""
    path = get_showcase_path(name)
    if not path.exists():
        return {}
    
    data = load_showcase(name)
    if not data:
        return {}
    
    info = {
        'name': name,
        'is_baseline': name == BASELINE_NAME,
        'size_kb': path.stat().st_size / 1024,
        'modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat()
    }
    
    # Add variant-specific info if present
    if '_variant_info' in data:
        info.update(data['_variant_info'])
    
    return info

def rename_showcase(old_name: str, new_name: str) -> bool:
    """Rename a showcase (cannot rename baseline)"""
    if old_name == BASELINE_NAME:
        return False
    
    old_path = get_showcase_path(old_name)
    new_path = get_showcase_path(new_name)
    
    if not old_path.exists() or new_path.exists():
        return False
    
    try:
        old_path.rename(new_path)
        return True
    except Exception as e:
        print(f"Error renaming showcase: {e}")
        return False
