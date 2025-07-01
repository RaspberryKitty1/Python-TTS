import pyttsx3
import re
import argparse
import pyperclip
import time
import sys
import threading
from langdetect import detect, DetectorFactory  # pip install langdetect

DetectorFactory.seed = 0  # Consistent language detection

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    return text.strip()

def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def handle_structured_text(text):
    paragraphs = text.split("\n\n")
    structured_text = []
    for paragraph in paragraphs:
        if paragraph.strip() == "":
            continue
        if re.match(r'^[A-Z0-9\s]+$', paragraph):
            structured_text.append(f"Heading: {paragraph}")
        else:
            structured_text.append(paragraph)
    return structured_text

def detect_language(text):
    try:
        lang = detect(text)
        print(f"[Language Detected]: {lang}")
        return lang
    except Exception as e:
        print(f"[Language Detection Error]: {e}")
        return None

def find_voice_for_language(lang_code, voices):
    lang_code = lang_code.lower()
    for v in voices:
        voice_langs = getattr(v, 'languages', [])
        for tag in voice_langs:
            if isinstance(tag, bytes):
                tag = tag.decode("utf-8")
            if lang_code in tag.lower():
                return v.id
        if lang_code in v.name.lower() or lang_code in v.id.lower():
            return v.id
    return None

def key_listener(pause_flag, stop_flag):
    print("Controls: type 'p' + Enter to pause, 'r' + Enter to resume, 'q' + Enter to quit.")
    while not stop_flag.is_set():
        try:
            key = input().strip().lower()
            if key == 'p':
                if pause_flag.is_set():
                    pause_flag.clear()
                    print("[Paused] Type 'r' to resume or 'q' to quit.")
            elif key == 'r':
                if not pause_flag.is_set():
                    pause_flag.set()
                    print("[Resumed]")
            elif key == 'q':
                print("[Quitting early]")
                stop_flag.set()
                pause_flag.set()
        except EOFError:
            break

def speak_with_progress(text, show_progress=False, rate=150, voice=None):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    voices = engine.getProperty("voices")

    selected_voice_id = None
    if voice is not None and voice < len(voices):
        selected_voice_id = voices[voice].id
        print(f"[Voice Set by --voice Index: {voice}]")
    else:
        detected_lang = detect_language(text)
        matched_voice = find_voice_for_language(detected_lang, voices)
        if matched_voice:
            selected_voice_id = matched_voice
            print(f"[Voice Auto-Selected for Language '{detected_lang}']")
        else:
            selected_voice_id = voices[0].id
            print(f"[No Matching Voice for '{detected_lang}'; using default voice]")

    engine.setProperty("voice", selected_voice_id)

    structured_text = handle_structured_text(text)
    total_words = len(text.split())
    spoken_words = 0

    pause_flag = threading.Event()
    pause_flag.set()
    stop_flag = threading.Event()

    key_thread = threading.Thread(target=key_listener, args=(pause_flag, stop_flag), daemon=True)
    key_thread.start()

    try:
        for section in structured_text:
            if stop_flag.is_set():
                break
            if "Heading:" in section:
                time.sleep(0.5)
                if show_progress:
                    print(f"\n{section.replace('Heading:', '').strip()}\n")
            else:
                sentences = split_into_sentences(section)
                for sentence in sentences:
                    if stop_flag.is_set():
                        break
                    pause_flag.wait()
                    if stop_flag.is_set():
                        break

                    word_count = len(sentence.split())
                    spoken_words += word_count
                    if show_progress:
                        print(f"{spoken_words}/{total_words} words: {sentence}\n")

                    engine.say(sentence)
                    engine.runAndWait()
                    time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[Interrupted by user]")
    finally:
        stop_flag.set()
        engine.stop()

def get_text_from_args(args):
    if args.text:
        return args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Failed to read file: {e}")
            exit(1)
    elif args.clipboard:
        return pyperclip.paste()
    else:
        print("Enter/Paste your text below. Finish input with Ctrl+D (Unix) or Ctrl+Z then Enter (Windows):")
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="TTS Reader with Language Detection, Auto Voice, Pause/Resume, and Word Progress")
    parser.add_argument("--text", help="Text to read")
    parser.add_argument("--file", help="Path to text file")
    parser.add_argument("--clipboard", action="store_true", help="Read text from clipboard")
    parser.add_argument("--word-indicator", action="store_true", help="Show word count progress per sentence")
    parser.add_argument("--rate", type=int, default=150, help="Set the speech rate (default: 150)")
    parser.add_argument("--voice", type=int, choices=range(0, 10), default=None, help="Choose voice by index")

    args = parser.parse_args()
    raw_text = get_text_from_args(args)
    cleaned = clean_text(raw_text)

    print("\nStarting speech...\n(Type 'p' + Enter to pause, 'r' + Enter to resume, 'q' + Enter to quit)\n")
    speak_with_progress(cleaned, show_progress=args.word_indicator, rate=args.rate, voice=args.voice)

if __name__ == "__main__":
    main()
