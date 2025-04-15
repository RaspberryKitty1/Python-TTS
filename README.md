# 🗣️ Python TTS Reader Script

A flexible, interactive script that reads text aloud using Text-to-Speech (TTS) with optional progress tracking. You can input text manually, load from a file, or grab clipboard content—customizable voices and speech rate included.

---

## ✨ Features

- **Multiple Input Options**  
  - Enter text manually  
  - Load from a file  
  - Use clipboard content  

- **Voice & Rate Customization**  
  - Choose from available system voices  
  - Adjust the speech rate (default: 150 WPM)

- **Progress Indicator**  
  - Option to display real-time word count while reading

- **Smart Text Structuring**  
  - Detects headings and paragraphs for natural speech flow

---

## 📦 Requirements

- Python 3.x
- [`pyttsx3`](https://pypi.org/project/pyttsx3/) – Offline TTS engine  
- [`pyperclip`](https://pypi.org/project/pyperclip/) – Clipboard access  

Install both via `pip install -r requirements.txt`.

---

## ⚙️ Installation

### 1. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

- **Windows**:  

  ```bash
  .\venv\Scripts\activate
  ```

- **macOS/Linux**:  

  ```bash
  source venv/bin/activate
  ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### ▶️ Command Line Options

| Argument           | Description                                                  |
|-------------------|--------------------------------------------------------------|
| `--text`          | Directly input the text to read                              |
| `--file`          | Specify a file path to read from                             |
| `--clipboard`     | Use text from the clipboard                                  |
| `--word-indicator`| Display word-by-word progress while reading                  |
| `--rate`          | Set custom speech rate (e.g., 200 for faster, 100 for slower)|
| `--voice`         | Choose voice by index (default is 0 - the first available)   |

---

### 💡 Example Commands

#### Read direct input

```bash
python tts_reader.py --text "Hello, world!"
```

#### Read from file

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

#### Select voice

```bash
python tts_reader.py --text "Different voice." --voice 1
```

---

## 📝 Manual Input (Fallback)

If no `--text`, `--file`, or `--clipboard` option is used, the script will prompt:

```
Enter/Paste your text below. Finish input with Ctrl+D (or ^D on Windows):
```

Once complete, the script begins reading the input aloud.

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
