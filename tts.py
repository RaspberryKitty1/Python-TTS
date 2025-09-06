import pyttsx3
import re
import argparse
import pyperclip
import time
import threading
import sys
from langdetect import detect, DetectorFactory
from tqdm import tqdm

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

try:
    import keyboard  # pip install keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

DetectorFactory.seed = 0


class TTSReader:
    def __init__(self, rate=150, voice=None):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.voices = self.engine.getProperty("voices")
        self.selected_voice_id = None
        self.rate = rate

        if voice is not None and voice < len(self.voices):
            self.selected_voice_id = self.voices[voice].id
            print(f"[Voice Set by --voice Index: {voice}]")

        self.pause_flag = threading.Event()
        self.stop_flag = threading.Event()
        self.pause_flag.set()  # Start unpaused

    @staticmethod
    def clean_text(text):
        text = re.sub(r"<.*?>", "", text)
        text = re.sub(r"https?://\S+|www\.\S+", "", text)
        return text.strip()

    @staticmethod
    def split_into_sentences(text):
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    def detect_language(self, text):
        try:
            lang = detect(text)
            print(f"[Language Detected]: {lang}")
            return lang
        except Exception as e:
            print(f"[Language Detection Error]: {e}")
            return None

    def find_voice_for_language(self, lang_code):
        lang_code = lang_code.lower()
        for v in self.voices:
            langs = getattr(v, "languages", [])
            for tag in langs:
                if isinstance(tag, bytes):
                    tag = tag.decode("utf-8")
                if lang_code in tag.lower():
                    return v.id
            if lang_code in v.name.lower() or lang_code in v.id.lower():
                return v.id
        return None

    def select_voice(self, text):
        if not self.selected_voice_id:
            lang = self.detect_language(text)
            matched = self.find_voice_for_language(lang) if lang else None
            self.selected_voice_id = matched or self.voices[0].id
            print(f"[Voice Selected]: {self.selected_voice_id}")

        self.engine.setProperty("voice", self.selected_voice_id)

    def speak(self, text, show_progress=False, highlight=False):
        text = self.clean_text(text)
        self.select_voice(text)
        sentences = self.split_into_sentences(text)

        progress = tqdm(total=len(sentences), unit="sentence", disable=not show_progress)

        for sentence in sentences:
            if self.stop_flag.is_set():
                break
            self.pause_flag.wait()

            # Show highlighted sentence above progress bar
            if highlight:
                tqdm.write(f"> {sentence}")

            self.engine.say(sentence)
            self.engine.runAndWait()

            if show_progress:
                progress.update(1)

            time.sleep(0.05)

        progress.close()
        self.engine.stop()

    def save_to_file(self, text, path="output.wav", split=False, mp3=False):
        text = self.clean_text(text)
        self.select_voice(text)

        if split:
            sentences = self.split_into_sentences(text)
            for i, sentence in enumerate(sentences, 1):
                filename = f"{path.rsplit('.',1)[0]}_{i}.wav"
                print(f"Saving: {filename}")
                self.engine.save_to_file(sentence, filename)
                self.engine.runAndWait()
                if mp3 and AudioSegment:
                    sound = AudioSegment.from_wav(filename)
                    mp3_name = filename.replace(".wav", ".mp3")
                    sound.export(mp3_name, format="mp3")
        else:
            print(f"Saving to {path}...")
            self.engine.save_to_file(text, path)
            self.engine.runAndWait()
            if mp3 and AudioSegment:
                sound = AudioSegment.from_wav(path)
                mp3_name = path.replace(".wav", ".mp3")
                sound.export(mp3_name, format="mp3")
                print(f"[Converted to MP3: {mp3_name}]")

        print("[Done]")

    def setup_hotkeys(self):
        if not KEYBOARD_AVAILABLE:
            print("[Hotkeys Disabled: install `keyboard` library for hotkey support]")
            return

        def toggle_pause():
            if self.pause_flag.is_set():
                self.pause_flag.clear()
                print("\n[Paused]")
            else:
                self.pause_flag.set()
                print("\n[Resumed]")

        def stop():
            self.stop_flag.set()
            self.pause_flag.set()
            print("\n[Stopped by hotkey]")

        keyboard.add_hotkey("space", toggle_pause)
        keyboard.add_hotkey("esc", stop)


def get_text_from_args(args):
    if args.text:
        return args.text
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read()
    elif args.clipboard:
        return pyperclip.paste()
    else:
        print("Enter text (Ctrl+D to finish):")
        return "\n".join(iter(input, ""))

def main():
    parser = argparse.ArgumentParser(description="Ultimate TTS Reader")
    parser.add_argument("--text", help="Text to read")
    parser.add_argument("--file", help="Read text from file")
    parser.add_argument("--clipboard", action="store_true", help="Read text from clipboard")
    parser.add_argument("--list-voices", action="store_true", help="List available voices and exit")
    parser.add_argument("--word-indicator", action="store_true", help="Show sentence progress")
    parser.add_argument("--highlight", action="store_true", help="Highlight current sentence")
    parser.add_argument("--rate", type=int, default=150, help="Speech rate")
    parser.add_argument("--voice", type=int, choices=range(0, 50), help="Choose voice index")
    parser.add_argument("--output", help="Save audio to file (WAV)")
    parser.add_argument("--split-sentences", action="store_true", help="Save each sentence separately")
    parser.add_argument("--mp3", action="store_true", help="Convert output to MP3 (requires pydub)")

    args = parser.parse_args()
    reader = TTSReader(rate=args.rate, voice=args.voice)

    if args.list_voices:
        for i, v in enumerate(reader.voices):
            langs = [l.decode("utf-8") if isinstance(l, bytes) else l for l in getattr(v, "languages", [])]
            print(f"[{i}] {v.name} - {langs or 'Unknown'}")
        return

    text = get_text_from_args(args)

    if args.output:
        reader.save_to_file(text, args.output, split=args.split_sentences, mp3=args.mp3)
    else:
        print("\nControls: [Space] Pause/Resume, [Esc] Quit\n")
        reader.setup_hotkeys()
        reader.speak(text, show_progress=args.word_indicator, highlight=args.highlight)


if __name__ == "__main__":
    main()
