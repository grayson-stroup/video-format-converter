# Video Converter

A modern, beautiful GUI application for converting videos between formats and creating high-quality GIFs. Built with **CustomTkinter** for an iOS-inspired design with rounded corners and smooth animations.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

<img src="videoConverterApp.png" alt="Video Converter App" width="500">

## ✨ Features

- 🎬 **Multi-Format Support** - Convert between MP4, MOV, MKV, WEBM, and AVI
- 🎨 **High-Quality GIF Creation** - Perfect for knowledge bases and release notes
- 📊 **GIF Quality Control** - Adjustable FPS (10-30) and resolution (50-100%)
- 🎯 **Batch Conversion** - Convert multiple videos at once
- 💎 **Crystal Clear GIFs** - Optimized settings prevent grainy output
- 🌙 **Modern Dark UI** - Beautiful three-card layout with rounded corners (#2A7AE8 blue)
- 📁 **Flexible Output** - Save to custom folder or same location as source
- ✓ **Status Indicators** - Visual feedback (✓ green, ○ grey) for field completion
- ⚡ **Background Processing** - UI stays responsive during conversion
- 📈 **Real-time Status** - Live progress updates with animated messages
- 🔒 **Privacy-Friendly** - Smart path display protects personal information

## 🎥 Supported Formats

### Input Formats
- **MP4** - MPEG-4 video
- **MOV** - Apple QuickTime
- **MKV** - Matroska video
- **WEBM** - WebM video
- **AVI** - Audio Video Interleave

### Output Formats
- **MP4** - Best for web and mobile
- **MOV** - Best for Apple devices
- **MKV** - Best for high-quality archiving
- **WEBM** - Best for web (smaller file size)
- **AVI** - Legacy format support
- **GIF** - Auto-playing animations (perfect for documentation!)

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- FFmpeg (required by moviepy)

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to PATH

### Installation

**Option 1: Automated Setup (Recommended)**

Use the setup script to install everything automatically:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- ✅ Check for and install FFmpeg (via Homebrew on macOS or apt on Linux)
- ✅ Install all Python dependencies
- ✅ Verify everything is ready

**Option 2: Manual Installation**

1. **Install FFmpeg** (required by moviepy):

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

2. **Install Python dependencies:**

```bash
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install customtkinter moviepy imageio imageio-ffmpeg
```

> **Note:** moviepy requires `imageio` and `imageio-ffmpeg` as dependencies. These are included in requirements.txt.

### Run the Application

```bash
python3 convertVideo.py
```

## 📖 Usage

### Basic Workflow

1. **Launch the app**
   ```bash
   python3 convertVideo.py
   ```

2. **Select Videos**
   - Click "Browse Files"
   - Select one or more video files
   - Supports all major formats
   - Green checkmark (✓) appears when files are selected

3. **Choose Output Format**
   - Select from dropdown: MP4, MOV, MKV, WEBM, AVI, or GIF

4. **Adjust GIF Settings** (if converting to GIF)
   - **Frame Rate (FPS):** 10-30 fps (default: 15)
     - Higher = smoother but larger file
     - 15 fps is perfect for most use cases
   - **Resolution:** 50-100% (default: 100%)
     - Lower for smaller file size
     - 100% for best quality

5. **(Optional) Select Output Folder**
   - Click "Browse Folder" to choose where to save
   - Or leave default to save alongside original files
   - Grey circle (○) changes to green checkmark (✓) when ready

6. **Convert**
   - Click "Convert Videos"
   - Watch real-time progress with animated status messages
   - Done! 🎉

### Example: Creating GIFs for Documentation

**Perfect for Knowledge Bases and Release Notes!**

1. Select your screen recording video
2. Choose "GIF" from dropdown
3. Set FPS to 15 (smooth and clear)
4. Keep resolution at 100% for crisp text
5. Convert!

**Result:** A high-quality, auto-playing GIF that looks great in documentation without requiring users to click play!

## 🎨 GIF Quality Settings Explained

### Frame Rate (FPS)

- **10 FPS** - Minimal animation, smallest file
- **15 FPS** - ⭐ **Recommended** - Smooth and clear
- **20 FPS** - Very smooth, larger file
- **30 FPS** - Silky smooth, largest file

### Resolution

- **50%** - Half size, much smaller file
- **75%** - Good balance
- **100%** - ⭐ **Recommended** - Full quality, no scaling

### Tips for Best Quality

✅ **DO:**
- Use 15-20 FPS for smooth motion
- Keep resolution at 100% for text clarity
- Keep videos under 30 seconds for GIFs
- Use good source quality

❌ **AVOID:**
- Very low FPS (looks choppy)
- Scaling down too much (text becomes unreadable)
- Converting very long videos to GIF (huge file sizes)

## 🎬 Conversion Examples

### Convert to MP4 (Universal)
```
Select: video.mov
Format: MP4
Output: video.mp4 (web-compatible)
```

### Create Documentation GIF
```
Select: demo-recording.mp4
Format: GIF
FPS: 15
Resolution: 100%
Output: demo-recording.gif (auto-plays in docs!)
```

### Batch Convert to WEBM
```
Select: video1.mp4, video2.mov, video3.avi
Format: WEBM
Output: 3 optimized WEBM files
```

## 🛠️ Technical Details

### Video Processing

- **Engine:** MoviePy (Python video editing)
- **Encoding:** FFmpeg backend
- **Codecs:**
  - MP4/MOV/MKV: H.264 (libx264)
  - WEBM: VP8 (libvpx)
  - AVI: MPEG-4
- **Audio:** AAC for MP4/MOV/MKV, Vorbis for WEBM

### GIF Optimization

- **Program:** FFmpeg with OptimizePlus
- **Fuzz Factor:** 1 (reduces size while maintaining quality)
- **Color Optimization:** Automatic palette generation
- **Frame Optimization:** Removes duplicate frames

## 🎨 UI Features

- **Modern Dark Theme** - Elegant dark interface
- **Three-Card Layout** - Side-by-side design for easy navigation
- **Rounded Corners** - 15-25px radius (iOS-style)
- **Blue Accent Color** - #2A7AE8 buttons with hover effects
- **Status Indicators** - Visual feedback (✓ green, ○ grey) for field completion
- **Dynamic UI** - GIF settings appear only when needed
- **Sliders** - Easy adjustment of FPS and resolution
- **Progress Bar** - Visual feedback during conversion with disabled appearance when inactive
- **Animated Messages** - Fun "thinking messages" every 8-10 seconds during conversion
- **Privacy-Friendly Paths** - Smart display (`.../Desktop`) protects personal info
- **Real-time Feedback** - Live value display and conversion status
- **Auto-Focus** - Window automatically appears on top when launched
- **Large Status Area** - Detailed conversion logs with color-coded messages

## 📁 Project Structure

```
Video Converter/
├── convertVideo.py         # Main GUI application
├── requirements.txt        # Python dependencies
├── setup.sh               # Automated setup script (installs FFmpeg + Python packages)
├── fix_moviepy.sh         # Script to fix moviepy 2.x issues
├── LICENSE                # MIT License
├── videoConverterApp.png  # Screenshot for README
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## 🛠️ Troubleshooting

### "No module named 'moviepy'"

Install moviepy:
```bash
pip3 install moviepy
```

### "FFmpeg not found"

MoviePy requires FFmpeg. Install it:

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to system PATH

### GIF looks grainy or low quality

Try these settings:
- Increase FPS to 20
- Keep resolution at 100%
- Use a high-quality source video
- Keep the video short (under 30 seconds)

### Conversion is slow

This is normal! Video conversion is CPU-intensive:
- Large files take longer
- GIF conversion is slower than video-to-video
- The app remains responsive (runs in background thread)

### "No module named 'tkinter'"

See the Image Converter README for tkinter installation instructions.

## 📝 Requirements

```
customtkinter>=5.2.0    # Modern UI framework
moviepy>=1.0.3          # Video processing
imageio>=2.9.0          # Image/video I/O (required by moviepy)
imageio-ffmpeg>=0.4.8   # FFmpeg wrapper (required by moviepy)
```

**System Requirements:**
- Python 3.7+
- FFmpeg (must be installed separately via system package manager)
- tkinter (usually comes with Python)

## 🤝 Contributing

This is a personal project shared for educational and practical use. While I appreciate interest in the project:

- 🐛 **Bug Reports**: Feel free to open issues for bugs you encounter
- 💡 **Feature Requests**: You can suggest features, but I may not implement them
- 🔧 **Pull Requests**: I review PRs when time permits, but responses may be slow
- 📚 **Documentation**: Improvements to docs are always welcome!

**Note:** This project is maintained on a best-effort basis in my spare time. I may not be able to respond to all issues or requests promptly. Feel free to fork the project for your own needs!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This means you're free to use, modify, and distribute this software for personal or commercial use.

## 💡 Use Cases

### Perfect For:

- 📚 **Knowledge Base Articles** - GIFs auto-play, no play button needed
- 📝 **Release Notes** - Show new features in action
- 🎓 **Tutorials** - Step-by-step visual guides
- 📧 **Email Campaigns** - Animated content that works everywhere
- 💬 **Slack/Teams** - Share quick demos
- 🐛 **Bug Reports** - Show issues clearly
- 📱 **Mobile Optimization** - Convert to efficient formats

### Why GIFs for Documentation?

✅ Auto-play (no user interaction needed)
✅ Work in emails and most platforms
✅ No video player required
✅ Smaller than videos for short clips
✅ Great for showing UI interactions

## 🔮 Future Enhancements

- [ ] Drag-and-drop file support
- [ ] Video trimming/cutting
- [ ] Batch rename functionality
- [ ] Preset profiles (Documentation, Web, High Quality, etc.)
- [ ] Progress bars for individual files
- [ ] Video preview before conversion
- [ ] Subtitle/watermark support
- [ ] Audio extraction

---

Made with ❤️ for easy video conversion

