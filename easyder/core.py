"""
EASYDER Core Module
CSS-inspired video downloader with automatic cookie fallback
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import yt_dlp
import requests

# Default download directory
DEFAULT_DOWNLOAD_DIR = "/storage/emulated/0/Download/ReiDownloader/"

# Video quality mapping
QUALITY_MAP = {
    0: "audio",
    2: "360p",
    3: "480p",
    4: "720p",
    5: "1080p",
    6: "best"
}


class EasyDer:
    """Main EASYDER handler"""
    
    def __init__(self, cookies_list: Optional[List[str]] = None):
        self.cookies_list = cookies_list or []
        self.download_dir = DEFAULT_DOWNLOAD_DIR
        self._ensure_dir()
    
    def _ensure_dir(self):
        """Create download directory if it doesn't exist"""
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
    
    def _test_url_without_cookies(self, url: str) -> bool:
        """Test if URL works without cookies"""
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
                ydl.extract_info(url, download=False)
            return True
        except Exception:
            return False
    
    def _test_cookie_file(self, url: str, cookie_path: str) -> bool:
        """Test if a specific cookie file works"""
        try:
            if not os.path.exists(cookie_path):
                return False
            
            with yt_dlp.YoutubeDL({
                "quiet": True,
                "no_warnings": True,
                "cookiefile": cookie_path
            }) as ydl:
                ydl.extract_info(url, download=False)
            return True
        except Exception:
            return False
    
    def _find_working_cookie(self, url: str) -> Optional[str]:
        """Find first working cookie from supplied list"""
        for cookie_path in self.cookies_list:
            if self._test_cookie_file(url, cookie_path):
                return cookie_path
        return None
    
    def _get_ydl_opts(self, quality: int = 4, cookie_file: Optional[str] = None) -> Dict[str, Any]:
        """Get yt-dlp options based on quality and cookies"""
        opts = {
            "quiet": False,
            "no_warnings": True,
            "outtmpl": os.path.join(self.download_dir, "%(title)s.%(ext)s"),
            "format": self._get_format_string(quality),
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4"
            }]
        }
        
        if cookie_file and os.path.exists(cookie_file):
            opts["cookiefile"] = cookie_file
        
        return opts
    
    def _get_format_string(self, quality: int) -> str:
        """Get yt-dlp format string based on quality number"""
        quality_formats = {
            0: "bestaudio/best",  # audio only
            2: "bestvideo[height<=360]+bestaudio/best",
            3: "bestvideo[height<=480]+bestaudio/best",
            4: "bestvideo[height<=720]+bestaudio/best",
            5: "bestvideo[height<=1080]+bestaudio/best",
            6: "bestvideo+bestaudio/best"
        }
        return quality_formats.get(quality, quality_formats[4])
    
    def _extract_metadata(self, url: str, cookie_file: Optional[str] = None) -> Dict[str, Any]:
        """Extract metadata from URL"""
        opts = {
            "quiet": True,
            "no_warnings": True
        }
        
        if cookie_file and os.path.exists(cookie_file):
            opts["cookiefile"] = cookie_file
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        return info
    
    def _download_thumbnail(self, thumbnail_url: str, title: str) -> str:
        """Download thumbnail image"""
        try:
            response = requests.get(thumbnail_url, timeout=10)
            response.raise_for_status()
            
            # Determine file extension
            ext = ".jpg"
            content_type = response.headers.get("content-type", "")
            if "png" in content_type:
                ext = ".png"
            elif "webp" in content_type:
                ext = ".webp"
            
            # Save thumbnail
            safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).rstrip()
            thumb_path = os.path.join(self.download_dir, f"{safe_title}_thumb{ext}")
            
            with open(thumb_path, "wb") as f:
                f.write(response.content)
            
            return thumb_path
        except Exception as e:
            raise Exception(f"Thumbnail download failed: {e}")
    
    def _process_selector(self, selector: str, value: str, url: str, cookie_file: Optional[str] = None) -> Any:
        """Process individual CSS-like selector"""
        
        # Video quality selector: video[NUMBER]
        if selector.startswith("video[") and selector.endswith("]"):
            quality_str = selector[6:-1]
            if quality_str.isdigit():
                quality = int(quality_str)
                return self._download_video(url, quality, cookie_file)
        
        # Video test mode: video:10
        if selector == "video:10":
            return self._test_video_download(url, cookie_file)
        
        # Metadata selectors
        metadata = self._extract_metadata(url, cookie_file)
        
        if selector == "title":
            return metadata.get("title", "Unknown")
        elif selector == "creator":
            return metadata.get("uploader", metadata.get("channel", "Unknown"))
        elif selector == "url":
            return metadata.get("webpage_url", url)
        elif selector == "views":
            return metadata.get("view_count", 0)
        elif selector == "likes":
            return metadata.get("like_count", 0)
        elif selector == "count":
            return metadata.get("comment_count", 0)
        elif selector == "time":
            return metadata.get("duration", 0)
        elif selector == "thumbnail":
            thumbnail_url = metadata.get("thumbnail")
            if thumbnail_url:
                return self._download_thumbnail(thumbnail_url, metadata.get("title", "thumb"))
            return None
        elif selector == "formats":
            return metadata.get("formats", [])
        
        return None
    
    def _download_video(self, url: str, quality: int, cookie_file: Optional[str] = None) -> str:
        """Download video at specified quality"""
        opts = self._get_ydl_opts(quality, cookie_file)
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
        
        return os.path.join(self.download_dir, f"{info['title']}.mp4")
    
    def _test_video_download(self, url: str, cookie_file: Optional[str] = None) -> Dict[str, Any]:
        """Test video download (video:10 mode)"""
        metadata = self._extract_metadata(url, cookie_file)
        return {
            "test_mode": True,
            "title": metadata.get("title"),
            "duration": metadata.get("duration"),
            "formats_available": len(metadata.get("formats", [])),
            "can_download": True
        }
    
    def _process_playlist(self, playlist_spec: str, url: str, cookie_file: Optional[str] = None) -> List[Dict[str, Any]]:
        """Process playlist with quality:skip:count syntax"""
        try:
            parts = playlist_spec.split(":")
            if len(parts) != 3:
                raise ValueError("Playlist format must be QUALITY:SKIP:COUNT")
            
            quality = int(parts[0])
            skip = int(parts[1])
            count = int(parts[2])
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid playlist syntax: {e}")
        
        # Extract playlist info
        opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": "in_playlist"
        }
        
        if cookie_file and os.path.exists(cookie_file):
            opts["cookiefile"] = cookie_file
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        # Get playlist entries
        entries = info.get("entries", [])
        
        # Apply skip and count
        selected_entries = entries[skip:skip + count]
        
        results = []
        for entry in selected_entries:
            try:
                entry_url = entry.get("url") or entry.get("webpage_url")
                if entry_url:
                    video_path = self._download_video(entry_url, quality, cookie_file)
                    results.append({
                        "title": entry.get("title"),
                        "url": entry_url,
                        "path": video_path,
                        "status": "downloaded"
                    })
            except Exception as e:
                results.append({
                    "title": entry.get("title"),
                    "url": entry.get("url"),
                    "status": "failed",
                    "error": str(e)
                })
        
        return results
    
    def process(self, selectors: Dict[str, str], url: str) -> Dict[str, Any]:
        """Main processing function - handles automatic cookie fallback"""
        
        result = {}
        
        # Step 1: Try without cookies
        cookie_file = None
        works_without_cookies = self._test_url_without_cookies(url)
        
        # Step 2: If fails, find working cookie
        if not works_without_cookies and self.cookies_list:
            cookie_file = self._find_working_cookie(url)
            if not cookie_file:
                raise Exception("URL failed without cookies and no working cookie found")
        
        # Step 3: Process each selector
        for selector, value in selectors.items():
            if selector == "playlist":
                result[value] = self._process_playlist(value, url, cookie_file)
            elif selector == "gallery":
                result[value] = self._process_gallery(url, cookie_file)
            else:
                result[value] = self._process_selector(selector, value, url, cookie_file)
        
        return result
    
    def _process_gallery(self, url: str, cookie_file: Optional[str] = None) -> str:
        """Process gallery downloads (requires gallery-dl)"""
        try:
            import gallery_dl
        except ImportError:
            raise ImportError("gallery-dl not installed. Install with: pip install gallery-dl")
        
        # Basic gallery-dl implementation
        opts = ["gallery-dl", url, "-d", self.download_dir]
        
        if cookie_file and os.path.exists(cookie_file):
            opts.extend(["--cookies", cookie_file])
        
        subprocess.run(opts, check=True)
        return f"Gallery downloaded to {self.download_dir}"


def rz(selectors: Dict[str, str], url: str, cookies: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Main EASYDER function
    
    Args:
        selectors: CSS-inspired selector dictionary
        url: Target URL
        cookies: Optional list of cookie file paths (uses global Cooki if available)
    
    Returns:
        Dictionary with processed results
    
    Example:
        from easyder import rz
        
        result = rz({
            "video[4]": "video",
            "title": "title",
            "creator": "creator"
        }, "https://www.youtube.com/watch?v=...")
    """
    
    # Check for global Cooki variable
    import sys
    frame = sys._getframe(1)
    cooki = frame.f_globals.get("Cooki", [])
    
    # Use provided cookies or fallback to global Cooki
    cookie_list = cookies or cooki or []
    
    handler = EasyDer(cookie_list)
    return handler.process(selectors, url)
