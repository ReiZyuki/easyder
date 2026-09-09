EASYDER — CSS-Inspired Video Downloader

""Python 3.8+" (https://img.shields.io/badge/python-3.8+-blue.svg)" (https://www.python.org/downloads/)
""License: MIT" (https://img.shields.io/badge/License-MIT-yellow.svg)" (https://opensource.org/licenses/MIT)

EASYDER is a CSS-inspired video downloader built with yt-dlp + FFmpeg.

Easyder V1.0 focuses on downloading video/audio, extracting metadata, downloading thumbnails, handling playlists, and automatically trying supplied cookie files when a normal request fails.

---

Features

- ✅ CSS-inspired dictionary syntax
- ✅ Video quality selection
- ✅ Audio-only downloads
- ✅ 360p, 480p, 720p and 1080p quality stages
- ✅ Original/best quality selection
- ✅ Automatic cookie fallback
- ✅ Multiple supplied cookie files
- ✅ Playlist downloads
- ✅ Video metadata extraction
- ✅ Thumbnail downloading
- ✅ yt-dlp + FFmpeg based downloading
- ✅ Download progress display
- ✅ MP4 output for video downloads

---

Installation

From PyPI

pip install easyder

From GitHub

git clone https://github.com/ReiZyuki/Easyder.git
cd Easyder
pip install -e .

---

Quick Start

from easyder import rz

result = rz(
    {
        "video[3]": "video",
        "title": "title",
        "creator": "creator",
    },
    url,
)

print("Video:", result["video"])
print("Title:", result["title"])
print("Creator:", result["creator"])

The right-side values such as ""video"", ""title"" and ""creator"" are user-defined variable names.

---

Video Quality

Easyder uses CSS-inspired quality selectors:

"video[0]"
"video[1]"
"video[2]"
"video[3]"
"video[4]"
"video[5]"

Selector| Quality
"video[0]"| Audio only
"video[1]"| 360p
"video[2]"| 480p
"video[3]"| 720p
"video[4]"| 1080p
"video[5]"| Best/original available quality

Example:

from easyder import rz

result = rz(
    {
        "video[4]": "video",
    },
    url,
)

print(result["video"])

If the requested quality is unavailable, yt-dlp selects an appropriate available format according to Easyder's format selection rules.

---

Audio Only

Use "video[0]" for audio:

from easyder import rz

result = rz(
    {
        "video[0]": "audio",
    },
    url,
)

print(result["audio"])

---

Metadata

Easyder can extract video metadata without downloading the video.

from easyder import rz

result = rz(
    {
        "title": "title",
        "creator": "creator",
        "url": "video_url",
        "views": "views",
        "likes": "likes",
        "count": "comments",
        "time": "duration",
        "thumbnail": "thumbnail",
        "formats": "formats",
    },
    url,
)

print("Title:", result["title"])
print("Creator:", result["creator"])
print("URL:", result["video_url"])
print("Views:", result["views"])
print("Likes:", result["likes"])
print("Comments:", result["comments"])
print("Duration:", result["duration"])
print("Thumbnail:", result["thumbnail"])
print("Formats:", result["formats"])

Metadata variable names are completely user-defined.

For example:

result = rz(
    {
        "title": "MyTitle",
        "creator": "MyCreator",
    },
    url,
)

print(result["MyTitle"])
print(result["MyCreator"])

---

Thumbnail

Use the "thumbnail" selector to download the video's thumbnail.

from easyder import rz

result = rz(
    {
        "thumbnail": "thumb",
    },
    url,
)

print(result["thumb"])

The returned value is the path of the downloaded thumbnail.

Default download directory:

/storage/emulated/0/Download/ReiDownloader

---

Playlist

Playlist syntax:

"playlist": "QUALITY:SKIP:COUNT"

Example:

from easyder import rz

result = rz(
    {
        "playlist": "3:5:10",
    },
    playlist_url,
)

print(result["videos"])

Meaning:

3 = 720p
5 = skip the first 5 videos
10 = download the next 10 videos

Quality values

Quality| Meaning
"0"| Audio
"1"| 360p
"2"| 480p
"3"| 720p
"4"| 1080p
"5"| Best/original

Example:

result = rz(
    {
        "playlist": "4:0:5",
    },
    playlist_url,
)

This requests:

1080p
Skip 0
Download 5 videos

Downloaded playlist files are returned in:

result["videos"]

---

Automatic Cookie Fallback

Easyder first attempts the request without cookies.

If the normal request fails, Easyder checks the cookie files supplied through the "Cooki" variable.

from easyder import rz

Cooki = [
    "/storage/emulated/0/Download/youtube.txt",
    "/storage/emulated/0/Download/other.txt",
]

result = rz(
    {
        "video[3]": "video",
        "title": "title",
    },
    url,
)

Easyder tests the supplied cookie files one by one and uses the first working cookie.

No cookie filenames are hardcoded by Easyder.

---

Cookie Variable

The cookie variable name is:

Cooki

It can contain a single path:

Cooki = "/path/to/cookies.txt"

or multiple paths:

Cooki = [
    "/path/to/cookies1.txt",
    "/path/to/cookies2.txt",
]

Easyder does not scan directories for cookie files.

---

Progress

During downloads Easyder displays progress information similar to:

Downloading: 1080p
[Download 50%] [Network 2.0 MB/s] [Mode Video]

The downloader can also receive a progress callback:

from easyder import rz

def progress(percent, network, mode):
    print(percent, network, mode)

result = rz(
    {
        "video[3]": "video",
    },
    url,
    progress_callback=progress,
)

The callback receives:

percent
network
mode

---

Custom Variable Names

Easyder does not require fixed output variable names.

For example:

result = rz(
    {
        "video[3]": "MyVideo",
        "title": "MyTitle",
        "creator": "MyCreator",
        "thumbnail": "MyThumbnail",
    },
    url,
)

Then:

print(result["MyVideo"])
print(result["MyTitle"])
print(result["MyCreator"])
print(result["MyThumbnail"])

This keeps the selector syntax separate from the variable names used by your application.

---

Complete Example

from easyder import rz

Cooki = [
    "/storage/emulated/0/Download/youtube.txt",
]

result = rz(
    {
        "video[4]": "video",
        "title": "title",
        "creator": "creator",
        "thumbnail": "thumbnail",
        "views": "views",
        "likes": "likes",
        "time": "duration",
    },
    url,
)

print("Video:", result["video"])
print("Title:", result["title"])
print("Creator:", result["creator"])
print("Thumbnail:", result["thumbnail"])
print("Views:", result["views"])
print("Likes:", result["likes"])
print("Duration:", result["duration"])

---

Selector Reference

Selector| Example value| Description
"video[0]"| ""video""| Audio only
"video[1]"| ""video""| 360p video
"video[2]"| ""video""| 480p video
"video[3]"| ""video""| 720p video
"video[4]"| ""video""| 1080p video
"video[5]"| ""video""| Best/original quality
"title"| ""title""| Video title
"creator"| ""creator""| Uploader/creator
"url"| ""video_url""| Video URL
"views"| ""views""| View count
"likes"| ""likes""| Like count
"count"| ""comments""| Comment count
"time"| ""duration""| Duration
"thumbnail"| ""thumbnail""| Download thumbnail
"formats"| ""formats""| Available formats
"playlist"| ""QUALITY:SKIP:COUNT""| Playlist download

---

Quality Reference

video[0] = Audio only
video[1] = 360p
video[2] = 480p
video[3] = 720p
video[4] = 1080p
video[5] = Best/original available

---

Requirements

Easyder uses:

- Python
- yt-dlp
- FFmpeg

FFmpeg is required for media processing and merging separate video/audio streams.

---

Download Location

The default download directory is:

/storage/emulated/0/Download/ReiDownloader

Videos and thumbnails downloaded by Easyder are stored there.

---

V1.0 Scope

Easyder V1.0 intentionally focuses on:

Video
Audio
Thumbnail
Metadata
Playlist
Automatic cookie fallback
Progress reporting

Easyder V1.0 does not include:

Gallery / gallery-dl
Telegram / TeleBot integration
Sender functionality

These features may be considered separately in future versions.

---

License

MIT License
