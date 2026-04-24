"""
player.py — MusicPlayer
=======================
pygame.mixer не работает на Python 3.14 + pygame 2.6.1.
Вместо него используем sounddevice + soundfile для воспроизведения аудио.
API остаётся тем же, что ожидает main.py.
"""

import threading
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf


class MusicPlayer:
    """Keyboard-controlled music player (sounddevice backend)."""

    def __init__(self, music_dir: Path):
        self.tracks = sorted(
            [p for p in music_dir.rglob("*")
             if p.suffix.lower() in {".wav", ".mp3", ".ogg", ".flac"}]
        )
        if not self.tracks:
            raise FileNotFoundError(f"No audio files found in {music_dir}")

        self.current_index = 0
        self.status = "stopped"          # "stopped" | "playing" | "paused"
        self.current_length = 0.0
        self._pos_seconds = 0.0          # playback position in seconds
        self._stream: sd.OutputStream | None = None
        self._audio_data: np.ndarray | None = None
        self._samplerate: int = 44100
        self._frame_index: int = 0       # current read position in frames
        self._lock = threading.Lock()
        self._on_end_callback = None

        self._load_current()

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _load_current(self):
        """Load audio file into memory."""
        self._stop_stream()
        path = self.current_track
        data, sr = sf.read(str(path), dtype="float32", always_2d=True)
        self._audio_data = data          # shape: (frames, channels)
        self._samplerate = sr
        self.current_length = len(data) / sr
        self._frame_index = 0
        self._pos_seconds = 0.0
        self.status = "stopped"

    def _audio_callback(self, outdata, frames, time_info, status):
        """Called by sounddevice in a background thread to fill audio buffer."""
        with self._lock:
            if self._audio_data is None or self.status != "playing":
                outdata[:] = 0
                return

            remaining = len(self._audio_data) - self._frame_index
            if remaining <= 0:
                outdata[:] = 0
                self.status = "stopped"
                self._frame_index = 0
                self._pos_seconds = 0.0
                if self._on_end_callback:
                    threading.Thread(target=self._on_end_callback, daemon=True).start()
                return

            chunk = min(frames, remaining)
            src = self._audio_data[self._frame_index: self._frame_index + chunk]
            # Match output channel count
            out_ch = outdata.shape[1]
            src_ch = src.shape[1]
            if src_ch < out_ch:
                src = np.tile(src, (1, out_ch // src_ch + 1))[:, :out_ch]
            elif src_ch > out_ch:
                src = src[:, :out_ch]

            outdata[:chunk] = src
            if chunk < frames:
                outdata[chunk:] = 0

            self._frame_index += chunk
            self._pos_seconds = self._frame_index / self._samplerate

    def _start_stream(self):
        if self._stream is not None:
            return
        channels = self._audio_data.shape[1] if self._audio_data is not None else 2
        self._stream = sd.OutputStream(
            samplerate=self._samplerate,
            channels=channels,
            callback=self._audio_callback,
            dtype="float32",
        )
        self._stream.start()

    def _stop_stream(self):
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    # ── Public API (same as original pygame.mixer version) ────────────────────

    def set_endevent_callback(self, callback):
        """Register a callable that fires when the current track ends."""
        self._on_end_callback = callback

    @property
    def current_track(self) -> Path:
        return self.tracks[self.current_index]

    def play(self):
        if self.status == "paused":
            self.status = "playing"
            return
        # Fresh play from current position (or start)
        self.status = "playing"
        self._start_stream()

    def pause(self):
        if self.status == "playing":
            self.status = "paused"

    def stop(self):
        with self._lock:
            self.status = "stopped"
            self._frame_index = 0
            self._pos_seconds = 0.0
        self._stop_stream()

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self._load_current()
        self.play()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self._load_current()
        self.play()

    def position_seconds(self) -> float:
        return self._pos_seconds
