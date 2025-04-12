# Python TTS Reader Script

This script reads text aloud using text-to-speech (TTS) with progress tracking. You can either input text manually, read from a file, or use clipboard content. The script supports voice selection and adjustable speech rate, with an option to show word count progress while reading.

## Features

- **Text Input Options**:
  - Manually enter text.
  - Read from a file.
  - Use the clipboard content.
  
- **Voice and Rate Customization**:
  - Select different voices (default is the first available voice).
  - Adjust speech rate for faster/slower reading.

- **Word Progress Indicator**:
  - Option to display word count progress while reading the text.

- **Structured Text Handling**:
  - The script detects headings and paragraphs to improve speech flow.

## Requirements

- Python 3.x
- `pyttsx3` (Text-to-Speech library)
- `pyperclip` (for clipboard access)

## Installation

### Step 1: Set up a Virtual Environment

It's recommended to use a **virtual environment** to avoid conflicts with your system's Python packages. Here's how to set it up:

1. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:

   - On **Windows**:

     ```bash
     .\venv\Scripts\activate
     ```

   - On **Linux/macOS**:

     ```bash
     source venv/bin/activate
     ```

### Step 2: Install Dependencies

With the virtual environment activated, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Script

After installing the dependencies, you can run the script with any of the available arguments.

## Usage

### Command Line Arguments

| Argument               | Description                                                 |
|------------------------|-------------------------------------------------------------|
| `--text`               | Directly input the text to read.                            |
| `--file`               | Provide the path to a text file to read from.               |
| `--clipboard`          | Use text from the clipboard.                                |
| `--word-indicator`     | Show word count progress while reading the text.            |
| `--rate`               | Set the speech rate (default is 150).                       |
| `--voice`              | Choose a voice by index (default is the first available).   |

### Example Commands

#### Reading text directly from command-line

```bash
python tts_reader.py --text "Hello, how are you today?"
```

#### Reading from a file

```bash
python tts_reader.py --file "example.txt"
```

#### Reading from clipboard

```bash
python tts_reader.py --clipboard
```

#### Showing word count progress

```bash
python tts_reader.py --text "This is some text." --word-indicator
```

#### Adjusting the speech rate

```bash
python tts_reader.py --text "This is some text." --rate 200
```

#### Choosing a voice

```bash
python tts_reader.py --text "This is some text." --voice 1
```

## Input via Command Line

When no text, file, or clipboard argument is provided, the script will prompt you to **enter or paste** text. To end input, press `Ctrl+D` (or type `^D` on Windows).

```bash
Enter/Paste your text below. Finish input with Ctrl+D (or ^D) to finish:
```

After entering the text, the script will start reading it aloud, with word count progress if enabled.

## Example Output

If using the word indicator:

```bash
Starting speech...
1/5 words: This is some text.
2/5 words: And this is more.
```

## Deactivating the Virtual Environment

When you're done, you can deactivate the virtual environment with:

```bash
deactivate
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
