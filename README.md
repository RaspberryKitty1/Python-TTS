# 🗣️ Python TTS Reader Script

A flexible, interactive Text-to-Speech (TTS) tool for reading text aloud with smart language detection, voice customization, word-level progress tracking, and optional audio file export. Supports input from files, clipboard, or manual entry—all controlled from the terminal.

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

  * Displays word-by-word progress during reading (optional)

* **Interactive Runtime Controls**

  * Type `p` + Enter → Pause
  * Type `r` + Enter → Resume
  * Type `q` + Enter → Quit immediately

* **Audio File Export**

  * Export speech to a WAV file using `--output`
  * Non-interactive mode (no progress or controls)

* **Natural Text Handling**

  * Detects and announces headings
  * Breaks text into natural-sounding phrases

---

## 📦 Requirements

* Python 3.x
* [`pyttsx3`](https://pypi.org/project/pyttsx3/) — Offline TTS engine
* [`pyperclip`](https://pypi.org/project/pyperclip/) — Clipboard access
* [`langdetect`](https://pypi.org/project/langdetect/) — Language detection

Install with:

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**

```txt
pyttsx3
pyperclip
langdetect
```

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

| Argument           | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| `--text`           | Provide text directly                                                  |
| `--file`           | Read text from a file                                                  |
| `--clipboard`      | Use text from the clipboard                                            |
| `--word-indicator` | Display word-by-word progress while reading                            |
| `--rate`           | Set speech rate (e.g., 200 = fast, 100 = slow)                         |
| `--voice`          | Select voice by index (overrides auto-selection)                       |
| `--output`         | Export spoken audio to a WAV file (disables live reading and progress) |

> **Note:**
> Audio file export works best on Windows. On Linux, `pyttsx3` may generate output sentence-by-sentence, causing audio to be overwritten unless properly handled.

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

#### 🧠 Show word-by-word progress

```bash
python tts_reader.py --text "This is some text." --word-indicator
```

#### ⏩ Adjust speech rate

```bash
python tts_reader.py --text "Faster speech here." --rate 200
```

#### 🎙️ Select a specific voice

```bash
python tts_reader.py --text "Different voice." --voice 1
```

#### 💾 Export to audio file

```bash
python tts_reader.py --file "example.txt" --output speech.wav
```

---

## 📝 Manual Text Input (Fallback Mode)

If no input is provided via `--text`, `--file`, or `--clipboard`, the script prompts for manual entry:

```plaintext
Enter/Paste your text below. Finish input with Ctrl+D (Unix) or Ctrl+Z then Enter (Windows):
```

Once input is complete, speech begins (or export starts if `--output` is used).

---

## ⌨️ Runtime Controls (Interactive Only)

During live reading (no `--output`):

* Type `p` + Enter → **Pause**
* Type `r` + Enter → **Resume**
* Type `q` + Enter → **Quit immediately**

Works across Windows, Linux, and macOS — no elevated permissions required.

---

## 🔊 Example Word Indicator Output

```bash
Starting speech...
1/5 words: This  
2/5 words: is  
3/5 words: some  
4/5 words: test  
5/5 words: text.
```

---

## 🔚 Deactivating the Virtual Environment

When you're done:

```bash
deactivate
```

---

## 📄 License

Licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

