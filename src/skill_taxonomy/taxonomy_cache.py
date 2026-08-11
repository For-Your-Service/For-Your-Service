"""
Taxonomy Cache

Local caching for O*NET taxonomy data to minimize API calls.
Uses JSON file storage for persistence across sessions.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime, timedelta


class TaxonomyCache:
    """File-based cache for skill taxonomy data"""
    
    def __init__(self, cache_dir: Optional[str] = None, ttl_days: int = 30):
        """
        Initialize taxonomy cache
        
        Args:
            cache_dir: Directory for cache files (default: ~/.fys_cache)
            ttl_days: Time-to-live for cache entries in days
        """
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.fys_cache")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.ttl_days = ttl_days
        self.onet_cache_file = self.cache_dir / "onet_cache.json"
        self.skills_cache_file = self.cache_dir / "skills_cache.json"
        
        # Load existing caches
        self.onet_cache = self._load_cache(self.onet_cache_file)
        self.skills_cache = self._load_cache(self.skills_cache_file)
    
    def _load_cache(self, file_path: Path) -> Dict:
        """Load cache from JSON file"""
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Cache load error: {e}")
        return {}
    
    def _save_cache(self, cache: Dict, file_path: Path):
        """Save cache to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            print(f"Cache save error: {e}")
    
    def _is_expired(self, timestamp_str: str) -> bool:
        """Check if cache entry is expired"""
        try:
            cached_time = datetime.fromisoformat(timestamp_str)
            age = datetime.now() - cached_time
            return age > timedelta(days=self.ttl_days)
        except Exception:
            return True
    
    def get_onet_occupation(self, onet_code: str) -> Optional[Dict]:
        """
        Get cached O*NET occupation data
        
        Args:
            onet_code: O*NET-SOC code
            
        Returns:
            Cached occupation data or None if not found/expired
        """
        if onet_code in self.onet_cache:
            entry = self.onet_cache[onet_code]
            if not self._is_expired(entry.get("timestamp", "")):
                return entry.get("data")
        return None
    
    def set_onet_occupation(self, onet_code: str, data: Dict):
        """
        Cache O*NET occupation data
        
        Args:
            onet_code: O*NET-SOC code
            data: Occupation data to cache
        """
        self.onet_cache[onet_code] = {
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self._save_cache(self.onet_cache, self.onet_cache_file)
    
    def get_normalized_skill(self, skill_name: str) -> Optional[Dict]:
        """
        Get cached normalized skill
        
        Args:
            skill_name: Raw skill name
            
        Returns:
            Cached normalized skill or None
        """
        key = skill_name.lower()
        if key in self.skills_cache:
            entry = self.skills_cache[key]
            if not self._is_expired(entry.get("timestamp", "")):
                return entry.get("data")
        return None
    
    def set_normalized_skill(self, skill_name: str, normalized_data: Dict):
        """
        Cache normalized skill data
        
        Args:
            skill_name: Raw skill name
            normalized_data: Normalized skill information
        """
        key = skill_name.lower()
        self.skills_cache[key] = {
            "data": normalized_data,
            "timestamp": datetime.now().isoformat()
        }
        self._save_cache(self.skills_cache, self.skills_cache_file)
    
    def clear_expired(self):
        """Remove expired entries from caches"""
        # Clear expired O*NET entries
        expired_onet = [
            code for code, entry in self.onet_cache.items()
            if self._is_expired(entry.get("timestamp", ""))
        ]
        for code in expired_onet:
            del self.onet_cache[code]
        
        # Clear expired skill entries
        expired_skills = [
            skill for skill, entry in self.skills_cache.items()
            if self._is_expired(entry.get("timestamp", ""))
        ]
        for skill in expired_skills:
            del self.skills_cache[skill]
        
        # Save cleaned caches
        self._save_cache(self.onet_cache, self.onet_cache_file)
        self._save_cache(self.skills_cache, self.skills_cache_file)
        
        return len(expired_onet) + len(expired_skills)
    
    def clear_all(self):
        """Clear all cached data"""
        self.onet_cache = {}
        self.skills_cache = {}
        self._save_cache(self.onet_cache, self.onet_cache_file)
        self._save_cache(self.skills_cache, self.skills_cache_file)
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            "onet_entries": len(self.onet_cache),
            "skill_entries": len(self.skills_cache),
            "cache_dir": str(self.cache_dir),
            "ttl_days": self.ttl_days
        }
