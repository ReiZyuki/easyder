from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="easyder",
    version="0.2.0",
    author="ReiZyuki",
    author_email="rei@example.com",
    description="EASYDER - CSS-inspired video downloader with automatic cookie fallback",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ReiZyuki/easyder",
    project_urls={
        "Bug Tracker": "https://github.com/ReiZyuki/easyder/issues",
        "Documentation": "https://github.com/ReiZyuki/easyder#readme",
        "Source Code": "https://github.com/ReiZyuki/easyder",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "yt-dlp>=2023.12.30",
        "requests>=2.31.0",
    ],
    extras_require={
        "gallery": ["gallery-dl>=1.26.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords=[
        "video",
        "downloader",
        "youtube",
        "instagram",
        "tiktok",
        "yt-dlp",
        "ffmpeg",
        "css-inspired",
        "easy",
    ],
    zip_safe=False,
)
