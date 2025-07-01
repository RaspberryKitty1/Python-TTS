import pyttsx3
import re
import argparse
import pyperclip
import time
import sys
import threading
from langdetect import detect, LangDetectException

# Global control flags
pause_flag = threading.Event()
pause_flag.set()  # Not paused initially
stop_flag = threading.Event()

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)  # Remove HTML-style tags
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Remove URLs
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
        return detect(text)
    except LangDetectException:
        return None

def select_voice_by_language(engine, lang_code):
    voices = engine.getProperty("voices")
    lang_code = lang_code.lower()
    for i, voice in enumerate(voices):
        langs = []
        for l in getattr(voice, 'languages', []):
            if isinstance(l, bytes):
                try:
                    langs.append(l.decode('utf-8').lower())
                except:
                    pass
            else:
                langs.append(l.lower())
        if any(lang_code in l for l in langs):
            return i
    return 0  # fallback to default

def speak_with_progress(text, show_progress=False, rate=150, voice=None):
    global pause_flag, stop_flag

    engine = pyttsx3.init()
    engine.setProperty("rate", rate)

    voices = engine.getProperty("voices")
    if voice is not None and voice < len(voices):
        engine.setProperty("voice", voices[voice].id)
    else:
        engine.setProperty("voice", voices[0].id)

    structured_text = handle_structured_text(text)
    total_words = len(text.split())
    spoken_words = 0

    def run_speech():
        nonlocal spoken_words
        for section in structured_text:
            if stop_flag.is_set():
                break
            if "Heading:" in section:
                time.sleep(0.5)
                if show_progress:
                    print(f"Heading: {section.replace('Heading:', '').strip()}\n")
            else:
                sentences = split_into_sentences(section)
                for sentence in sentences:
                    if stop_flag.is_set():
                        break
                    pause_flag.wait()  # Wait if paused
                    word_count = len(sentence.split())
                    spoken_words += word_count
                    if show_progress:
                        print(f"{spoken_words}/{total_words} words: {sentence}\n")
                    engine.say(sentence)
                    engine.runAndWait()
                    time.sleep(0.1)

    speech_thread = threading.Thread(target=run_speech)
    speech_thread.start()

    while speech_thread.is_alive():
        try:
            import select
            if sys.platform.startswith('win'):
                import msvcrt
                if msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    if ch.lower() == 'p':
                        pause_flag.clear()
                        print("[Paused]")
                    elif ch.lower() == 'r':
                        pause_flag.set()
                        print("[Resumed]")
                    elif ch.lower() == 'q':
                        stop_flag.set()
                        pause_flag.set()
                        print("[Stopping]")
                        break
            else:
                dr, _, _ = select.select([sys.stdin], [], [], 0.1)
                if dr:
                    ch = sys.stdin.read(1)
                    if ch.lower() == 'p':
                        pause_flag.clear()
                        print("[Paused]")
                    elif ch.lower() == 'r':
                        pause_flag.set()
                        print("[Resumed]")
                    elif ch.lower() == 'q':
                        stop_flag.set()
                        pause_flag.set()
                        print("[Stopping]")
                        break
            time.sleep(0.1)
        except KeyboardInterrupt:
            stop_flag.set()
            pause_flag.set()
            print("\n[Interrupted]")
            break

    speech_thread.join()

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
        print("Enter/Paste your text below. Finish input with Ctrl+D (or ^D) to finish:")
        lines = []
        while True:
            try:
                line = input()
                if line == "^D":
                    break
                lines.append(line)
            except EOFError:
                break
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="TTS Reader Script with Pause/Resume and Automatic Language Detection")
    parser.add_argument("--text", help="Text to read")
    parser.add_argument("--file", help="Path to text file")
    parser.add_argument("--clipboard", action="store_true", help="Read text from clipboard")
    parser.add_argument("--word-indicator", action="store_true", help="Show word count progress per sentence")
    parser.add_argument("--rate", type=int, default=150, help="Set the speech rate (default: 150)")
    parser.add_argument("--voice", type=int, choices=range(0, 20), default=None, help="Choose a voice by index (overrides language detection)")

    args = parser.parse_args()

    raw_text = get_text_from_args(args)
    cleaned = clean_text(raw_text)

    if args.voice is not None:
        chosen_voice = args.voice
    else:
        lang = detect_language(cleaned)
        if lang:
            print(f"Detected language: {lang}")
            engine_tmp = pyttsx3.init()
            chosen_voice = select_voice_by_language(engine_tmp, lang)
            print(f"Using voice index: {chosen_voice}")
        else:
            print("Language detection failed, using default voice.")
            chosen_voice = 0

    print(f"\nStarting speech...\n")
    print("Press 'p' to pause, 'r' to resume, 'q' to quit.\n")
    speak_with_progress(cleaned, show_progress=args.word_indicator, rate=args.rate, voice=chosen_voice)

if __name__ == "__main__":
    main()

