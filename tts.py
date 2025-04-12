import pyttsx3
import re
import argparse
import pyperclip
import time
import sys

def clean_text(text):
    # Remove HTML-style tags
    text = re.sub(r'<.*?>', '', text)
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    return text.strip()

def split_into_sentences(text):
    # Split text into sentences based on punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def handle_structured_text(text):
    # Split text into paragraphs based on double line breaks
    paragraphs = text.split("\n\n")
    
    structured_text = []
    for paragraph in paragraphs:
        # Skip empty or whitespace-only paragraphs
        if paragraph.strip() == "":
            continue
        
        # Check if it's a heading (typically all caps or short phrases)
        if re.match(r'^[A-Z0-9\s]+$', paragraph):
            structured_text.append(f"Heading: {paragraph}")
        else:
            # Process as normal paragraph
            structured_text.append(paragraph)
    
    return structured_text

def speak_with_progress(text, show_progress=False, rate=150, voice=None):
    engine = pyttsx3.init()

    # Set speaking rate
    engine.setProperty("rate", rate)

    # Set voice
    voices = engine.getProperty("voices")
    if voice is not None:
        engine.setProperty("voice", voices[voice].id)
    else:
        # Default to first available voice if no voice argument
        engine.setProperty("voice", voices[0].id)

    structured_text = handle_structured_text(text)
    total_words = len(text.split())
    spoken_words = 0

    for section in structured_text:
        # Add a pause between headings and paragraphs
        if "Heading:" in section:
            time.sleep(0.5)  # Pause before headings
            if show_progress:
                print(f"Heading: {section.replace('Heading:', '').strip()}\n")
        else:
            sentences = split_into_sentences(section)
            for sentence in sentences:
                word_count = len(sentence.split())
                spoken_words += word_count

                if show_progress:
                    print(f"{spoken_words}/{total_words} words: {sentence}\n")

                engine.say(sentence)
                engine.runAndWait()
                time.sleep(0.1)

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
                if line == "^D":  # Check for Ctrl+D (on Windows or Unix)
                    break
                lines.append(line)
            except EOFError:
                break  # EOF reached, terminate input collection (Ctrl+D in Unix-based systems)

        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="TTS Reader Script with Word Count Progress")
    parser.add_argument("--text", help="Text to read")
    parser.add_argument("--file", help="Path to text file")
    parser.add_argument("--clipboard", action="store_true", help="Read text from clipboard")
    parser.add_argument("--word-indicator", action="store_true", help="Show word count progress per sentence")
    parser.add_argument("--rate", type=int, default=150, help="Set the speech rate (default: 150)")
    parser.add_argument("--voice", type=int, choices=range(0, 10), default=None, help="Choose a voice by index (default: 0)")

    args = parser.parse_args()

    raw_text = get_text_from_args(args)
    cleaned = clean_text(raw_text)

    print(f"\nStarting speech...\n")
    speak_with_progress(cleaned, show_progress=args.word_indicator, rate=args.rate, voice=args.voice)

if __name__ == "__main__":
    main()
