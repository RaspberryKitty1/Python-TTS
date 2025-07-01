# 🗣️ Python TTS Reader Script

A flexible, interactive script that reads text aloud using Text-to-Speech (TTS) with progress tracking, automatic language detection, and full keyboard control. Input text from a file, the clipboard, or directly in the terminal.

---

## ✨ Features

* **Multiple Input Options**

  * Enter text manually
  * Load from a file
  * Use clipboard content

* **Voice & Rate Customization**

  * Automatically selects a voice based on detected language
  * Manually choose voice by index if preferred
  * Set custom speech rate (words per minute)

* **Progress Indicator**

  * Optional word-by-word display while reading aloud

* **Pause / Resume / Quit Controls**

  * `p` + Enter → Pause reading
  * `r` + Enter → resume
  * `q` + Enter → stop reading

* **Smart Text Structuring**

  * Detects and announces headings
  * Breaks paragraphs into natural speech segments

---

## 📦 Requirements

* Python 3.x
* [`pyttsx3`](https://pypi.org/project/pyttsx3/) – Offline TTS engine
* [`pyperclip`](https://pypi.org/project/pyperclip/) – Clipboard access
* [`langdetect`](https://pypi.org/project/langdetect/) – Auto language detection

Install all dependencies via:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Installation

### 1. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

* **Windows**

  ```bash
  .\venv\Scripts\activate
  ```

* **macOS/Linux**

  ```bash
  source venv/bin/activate
  ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` should include:

```txt
pyttsx3
pyperclip
langdetect
```

---

## 🚀 Usage

### ▶️ Command Line Options

| Argument           | Description                                                    |
| ------------------ | -------------------------------------------------------------- |
| `--text`           | Directly input the text to read                                |
| `--file`           | Specify a file path to read from                               |
| `--clipboard`      | Use text from the clipboard                                    |
| `--word-indicator` | Display word-by-word progress while reading                    |
| `--rate`           | Set custom speech rate (e.g., 200 for faster, 100 for slower)  |
| `--voice`          | Choose voice by index (overrides automatic language detection) |

---

### 💡 Example Commands

#### Read direct input

```bash
python tts_reader.py --text "Hello, world!"
```

#### Read from a file

```bash
python tts_reader.py --file "example.txt"
```

#### Read from clipboard

```bash
python tts_reader.py --clipboard
```

#### Show word-by-word progress

```bash
python tts_reader.py --text "This is some text." --word-indicator
```

#### Adjust speech rate

```bash
python tts_reader.py --text "Faster speech here." --rate 200
```

#### Select a specific voice

```bash
python tts_reader.py --text "Different voice." --voice 1
```

---

## 📝 Manual Input (Fallback)

If no `--text`, `--file`, or `--clipboard` option is provided, the script will prompt you to paste or type input:

```plaintext
Enter/Paste your text below. Finish input with Ctrl+D (or ^D on Windows):
```

After submission, the script will begin reading aloud.

---

## 🎛️ Runtime Controls

While the script is speaking, you can interact with it using the keyboard:

* `p` → Pause reading
* `r` → Resume reading
* `q` → Stop and exit immediately

These controls work both in the terminal (Unix/Mac) and in the Windows console.

---

## 🔊 Example Output (With Word Indicator)

```bash
Starting speech...
1/5 words: This
2/5 words: is
3/5 words: some
4/5 words: test
5/5 words: text.
```

---

## 🔚 Deactivating the Environment

When done:

```bash
deactivate
```

---

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for full details.
