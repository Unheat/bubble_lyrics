from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QEasingCurve
from PyQt5.QtGui import QFont, QFontDatabase
import os
import sys
import platform
from get_current_song import get_current_song
from fetch_song import fetch_lyrics
try:
    from AppKit import NSApplication
    from Quartz import CGWindowLevelForKey, kCGOverlayWindowLevelKey
    import objc
except ImportError:
    NSApplication = None

class LyricsOverlay(QWidget):
    def __init__(self):
        super().__init__()
        # Variables for tracking song and lyrics
        self.current_song_title = None
        self.current_lyrics = []
        self.current_lyric_index = 0  # Track the index of the current lyric

        # Configure the PyQt window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(200, 200, 600, 180)

        # Load a custom font
        font_family = self.load_custom_font("font/CircularSpotifyText-Black.otf")

        # Create QLabel widgets for recent, current, and next lines
        self.recent_label = QLabel("")
        self.current_label = QLabel("")
        self.next_label = QLabel("")

        # Apply distinct styles
        self.recent_label.setStyleSheet("color: white; background: transparent; border: none;")
        self.next_label.setStyleSheet("color: white; background: transparent; border: none;")
        self.current_label.setStyleSheet("color: green; background: transparent; border: none;")  # Highlight the current line

        # Set fonts and alignment
        for label in (self.recent_label, self.current_label, self.next_label):
            label.setFont(QFont(font_family, 22))
            label.setAlignment(Qt.AlignCenter)
        if platform.system() == "Darwin":
            self.ensure_mac_panel_behavior()
      
        # Add the labels to the layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove additional margins
        self.layout.addWidget(self.recent_label)
        self.layout.addWidget(self.current_label)
        self.layout.addWidget(self.next_label)

        # Timer to periodically update lyrics
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_lyrics)
        self.timer.start(2000)  # Update every half second
    def ensure_mac_panel_behavior(self):
        """
        Configure the window as an NSPanel to ensure:
        - Always-on-top behavior.
        - No interference with other applications.
        """
        if NSApplication:
            app = NSApplication.sharedApplication()
            window_id = self.winId().__int__()
            ns_view = objc.objc_object(c_void_p=window_id)

            # Retrieve the NSWindow from the QNSView
            ns_window = ns_view.window()

            if ns_window:
                ns_panel = objc.objc_object(c_void_p=window_id).window()
                ns_panel.setStyleMask_(ns_panel.styleMask() | 0x80)  # NSPanel style
                ns_panel.setLevel_(CGWindowLevelForKey(kCGOverlayWindowLevelKey))

                NSWindowCollectionBehaviorCanJoinAllSpaces = 1 << 0
                NSWindowCollectionBehaviorFullScreenAuxiliary = 1 << 4
                ns_panel.setCollectionBehavior_(
                    NSWindowCollectionBehaviorCanJoinAllSpaces | NSWindowCollectionBehaviorFullScreenAuxiliary
                )
                ns_panel.setHidesOnDeactivate_(False)
                ns_panel.setWorksWhenModal_(True)

                app.activateIgnoringOtherApps_(False)
            else:
                print("Failed to retrieve NSWindow.")
        else:
            print("PyObjC is not installed. macOS-specific behavior might not work.")   
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            
            
    def update_lyrics(self):
        """
        Update the displayed lyrics based on the currently playing song and its progress.
        Handles song changes, skips, and updates lyrics dynamically.
        """
        current_song = get_current_song()

        if not current_song:
            self.current_label.setText("No song is currently playing.")
            return

        # Extract song details
        title = current_song['title']
        artist = current_song['artist']
        progress_ms = current_song['progress_ms']

        # Check if the song has changed or lyrics are not loaded
        if self.current_song_title != title:
            self.current_song_title = title
            self.current_lyrics = fetch_lyrics(title, artist)
            self.current_lyric_index = 0  # Reset the lyric index for the new song

            if not self.current_lyrics:
                self.current_label.setText(f"Lyrics not found for '{title}' by {artist}.")
                return

        # Handle song skip by resetting the lyric index based on current progress
        self.current_lyric_index = self.find_current_lyric_index(progress_ms)

        # Get the three lines to display
        recent = self.get_lyric_line(self.current_lyric_index - 1)
        current = self.get_lyric_line(self.current_lyric_index)
        next_lyric = self.get_lyric_line(self.current_lyric_index + 1)

        # Update only if there's a change
        if self.current_label.text() != current:
            self.animate_lyrics(recent, current, next_lyric)

    def find_current_lyric_index(self, progress_ms):
        """
        Find the correct lyric index based on the song's current progress.
        Handles cases where the user skips through the song.
        """
        for i, lyric in enumerate(self.current_lyrics):
            if progress_ms < lyric["time"]:
                return max(0, i - 1)
        return len(self.current_lyrics) - 1

    def animate_lyrics(self, recent, current, next_lyric):
        """
        Animate the lyrics with gradual scrolling and fading effects.
        """
        # Update the text before animating
        self.recent_label.setText(recent)
        self.current_label.setText(current)
        self.next_label.setText(next_lyric)

        # Set initial positions
        self.recent_label.move(0, 0)
        self.current_label.move(0, 60)
        self.next_label.move(0, 120)

        # Animate positions for smooth scrolling
        animations = []
        for label, start_y, end_y in zip(
            [self.recent_label, self.current_label, self.next_label],
            [0, 60, 120],  # Start Y positions
            [-60, 0, 60],  # End Y positions
        ):
            animation = QPropertyAnimation(label, b"pos", self)
            animation.setDuration(500)  # Half a second
            animation.setStartValue(QPoint(0, start_y))
            animation.setEndValue(QPoint(0, end_y))
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.start()
            animations.append(animation)  # Keep a reference to avoid garbage collection

    def get_lyric_line(self, index):
        """
        Get the lyric line at the given index, or an empty string if out of bounds.
        """
        if 0 <= index < len(self.current_lyrics):
            return self.current_lyrics[index]["text"]
        return ""

    def load_custom_font(self, relative_path):
        """
        Load a custom font from a relative path and return its family name.
        """
        font_path = self.resource_path(relative_path)
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Failed to load font from: {font_path}")
            return None
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        print(f"Successfully loaded font: {font_family}")
        return font_family

    @staticmethod
    def resource_path(relative_path):
        """
        Get the absolute path to a resource, works for development and PyInstaller builds.
        """
        if getattr(sys, 'frozen', False):  # If the app is bundled with PyInstaller
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = QApplication([])
    overlay = LyricsOverlay()
    overlay.show()
    app.exec_()
