# EASYDER - CSS-Inspired Video Downloader

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**EASYDER** is a powerful, CSS-inspired video downloader built on **yt-dlp** + **FFmpeg** with automatic cookie fallback, playlist support, and metadata extraction.

## Features

✅ **CSS-Inspired Syntax** - Declarative selectors instead of complex parameters  
✅ **Automatic Cookie Fallback** - Try without cookies first, auto-test if needed  
✅ **Video Quality Selection** - `video[0]` to `video[5]` for different qualities  
✅ **Playlist Support** - `"playlist": "3:5:10"` = Quality 3 (720p), skip 5, download 10  
✅ **Metadata Extraction** - Title, creator, views, likes, duration, thumbnail  
✅ **TeleBot Integration** - Easy to use inside Telegram bots  
✅ **Gallery Support** - Optional gallery-dl integration  

## Installation

### PyPI (Recommended)

```bash
pip install easyder
```

### From GitHub

```bash
git clone https://github.com/ReiZyuki/easyder.git
cd easyder
pip install -e .
```

### With Gallery Support

```bash
pip install easyder[gallery]
```

## Quick Start

### Basic Video Download

```python
from easyder import rz

# Download 720p video
result = rz({
    "video[3]": "video",      # 720p quality
    "title": "title",
    "creator": "creator"
}, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

print(f"Downloaded: {result['video']}")
print(f"Title: {result['title']}")
print(f"Creator: {result['creator']}")
```

### With Automatic Cookies

```python
from easyder import rz

# Define cookie paths
Cooki = [
    "/storage/emulated/0/Download/youtube.txt",
    "/storage/emulated/0/Download/instagram.txt"
]

# EASYDER automatically tests cookies if needed
result = rz({
    "video[3]": "video",
    "title": "title"
}, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

### Video Quality Selector

```python
# video[0] = audio only
# video[1] = 360p
# video[2] = 480p
# video[3] = 720p (default)
# video[4] = 1080p
# video[5] = original/best quality

result = rz({
    "video[4]": "video",  # 1080p
    "title": "title"
}, url)
```

### Video Test Mode

```python
# Test if video can be downloaded without actual download
result = rz({
    "video:10": "video",
    "title": "title"
}, url)

# Returns:
# {
#     "video": {
#         "test_mode": True,
#         "title": "Video Title",
#         "duration": 300,
#         "formats_available": 15,
#         "can_download": True
#     },
#     "title": "Video Title"
# }
```

### Playlist Download

```python
# "playlist": "QUALITY:SKIP:COUNT"
# Quality 3 = 720p
# Skip first 5 videos
# Download next 10 videos

result = rz({
    "playlist": "3:5:10",
    "title": "title"
}, "https://www.youtube.com/playlist?list=...")

# Returns list of downloaded videos
for video in result['3:5:10']:
    print(f"{video['title']} → {video['path']}")
```

### Metadata Extraction

```python
result = rz({
    "title": "title",
    "creator": "creator",
    "url": "video_url",
    "views": "views",
    "likes": "likes",
    "count": "comments",
    "time": "duration",
    "thumbnail": "thumbnail",
    "formats": "formats"
}, url)

print(f"Title: {result['title']}")
print(f"Creator: {result['creator']}")
print(f"Views: {result['views']:,}")
print(f"Duration: {result['time']} seconds")
print(f"Thumbnail: {result['thumbnail']}")
```

### TeleBot Integration

```python
import telebot
from easyder import rz

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

Cooki = [
    "/storage/emulated/0/Download/youtube.txt",
    "/storage/emulated/0/Download/instagram.txt"
]

@bot.message_handler(commands=["video"])
def video(message):
    url = message.text.replace("/video", "", 1).strip()
    
    if not url:
        bot.reply_to(message, "URL bhejo.")
        return
    
    try:
        result = rz({
            "video[3]": "video",      # 720p
            "title": "title",
            "creator": "creator"
        }, url)
        
        bot.reply_to(
            message,
            f"✅ Downloaded!\n"
            f"Title: {result['title']}\n"
            f"Creator: {result['creator']}\n"
            f"Video: {result['video']}"
        )
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

bot.infinity_polling()
```

### Gallery Download

```python
# Requires: pip install easyder[gallery]

result = rz({
    "gallery": "images"
}, "https://imgur.com/gallery/...")

print(result)
```

## Selector Reference

| Selector | Value | Description |
|----------|-------|-------------|
| `video[0]` | `"video"` | Download audio only |
| `video[1]` | `"video"` | Download in 360p |
| `video[2]` | `"video"` | Download in 480p |
| `video[3]` | `"video"` | Download in 720p |
| `video[4]` | `"video"` | Download in 1080p |
| `video[5]` | `"video"` | Download in original/best quality |
| `video:10` | `"video"` | Test video download capability |
| `title` | `"title"` | Get video title |
| `creator` | `"creator"` | Get uploader/channel name |
| `url` | `"video_url"` | Get video URL |
| `views` | `"views"` | Get view count |
| `likes` | `"likes"` | Get like count |
| `count` | `"comments"` | Get comment count |
| `time` | `"duration"` | Get duration in seconds |
| `thumbnail` | `"thumbnail"` | Download thumbnail image |
| `formats` | `"formats"` | Get available formats |
| `playlist` | `"QUALITY:SKIP:COUNT"` | Download playlist videos |
| `gallery` | `"images"` | Download gallery images |

## Quality Levels Reference

```
video[0] = Audio Only (MP3/M4A)
video[1] = 360p (Low Quality)
video[2] = 480p (Medium Quality)
video[3] = 720p (HD - Default)
video[4] = 1080p (Full HD)
video[5] = Original/Best (Highest Available)
```

## Playlist Syntax Reference

```
"playlist": "QUALITY:SKIP:COUNT"

QUALITY = video quality level (0-5)
SKIP    = number of items to skip from start
COUNT   = number of items to download

Example:
"playlist": "3:5:10"
  ↓
Quality 3 (720p), skip first 5 items, download next 10
```

## Automatic Cookie Fallback

EASYDER follows this intelligent flow:

1. **Try without cookies** - If successful, return result immediately
2. **If failed** - Check if `Cooki` variable exists in caller's scope
3. **Test cookies one by one** - From the supplied list in order
4. **Use first working cookie** - Retry operation with it
5. **If all fail** - Raise original error with details

```python
Cooki = [
    "/path/to/youtube.txt",
    "/path/to/instagram.txt",
    "/path/to/reddit.txt"
]

# Cookies are tested automatically if needed!
result = rz({"video[3]": "video"}, url)
```

## Download Location

**Default:** `/storage/emulated/0/Download/ReiDownloader/`

All videos, thumbnails, and other media are saved here automatically.

## Requirements

- Python 3.8+
- yt-dlp (>= 2023.12.30)
- FFmpeg (system requirement)
- requests (>= 2.31.0)

### Optional

- gallery-dl (>= 1.26.0) - For gallery support

## Installation on Different Platforms

### Linux/Mac
```bash
# Install FFmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Ubuntu/Debian

# Install package
pip install easyder
```

### Windows
```bash
# Download FFmpeg from https://ffmpeg.org/download.html
# Add to PATH

pip install easyder
```

### Android (Termux)
```bash
pkg install python ffmpeg
pip install easyder
```

## Troubleshooting

### "FFmpeg not found"
Install FFmpeg on your system:
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from https://ffmpeg.org/download.html
- **Android (Termux)**: `pkg install ffmpeg`

### "Gallery-dl not installed"
Install with: `pip install easyder[gallery]`

### Video download fails
1. Check if URL is valid
2. Try with `video:10` (test mode) first
3. Add cookie files to `Cooki` variable
4. Check if FFmpeg is installed
5. Check internet connection

### "URL failed without cookies and no working cookie found"
- Add valid cookie files to `Cooki` list
- Cookie files must be in Netscape format
- Check if cookies are expired

## Common Use Cases

### Download Best Quality Video
```python
result = rz({
    "video[5]": "video",  # Original/Best
    "title": "title"
}, url)
```

### Download Audio Only
```python
result = rz({
    "video[0]": "video",  # Audio
    "title": "title"
}, url)
```

### Get All Video Info
```python
result = rz({
    "video[3]": "video",
    "title": "title",
    "creator": "creator",
    "views": "views",
    "likes": "likes",
    "time": "duration",
    "thumbnail": "thumbnail"
}, url)
```

### Download Full Playlist
```python
result = rz({
    "playlist": "3:0:999",  # Quality 3, skip 0, download all
    "title": "title"
}, playlist_url)
```

## License

MIT License - See LICENSE file

## Author

**ReiZyuki** - https://github.com/ReiZyuki

## Contributing

Pull requests welcome! Please feel free to fork and improve.

---

Made with ❤️ for easy video downloading
