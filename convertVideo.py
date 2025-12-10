#!/usr/bin/env python3
"""
Video Converter - Modern GUI
Convert between video formats (MP4, MOV, MKV, WEBM, AVI) and create high-quality GIFs
Built with CustomTkinter for iOS-inspired design
"""

import os
import re
import sys
import random
import threading
from pathlib import Path
import warnings

import customtkinter as ctk
from tkinter import filedialog, messagebox

try:
    from PIL import Image
except ImportError:
    Image = None


def ensure_antialias_compat():
    """Ensure PIL.Image exposes ANTIALIAS to satisfy MoviePy legacy usage."""
    if Image is None:
        return

    resampling = getattr(Image, "Resampling", None)
    if resampling and not hasattr(Image, "ANTIALIAS"):
        setattr(Image, "ANTIALIAS", getattr(resampling, "LANCZOS", resampling.LANCZOS))


warnings.filterwarnings(
    "ignore",
    message=r"resource_tracker: There appear to be .* leaked semaphore objects to clean up at shutdown: .*",
    category=UserWarning,
    module=r"multiprocessing\.resource_tracker"
)


def _append_warning_filter_env():
    """Add a PYTHONWARNINGS rule to ignore resource_tracker warnings in child processes."""
    filter_rule = "ignore::UserWarning:multiprocessing.resource_tracker"
    existing = os.environ.get("PYTHONWARNINGS", "")
    rules = [rule for rule in existing.split(",") if rule]
    if filter_rule in rules:
        return
    rules.append(filter_rule)
    os.environ["PYTHONWARNINGS"] = ",".join(rules)


_append_warning_filter_env()

# Try to import moviepy with helpful error message
try:
    from moviepy.editor import VideoFileClip
except ImportError as e:
    print("=" * 60)
    print("ERROR: moviepy is not installed or cannot be imported!")
    print("=" * 60)
    print(f"\nImport error details: {e}")
    print(f"\nPython path: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"\n✓ Virtual environment detected: {sys.prefix}")
        print("\nInstall in your virtual environment:")
        print(f"  {sys.executable} -m pip install -r requirements.txt")
    else:
        print("\nInstall moviepy and dependencies:")
        print("  pip3 install moviepy imageio imageio-ffmpeg customtkinter")
        print("\nOr install all requirements:")
        print("  pip3 install -r requirements.txt")
    
    print("\nAlso make sure FFmpeg is installed:")
    print("  macOS: brew install ffmpeg")
    print("  Linux: sudo apt-get install ffmpeg")
    print("=" * 60)
    sys.exit(1)

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VideoConverterApp:
    """
    A modern GUI application for converting video files
    Supports: MP4, MOV, MKV, WEBM, AVI, and GIF
    """
    
    VIDEO_FORMATS = ['MP4', 'MOV', 'MKV', 'WEBM', 'AVI', 'GIF']
    
    # Funny status messages to display during conversion (Claude Code style)
    THINKING_MESSAGES = [
        "🎬 Wrangling pixels into submission...",
        "🔧 Teaching bits new dance moves...",
        "🎨 Convincing frames to get along...",
        "⚡ Negotiating with the codec union...",
        "🎭 Rehearsing the video's new format...",
        "🔮 Consulting the FFmpeg oracle...",
        "🎪 Herding cats... I mean, frames...",
        "🧙 Casting video transformation spell...",
        "🎵 Humming while encoding...",
        "🚀 Launching frames into new dimension...",
        "🎯 Aligning pixels with cosmic precision...",
        "🌀 Spinning up the flux capacitor...",
        "🎸 Teaching audio to play nice...",
        "🔬 Analyzing frame DNA...",
        "🎁 Gift-wrapping your video...",
        "☕ Brewing a fresh batch of frames...",
        "🎲 Rolling for codec compatibility...",
        "🧪 Mixing video potions...",
        "📐 Measuring twice, encoding once...",
        "🎻 Orchestrating the bit symphony...",
        "🌈 Adding a sprinkle of magic...",
        "🔥 Turning up the encoding heat...",
        "🧊 Keeping things cool under pressure...",
        "🎯 Zeroing in on perfection...",
        "🛸 Beaming frames to their new home...",
        "🤖 Asking AI nicely to help...",
        "🎩 Pulling codecs out of a hat...",
        "🧲 Magnetically aligning bits...",
        "🎪 Juggling keyframes...",
        "🌊 Riding the bitrate wave...",
        "🔭 Searching for the perfect frame...",
        "🎯 Playing darts with pixels...",
        "🧩 Solving the video puzzle...",
        "🎨 Bob Ross-ing these frames...",
        "🏋️ Heavy lifting in progress...",
        "🎹 Composing a visual symphony...",
        "🧬 Splicing video genes...",
        "🌪️ Tornado of transformation...",
        "🎡 Taking frames for a spin...",
        "🔐 Unlocking video potential...",
        "🎪 Teaching pixels circus tricks...",
        "🧠 Big brain encoding time...",
        "🎸 Shredding through frames...",
        "🌟 Sprinkling some stardust...",
        "🎭 Frames auditioning for new roles...",
        "🧁 Baking video goodness...",
        "🎯 Pixel perfect in progress...",
        "🚂 All aboard the encode train...",
        "🎨 Finger painting with data...",
        "🔧 Tightening the loose bits...",
        "🎵 Finding the right rhythm...",
        "🌙 Working the night shift...",
        "🎪 Video acrobatics underway...",
        "🧪 Experimental encoding phase...",
        "🎭 Drama-free conversion mode...",
        "🚀 Houston, we have liftoff...",
        "🎬 Lights, camera, encode!",
        "🧙 Abracadabra, new format!",
        "🎸 Rock and roll encoding...",
        "🌈 Chasing the perfect rainbow...",
        "🎯 Bullseye optimization...",
        "☕ Coffee break for the CPU...",
        "🎪 Frame gymnastics routine...",
        "🔮 Reading the codec tea leaves...",
        "🧊 Keeping the bits frosty...",
        "🎹 Tickling the ivories of data...",
        "🌊 Surfing the data stream...",
        "🎨 Painting by numbers (binary)...",
        "🧬 DNA test for your video...",
        "🎭 Standing ovation incoming...",
        "🔧 Fine-tuning the masterpiece...",
        "🎵 Dropping the bass (and treble)...",
        "🚂 Choo choo! Encode express!",
        "🎪 Taming wild pixels...",
        "🧠 Neurons firing on all cylinders...",
        "🌟 Making movie magic...",
        "🎬 Director's cut in progress...",
        "🎸 This one goes to eleven...",
        "🧁 The secret ingredient is love...",
        "🔮 The spirits say... almost done...",
        "🎯 Sniper-level precision...",
        "🌪️ Controlled chaos mode...",
        "🎹 Mozart would be proud...",
        "🧪 Science is happening...",
        "🎭 Oscar-worthy conversion...",
        "🚀 To infinity and beyond!",
        "🎨 Michelangelo of encoding...",
        "☕ Fueled by caffeine and hope...",
        "🌈 Taste the rainbow of bits...",
        "🔧 Wrench in hand, ready to go...",
        "🎵 Symphony of compression...",
        "🧙 Gandalf approved encoding...",
        "🎪 Greatest show on earth...",
        "🌊 Making waves in video land...",
        "🎯 Threading the needle...",
        "🧊 Ice cold execution...",
        "🎬 And... action!",
        "🔮 Fortune favors the encoded...",
        "🎸 Encoding solo in progress...",
        "🧁 Fresh out of the oven soon...",
    ]
    
    def __init__(self, root):
        self.root = root
        self.root.title("Video Converter")
        self.root.geometry("900x900")
        ensure_antialias_compat()
        
        # Set minimum window size
        self.root.minsize(850, 975)
        
        self.selected_files = []
        self.output_folder = None
        self.last_input_dir = os.path.expanduser("~/Documents")
        self.last_output_dir = os.path.expanduser("~/Documents")
        
        # Simulated progress tracking
        self.simulated_progress = 0.0
        self.simulated_progress_running = False
        self.current_file_start_progress = 0.0
        self.current_file_end_progress = 0.0
        
        # Funny message tracking
        self.funny_message_running = False
        self.used_messages = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the modern user interface with CustomTkinter"""
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        
        # Configure grid weights for responsiveness
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(6, weight=1)  # Status area should expand
        
        current_row = 0
        
        # Header section with title and reset action
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=current_row, column=0, columnspan=3, sticky="ew", pady=(0, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        title_label = ctk.CTkLabel(
            header_frame,
            text="Video Converter",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w")

        restart_icon_btn = ctk.CTkButton(
            header_frame,
            text="↻",
            command=self.reset_form,
            width=48,
            height=48,
            corner_radius=24,
            font=ctk.CTkFont(size=20),
            fg_color="#3a3f4a",
            hover_color="#555b6e"
        )
        restart_icon_btn.grid(row=0, column=1, sticky="e", padx=(10, 0))

        current_row += 1
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Convert videos between formats or create high-quality GIFs",
            font=ctk.CTkFont(size=13),
            text_color=("gray60", "gray60")
        )
        subtitle_label.grid(row=current_row, column=0, columnspan=3, pady=(0, 20), sticky="w")
        current_row += 1
        
        # Three cards side by side
        cards_row = current_row
        
        # Set uniform column weights to prevent resizing when content changes
        main_frame.grid_columnconfigure(0, weight=1, uniform="cards")
        main_frame.grid_columnconfigure(1, weight=1, uniform="cards")
        main_frame.grid_columnconfigure(2, weight=1, uniform="cards")
        
        # 1. File Selection Card (Left)
        file_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        file_frame.grid(row=cards_row, column=0, padx=(0, 10), pady=(0, 20), sticky="nsew")
        file_frame.grid_columnconfigure(0, weight=1)
        file_frame.grid_propagate(False)  # Prevent frame from resizing based on content
        file_frame.configure(width=260, height=140)
        
        file_label = ctk.CTkLabel(
            file_frame,
            text="1. Select Videos",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        file_label.grid(row=0, column=0, padx=20, pady=(20, 15), sticky="w")
        
        browse_btn = ctk.CTkButton(
            file_frame,
            text="Browse Files",
            command=self.select_files,
            width=140,
            height=40,
            corner_radius=20,
            font=ctk.CTkFont(size=13),
            fg_color="#2A7AE8",
            hover_color="#1e5fb8"
        )
        browse_btn.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")
        
        self.files_label = ctk.CTkLabel(
            file_frame,
            text="No files selected",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
            wraplength=200
        )
        self.files_label.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")
        
        # 2. Format Selection Card (Middle)
        format_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        format_frame.grid(row=cards_row, column=1, padx=5, pady=(0, 20), sticky="nsew")
        format_frame.grid_columnconfigure(0, weight=1)
        format_frame.grid_propagate(False)  # Prevent frame from resizing based on content
        format_frame.configure(width=260, height=140)
        
        format_label = ctk.CTkLabel(
            format_frame,
            text="2. Choose Format",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        format_label.grid(row=0, column=0, padx=20, pady=(20, 15), sticky="w")
        
        self.format_var = ctk.StringVar(value='MP4')
        format_dropdown = ctk.CTkComboBox(
            format_frame,
            values=self.VIDEO_FORMATS,
            variable=self.format_var,
            width=180,
            height=40,
            corner_radius=20,
            font=ctk.CTkFont(size=13),
            state="readonly",
            button_color="#2A7AE8",
            button_hover_color="#1e5fb8",
            border_color="#2A7AE8"
        )
        format_dropdown.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        
        # Bind format change to show/hide GIF settings
        format_dropdown.configure(command=self.on_format_change)
        
        # 3. Output Folder Card (Right)
        output_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        output_frame.grid(row=cards_row, column=2, padx=(10, 0), pady=(0, 20), sticky="nsew")
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_propagate(False)  # Prevent frame from resizing based on content
        output_frame.configure(width=260, height=140)
        
        output_label = ctk.CTkLabel(
            output_frame,
            text="3. Output Folder",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        output_label.grid(row=0, column=0, padx=20, pady=(20, 15), sticky="w")
        
        folder_btn = ctk.CTkButton(
            output_frame,
            text="Browse Folder",
            command=self.select_output_folder,
            width=140,
            height=40,
            corner_radius=20,
            font=ctk.CTkFont(size=13),
            fg_color="#2A7AE8",
            hover_color="#1e5fb8"
        )
        folder_btn.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")
        
        # Output folder status with indicator
        output_status_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_status_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")
        
        self.output_status_indicator = ctk.CTkLabel(
            output_status_frame,
            text="○",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray60")
        )
        self.output_status_indicator.grid(row=0, column=0, padx=(0, 5), sticky="w")
        
        self.output_label = ctk.CTkLabel(
            output_status_frame,
            text="Same as source of video(s)",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray60"),
            wraplength=180
        )
        self.output_label.grid(row=0, column=1, sticky="w")
        
        current_row += 1  # Move past cards row
        
        # GIF Quality Settings (show when GIF is selected, below the cards)
        self.gif_settings_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        
        gif_settings_label = ctk.CTkLabel(
            self.gif_settings_frame,
            text="GIF Quality Settings",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        gif_settings_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 10), sticky="w")
        
        # FPS slider
        fps_frame = ctk.CTkFrame(self.gif_settings_frame, fg_color="transparent")
        fps_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        fps_label = ctk.CTkLabel(
            fps_frame,
            text="Frame Rate (FPS):",
            font=ctk.CTkFont(size=12)
        )
        fps_label.pack(side="left", padx=(0, 15))
        
        self.fps_var = ctk.IntVar(value=15)
        self.fps_value_label = ctk.CTkLabel(
            fps_frame,
            text="15",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=30
        )
        self.fps_value_label.pack(side="right", padx=(10, 0))
        
        fps_slider = ctk.CTkSlider(
            fps_frame,
            from_=10,
            to=30,
            number_of_steps=20,
            variable=self.fps_var,
            command=self.update_fps_label,
            width=200
        )
        fps_slider.pack(side="left", padx=(0, 10))
        
        # Scale slider
        scale_frame = ctk.CTkFrame(self.gif_settings_frame, fg_color="transparent")
        scale_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        scale_label = ctk.CTkLabel(
            scale_frame,
            text="Resolution:",
            font=ctk.CTkFont(size=12)
        )
        scale_label.pack(side="left", padx=(0, 15))
        
        self.scale_var = ctk.DoubleVar(value=1.0)
        self.scale_value_label = ctk.CTkLabel(
            scale_frame,
            text="100%",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=50
        )
        self.scale_value_label.pack(side="right", padx=(10, 0))
        
        scale_slider = ctk.CTkSlider(
            scale_frame,
            from_=0.5,
            to=1.0,
            number_of_steps=10,
            variable=self.scale_var,
            command=self.update_scale_label,
            width=200
        )
        scale_slider.pack(side="left", padx=(0, 10))
        
        # Quality info
        quality_info = ctk.CTkLabel(
            self.gif_settings_frame,
            text="💡 Higher FPS and resolution = better quality but larger file size",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray60")
        )
        quality_info.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="w")
        
        # Max width slider (GIF-only)
        max_width_frame = ctk.CTkFrame(self.gif_settings_frame, fg_color="transparent")
        max_width_frame.grid(row=4, column=0, padx=20, pady=(0, 15), sticky="ew")
        max_width_frame.grid_columnconfigure(1, weight=1)

        max_width_label = ctk.CTkLabel(
            max_width_frame,
            text="Max Width:",
            font=ctk.CTkFont(size=12)
        )
        max_width_label.grid(row=0, column=0, sticky="w")

        self.max_width_var = ctk.IntVar(value=700)
        self.max_width_value_label = ctk.CTkLabel(
            max_width_frame,
            text=f"{self.max_width_var.get()} px",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=50
        )
        self.max_width_value_label.grid(row=0, column=2, sticky="e")

        max_width_controls_frame = ctk.CTkFrame(max_width_frame, fg_color="transparent")
        max_width_controls_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        max_width_controls_frame.grid_columnconfigure(0, weight=1)

        max_width_slider = ctk.CTkSlider(
            max_width_controls_frame,
            from_=400,
            to=1400,
            number_of_steps=20,
            variable=self.max_width_var,
            command=self.update_max_width_label,
            width=200
        )
        max_width_slider.grid(row=0, column=0, sticky="w")

        self.full_width_var = ctk.BooleanVar(value=False)
        full_width_checkbox = ctk.CTkCheckBox(
            max_width_controls_frame,
            text="Convert at full width",
            variable=self.full_width_var,
            command=self.update_full_width_state,
            onvalue=True,
            offvalue=False
        )
        full_width_checkbox.grid(row=0, column=1, padx=(10, 0), sticky="e")

        self.max_width_slider = max_width_slider
        self.update_full_width_state()
        # Store row numbers for dynamic placement
        self.gif_settings_row = current_row
        self.status_label_row = current_row + 1  # "Converting X of Y" above button
        self.convert_button_row = current_row + 2
        self.progress_row = current_row + 3
        self.status_row = current_row + 4
        
        # Status label for "Converting X of Y..." - ABOVE the button
        self.progress_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=("gray60", "gray60")
        )
        self.progress_label.grid(row=self.status_label_row, column=0, columnspan=3, pady=(5, 5))
        
        # Convert Button - Large and prominent (below the status label)
        # Using bg_color="transparent" to remove the rectangular background
        self.convert_btn = ctk.CTkButton(
            main_frame,
            text="Convert Video(s)",
            command=self.start_conversion,
            width=240,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2A7AE8",
            hover_color="#1e5fb8",
            bg_color="transparent"
        )
        self.convert_btn.grid(row=self.convert_button_row, column=0, columnspan=3, pady=(5, 15))
        
        # Store original button text for animation
        self.original_btn_text = "Convert Video(s)"
        self.animation_running = False
        self.animation_frame = 0
        
        # Progress Bar (below convert button) - hidden when not in use
        self.progress_bar = ctk.CTkProgressBar(
            main_frame, 
            width=400, 
            height=18,
            progress_color="#2A7AE8",
            fg_color=("gray70", "gray30"),
            border_width=0,
            corner_radius=9
        )
        self.progress_bar.grid(row=self.progress_row, column=0, columnspan=3, pady=(0, 15))
        self.progress_bar.set(0)
        # Hide progress bar initially
        self.progress_bar.grid_remove()
        
        # Status Section (below progress bar)
        self.status_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        self.status_frame.grid(row=self.status_row, column=0, columnspan=3, sticky="nsew", pady=(0, 0))
        self.status_frame.grid_columnconfigure(0, weight=1)
        self.status_frame.grid_rowconfigure(1, weight=1)
        
        status_label = ctk.CTkLabel(
            self.status_frame,
            text="Conversion Status",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        status_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Status text area with CustomTkinter
        self.status_text = ctk.CTkTextbox(
            self.status_frame,
            height=200,
            corner_radius=10,
            font=ctk.CTkFont(family="SF Mono" if sys.platform == 'darwin' else "Consolas", size=12),
            wrap="word",
            activate_scrollbars=True
        )
        self.status_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
    
    def update_fps_label(self, value):
        """Update FPS label when slider changes"""
        self.fps_value_label.configure(text=str(int(float(value))))
    
    def update_scale_label(self, value):
        """Update scale label when slider changes"""
        percent = int(float(value) * 100)
        self.scale_value_label.configure(text=f"{percent}%")

    def update_max_width_label(self, value):
        """Update max width label for GIF resizing"""
        self.max_width_value_label.configure(text=f"{int(float(value))} px")

    def update_full_width_state(self, *_):
        """Enable/disable max width slider based on full-width option"""
        state = "disabled" if self.full_width_var.get() else "normal"
        self.max_width_slider.configure(state=state)
    
    def on_format_change(self, choice):
        """Show/hide GIF settings based on format selection"""
        if choice == 'GIF':
            # Place GIF settings below the three cards, spanning all columns
            self.gif_settings_frame.grid(row=self.gif_settings_row, column=0, columnspan=3, pady=(0, 10), sticky="ew")
        else:
            self.gif_settings_frame.grid_remove()
    
    def select_files(self):
        """Open file dialog to select videos"""
        filetypes = (
            ('All supported videos', '*.mp4 *.mov *.mkv *.webm *.avi *.MP4 *.MOV *.MKV *.WEBM *.AVI'),
            ('MP4 files', '*.mp4 *.MP4'),
            ('MOV files', '*.mov *.MOV'),
            ('MKV files', '*.mkv *.MKV'),
            ('WEBM files', '*.webm *.WEBM'),
            ('AVI files', '*.avi *.AVI'),
            ('All files', '*.*')
        )
        
        files = filedialog.askopenfilenames(
            title='Select videos to convert',
            filetypes=filetypes,
            initialdir=self.last_input_dir
        )
        
        if files:
            self.selected_files = list(files)
            # Update last used directory
            if self.selected_files:
                self.last_input_dir = os.path.dirname(self.selected_files[0])
            
            count = len(self.selected_files)
            self.files_label.configure(
                text=f"✓ {count} file{'s' if count > 1 else ''} selected",
                text_color=("#2ecc71", "#2ecc71")
            )
            
            # Update output folder indicator to green (source is now known)
            # Only update if no custom output folder has been selected
            if not self.output_folder:
                self.output_status_indicator.configure(text="✓", text_color="#2ecc71")
                self.output_label.configure(text_color="#2ecc71")
            
            self.log_status(f"Selected {count} file(s) for conversion")
    
    def get_display_path(self, full_path):
        """Convert full path to display-friendly format"""
        if not full_path:
            return ""
        
        path_obj = Path(full_path)
        
        # Get user's home directory
        home_dir = Path.home()
        
        try:
            # If path is in user's home directory, show relative to common folders
            if path_obj.is_relative_to(home_dir):
                rel_to_home = path_obj.relative_to(home_dir)
                parts = rel_to_home.parts
                
                # If it's directly in a common folder like Desktop, Documents, etc.
                if len(parts) > 0 and parts[0] in ['Desktop', 'Documents', 'Downloads', 'Pictures', 'Videos']:
                    return f".../{parts[0]}"
                
        except (ValueError, AttributeError):
            pass
        
        # Otherwise show just the folder name with ellipsis
        folder_name = path_obj.name
        return f".../{folder_name}"
    
    def select_output_folder(self):
        """Open folder dialog to select output directory"""
        folder = filedialog.askdirectory(
            title='Select output folder',
            initialdir=self.last_output_dir
        )
        
        if folder:
            self.output_folder = folder
            self.last_output_dir = folder  # Update last used directory
            
            # Get privacy-friendly display path
            display_path = self.get_display_path(folder)
            
            # Update indicator to checkmark and make text green
            self.output_status_indicator.configure(text="✓", text_color="#2ecc71")
            self.output_label.configure(
                text=display_path,
                text_color="#2ecc71"
            )
            self.log_status(f"Output folder: {folder}")

    def reset_form(self):
        """Reset the UI form to its default state"""
        if self.animation_running or self.simulated_progress_running:
            messagebox.showwarning(
                "Conversion running",
                "Please wait for the current conversion to finish before resetting."
            )
            return

        self.selected_files = []
        self.files_label.configure(
            text="No files selected",
            text_color=("gray50", "gray50")
        )
        self.output_folder = None
        self.output_status_indicator.configure(
            text="○",
            text_color=("gray60", "gray60")
        )
        self.output_label.configure(
            text="Same as source of video(s)",
            text_color=("gray60", "gray60")
        )
        self.format_var.set('MP4')
        self.on_format_change('MP4')
        self.fps_var.set(15)
        self.update_fps_label(15)
        self.scale_var.set(1.0)
        self.update_scale_label(1.0)
        self.max_width_var.set(700)
        self.update_max_width_label(700)
        self.full_width_var.set(False)
        self.update_full_width_state()

        self.progress_label.configure(text="")
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()

        self.status_text.delete("0.0", "end")
        self.used_messages = []
        self.simulated_progress_running = False
        self.stop_funny_messages()
        self.stop_button_animation()
        self.convert_btn.configure(state="normal")
        self.log_status("Form reset to defaults.")
    
    def log_status(self, message):
        """Add a message to the status text area"""
        self.status_text.insert("end", message + '\n')
        self.status_text.see("end")
        self.root.update_idletasks()
    
    def start_button_animation(self):
        """Start the spinning animation on the convert button"""
        self.animation_running = True
        self.animation_frame = 0
        self.animate_button()
    
    def stop_button_animation(self):
        """Stop the spinning animation and restore button text"""
        self.animation_running = False
        self.convert_btn.configure(text=self.original_btn_text)
    
    def animate_button(self):
        """Animate the button with a spinning indicator"""
        if not self.animation_running:
            return
        
        # Spinning characters
        spinners = ["◐", "◓", "◑", "◒"]
        spinner = spinners[self.animation_frame % len(spinners)]
        self.convert_btn.configure(text=f"{spinner}  Converting...  {spinner}")
        
        self.animation_frame += 1
        # Schedule next frame (100ms = 10fps animation)
        self.root.after(100, self.animate_button)
    
    def start_conversion(self):
        """Start the conversion process in a separate thread"""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select at least one video file to convert.")
            return
        
        # Disable convert button during conversion and start animation
        self.convert_btn.configure(state="disabled")
        self.start_button_animation()
        
        # Clear previous status
        self.status_text.delete("0.0", "end")
        
        # Run conversion in separate thread to keep UI responsive
        thread = threading.Thread(target=self.convert_videos, daemon=True)
        thread.start()
    
    def convert_videos(self):
        """Convert all selected videos to the target format"""
        target_format = self.format_var.get()
        success_count = 0
        total = len(self.selected_files)
        
        # Reset and activate progress bar
        self.progress_bar.set(0)
        self.simulated_progress = 0.0
        # Show the progress bar
        self.progress_bar.grid()
        self.progress_bar.configure(progress_color="#2A7AE8")
        
        # Reset funny messages
        self.used_messages = []
        
        # Start funny messages once at the beginning (not per file)
        self.start_funny_messages()
        
        self.log_status(f"Starting conversion to {target_format}...\n")
        self.log_status("=" * 60)
        
        for index, file_path in enumerate(self.selected_files, 1):
            try:
                # Calculate progress range for this file
                self.current_file_start_progress = (index - 1) / total
                self.current_file_end_progress = index / total
                self.simulated_progress = self.current_file_start_progress
                
                self.progress_label.configure(text=f"Converting {index} of {total}...")
                self.root.update_idletasks()
                
                # Start simulated progress animation
                self.start_simulated_progress()
                
                result = self.convert_single_video(file_path, target_format)
                
                # Stop simulated progress
                self.stop_simulated_progress()
                
                if result:
                    self.log_status(f"✓ {Path(file_path).name} → {Path(result).name}")
                    success_count += 1
                    # Snap to actual completion for this file
                    self.progress_bar.set(self.current_file_end_progress)
                    self.root.update_idletasks()
            except Exception as e:
                self.stop_simulated_progress()
                self.log_status(f"✗ {Path(file_path).name}: {str(e)}")
                # Still advance progress even on failure
                self.progress_bar.set(index / total)
                self.root.update_idletasks()
        
        # Stop funny messages at the end
        self.stop_funny_messages()
        
        # Complete progress bar
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="✓ Complete!")
        
        # Stop button animation and re-enable
        self.stop_button_animation()
        self.convert_btn.configure(state="normal")
        
        # Summary
        self.log_status("=" * 60)
        self.log_status(f"🎉 Conversion complete: {success_count}/{total} successful")
        
        if success_count > 0:
            messagebox.showinfo("Success", 
                              f"Successfully converted {success_count}/{total} video(s)!")
        
        # Reset progress after a delay
        def reset_progress():
            self.progress_label.configure(text="")
            self.progress_bar.set(0)
            # Hide progress bar when not in use
            self.progress_bar.grid_remove()
        
        self.root.after(3000, reset_progress)
    
    def start_simulated_progress(self):
        """Start the simulated progress animation"""
        self.simulated_progress_running = True
        self.animate_simulated_progress()
    
    def stop_simulated_progress(self):
        """Stop the simulated progress animation"""
        self.simulated_progress_running = False
    
    def animate_simulated_progress(self):
        """Gradually fill progress bar to simulate conversion progress"""
        if not self.simulated_progress_running:
            return
        
        # Calculate how much of this file's range we can fill (stop at 90% to leave room for completion)
        max_progress = self.current_file_start_progress + (self.current_file_end_progress - self.current_file_start_progress) * 0.9
        
        if self.simulated_progress < max_progress:
            # Increment progress slowly (smaller increments = smoother animation)
            increment = (self.current_file_end_progress - self.current_file_start_progress) * 0.02
            self.simulated_progress = min(self.simulated_progress + increment, max_progress)
            self.progress_bar.set(self.simulated_progress)
            self.root.update_idletasks()
        
        # Schedule next frame (150ms intervals)
        if self.simulated_progress_running:
            self.root.after(150, self.animate_simulated_progress)
    
    def start_funny_messages(self):
        """Start displaying funny status messages"""
        self.funny_message_running = True
        self.show_funny_message()
    
    def stop_funny_messages(self):
        """Stop displaying funny status messages"""
        self.funny_message_running = False
    
    def get_random_message(self):
        """Get a random message that hasn't been used recently"""
        available = [m for m in self.THINKING_MESSAGES if m not in self.used_messages]
        if not available:
            # Reset if we've used all messages
            self.used_messages = []
            available = self.THINKING_MESSAGES.copy()
        
        message = random.choice(available)
        self.used_messages.append(message)
        # Keep only last 10 used messages to allow reuse eventually
        if len(self.used_messages) > 10:
            self.used_messages.pop(0)
        return message
    
    def show_funny_message(self):
        """Display a funny message in the status area"""
        if not self.funny_message_running:
            return
        
        message = self.get_random_message()
        self.log_status(f"  {message}")
        
        # Show a new message every 8-10 seconds (randomized for natural feel)
        delay = random.randint(8000, 10000)
        if self.funny_message_running:
            self.root.after(delay, self.show_funny_message)
    
    @staticmethod
    def _normalize_dimension(value):
        """Round to the nearest even integer and enforce a minimum size"""
        even = int(round(value))
        if even % 2 != 0:
            even -= 1
        return max(2, even)
    
    def convert_single_video(self, input_path, target_format):
        """Convert a single video file"""
        input_path = Path(input_path)
        
        # Determine output path
        if self.output_folder:
            output_dir = Path(self.output_folder)
        else:
            output_dir = input_path.parent
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create output filename
        output_name = input_path.stem + '.' + target_format.lower()
        output_path = output_dir / output_name
        
        self.log_status(f"Converting {input_path.name}...")
        
        clip = None
        try:
            clip = VideoFileClip(str(input_path))
            
            if target_format == 'GIF':
                # High-quality GIF conversion
                fps = self.fps_var.get()
                scale = self.scale_var.get()
                
                # Resize if needed, ensuring ffmpeg-friendly even dims
                if scale < 1.0:
                    target_width = self._normalize_dimension(clip.w * scale)
                    target_height = self._normalize_dimension(clip.h * scale)
                    clip = clip.resize(newsize=(target_width, target_height))
                
                if not self.full_width_var.get():
                    max_width = self.max_width_var.get()
                    if clip.w > max_width:
                        ratio = max_width / clip.w
                        max_width_even = self._normalize_dimension(max_width)
                        target_height = self._normalize_dimension(clip.h * ratio)
                        clip = clip.resize(newsize=(max_width_even, target_height))
                
                clip.write_gif(
                    str(output_path),
                    fps=fps,
                    program='ffmpeg',
                    opt='OptimizePlus',
                    fuzz=1
                )
            else:
                # Convert to video format
                codec_map = {
                    'MP4': 'libx264',
                    'MOV': 'libx264',
                    'MKV': 'libx264',
                    'WEBM': 'libvpx',
                    'AVI': 'mpeg4'
                }
                
                codec = codec_map.get(target_format, 'libx264')
                
                clip.write_videofile(
                    str(output_path),
                    codec=codec,
                    audio_codec='aac' if target_format in ['MP4', 'MOV', 'MKV'] else 'libvorbis',
                    logger=None  # Suppress moviepy progress bar
                )
        finally:
            if clip:
                clip.close()
        
        return str(output_path)

def main():
    """Main entry point for the application"""
    root = ctk.CTk()
    app = VideoConverterApp(root)
    
    # Bring window to front and focus it (especially important on macOS)
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.focus_force()
    
    root.mainloop()

if __name__ == "__main__":
    main()