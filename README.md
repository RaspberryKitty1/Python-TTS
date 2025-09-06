# 🗣️ Python TTS Reader

A flexible, interactive Text-to-Speech (TTS) tool for reading text aloud with **automatic language detection**, **voice customization**, **progress tracking**, and optional **audio file export**. Supports input from **files, clipboard, or manual entry**, with real-time **hotkey controls**.

---

## ✨ Features

* **Multiple Input Options**

  * Enter text manually
  * Load text from a file
  * Use clipboard content

* **Smart Voice Selection**

  * Automatically chooses a voice based on detected language
  * Optionally select a specific voice by index
  * Customize speech rate (words per minute)

* **Live Progress Indicator**

  * Sentence-level progress bar (`--word-indicator`)
  * Optional highlighting of the currently spoken sentence (`--highlight`)

* **Interactive Runtime Controls**

  * `Space` → Pause/Resume
  * `Esc` → Stop immediately
  * Works without typing commands

* **Audio File Export**

  * Export speech to WAV (`--output`)
  * Optionally split sentences (`--split-sentences`)
  * Optionally export MP3 (`--mp3`) using `pydub` + `ffmpeg`

* **Natural Text Handling**

  * Detects headings
  * Breaks text into natural-sounding sentences

---

## 📦 Requirements

* Python 3.x
* [`pyttsx3`](https://pypi.org/project/pyttsx3/) — Offline TTS engine
* [`pyperclip`](https://pypi.org/project/pyperclip/) — Clipboard access
* [`langdetect`](https://pypi.org/project/langdetect/) — Language detection
* [`tqdm`](https://pypi.org/project/tqdm/) — Progress bars
* [`keyboard`](https://pypi.org/project/keyboard/) — Hotkeys (optional)
* [`pydub`](https://pypi.org/project/pydub/) — MP3 conversion (optional)

Install all dependencies:

```bash
pip install -r requirements.txt
```

**requirements.txt**

```txt
pyttsx3>=2.90
pyperclip>=1.8.2
langdetect>=1.0.9
tqdm>=4.64.0
keyboard>=0.13.5
pydub>=0.25.1
```

**Note:** `pydub` requires **ffmpeg** for MP3 conversion.

---

## ⚙️ Installation

### 1. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

* **Windows:**

```bash
.\venv\Scripts\activate
```

* **macOS/Linux:**

```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 🔧 Command-Line Options

| Argument            | Description                                          |
| ------------------- | ---------------------------------------------------- |
| `--text`            | Provide text directly                                |
| `--file`            | Read text from a file                                |
| `--clipboard`       | Use text from the clipboard                          |
| `--word-indicator`  | Show sentence-level progress bar                     |
| `--highlight`       | Highlight the currently spoken sentence              |
| `--rate`            | Set speech rate (words per minute, e.g., 200 = fast) |
| `--voice`           | Select voice by index (overrides auto-selection)     |
| `--output`          | Export spoken audio to WAV file                      |
| `--split-sentences` | Save each sentence separately                        |
| `--mp3`             | Convert output to MP3 (requires `pydub` + `ffmpeg`)  |
| `--list-voices`     | List available voices and exit                       |

---

### 💡 Examples

#### 🔤 Read direct input

```bash
python tts_reader.py --text "Hello, world!"
```

#### 📂 Read from a file

```bash
python tts_reader.py --file "example.txt"
```

#### 📋 Read from clipboard

```bash
python tts_reader.py --clipboard
```

#### 🧠 Show progress bar and highlight sentences

```bash
python tts_reader.py --file "example.txt" --word-indicator --highlight
```

#### ⏩ Adjust speech rate

```bash
python tts_reader.py --text "Faster speech here." --rate 200
```

#### 🎙️ Select a specific voice

```bash
python tts_reader.py --text "Different voice." --voice 1
```

#### 💾 Export to audio file (WAV)

```bash
python tts_reader.py --file "example.txt" --output speech.wav
```

#### 💾 Export to audio file (MP3) and split sentences

```bash
python tts_reader.py --file "example.txt" --output speech.wav --mp3 --split-sentences
```

#### 📋 List available voices

```bash
python tts_reader.py --list-voices
```

---

## 📝 Manual Text Input (Fallback Mode)

If no input is provided via `--text`, `--file`, or `--clipboard`, the script prompts for manual entry:

```plaintext
Enter/Paste your text below. Finish input with Ctrl+D (Unix) or Ctrl+Z then Enter (Windows):
```

---

## ⌨️ Runtime Controls (Interactive Only)

During live reading (no `--output`):

* `Space` → Pause/Resume
* `Esc` → Stop immediately

No elevated permissions required (keyboard library must be installed for hotkeys).

---

## 🔚 Deactivating the Virtual Environment

```bash
deactivate
```

---

## 📄 License

MIT License – see [LICENSE](LICENSE) for details.

