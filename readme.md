# Lyrics Overlay

A desktop application that displays synchronized lyrics for your currently playing songs in real-time. Perfect for karaoke-style singing or simply enjoying your music with synchronized lyrics display.

## Features

- Multi-line lyrics display:
  - Previous line
  - Current line (highlighted in green)
  - Next line
- Real-time synchronization with currently playing music
- Smooth scrolling and fading animations
- Dynamic updates on song changes or timeline skips
- Genius API integration for lyrics fetching
- Cross-platform support (macOS and Windows)
- Customizable appearance (fonts and colors)

## Prerequisites

### Dependencies

Python 3.8 or higher is required, along with the following libraries:

- PyQt5 (GUI and animations)
- requests (API calls)
- lyricsgenius (Genius API integration)
- certifi (SSL certificate verification)
- PyObjC (macOS-specific features)
- urllib3 (HTTPS requests)

Install all dependencies using pip:

```bash
pip install PyQt5 requests lyricsgenius certifi PyObjC urllib3
```

### API Requirements

The application requires access to:
- Spotify API (or similar) for current song information
- Textyle API for synchronized lyrics

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lyrics-overlay.git
   cd lyrics-overlay
   ```

2. Set up virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


4. Launch the application:
   ```bash
   python main.py
   ```

## Project Structure

```
.
├── main.py                 # Application entry point
├── fetch_song.py           # Genius API lyrics fetcher
├── get_current_song.py     # Current song detection
├── requirements.txt        # Project dependencies
├── README.md              
└── font/
    └── CircularSpotifyText-Black.otf  # Default font
```

## Usage

1. Start your music player (e.g., Spotify)
2. Launch Lyrics Overlay
3. A floating window will appear showing synchronized lyrics

## Customization

### Appearance

#### Font
Replace `font/CircularSpotifyText-Black.otf` with your preferred font file.

#### Colors
Modify the style settings in `main.py`:

```python
self.current_label.setStyleSheet("color: green; background: transparent; border: none;")
self.recent_label.setStyleSheet("color: white; background: transparent; border: none;")
self.next_label.setStyleSheet("color: white; background: transparent; border: none;")
```

### Animation Settings

Adjust timing and easing in `main.py`:

```python
position_animation.setDuration(1000)  # Animation duration (ms)
position_animation.setEasingCurve(QEasingCurve.InOutQuad)  # Easing curve
```

## Troubleshooting

### Common Issues

1. **Lyrics Not Displaying**
   - Verify song title and artist spelling
   - Check if the song exists in Genius database

2. **Song Change Detection Issues**
   - Verify media player API integration in `get_current_song.py`

3. **SSL Warnings**
   ```bash
   pip install certifi
   ```

4. **macOS Specific Issues**
   ```bash
   pip install pyobjc
   ```

## Limitations

- Requires Genius database availability for lyrics
- Limited to media players with API support
- Currently supports Spotify (additional platforms planned)

## Roadmap

- [ ] Apple Music support
- [ ] YouTube Music integration
- [ ] Enhanced animation options
- [ ] Dynamic overlay positioning
- [ ] User-configurable window size

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## License

