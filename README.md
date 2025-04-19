# YouTube Video Summarizer

A Python script to summarize YouTube videos using AI (DeepSeek).

## Features

*   Extracts video ID from various YouTube URL formats.
*   Fetches video transcripts (prioritizes Chinese, falls back to English).
*   Uses the DeepSeek API to generate a summary of the transcript in Chinese.

## Requirements

*   Python 3.x
*   DeepSeek API Key

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/cming401/youtube-video-summarizer.git
    cd youtube-video-summarizer
    ```
2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3.  Edit `youtube_summarizer.py` and insert your DeepSeek API key:
    ```python
    DEEPSEEK_API_KEY = "INSERT_YOUR_DEEKSEEK_API" # Replace with your actual key
    ```

## Usage

Run the script from your terminal:

```bash
python youtube_summarizer.py
```

The script will prompt you to enter a YouTube video URL. It will then fetch the transcript, summarize it using DeepSeek, and print the summary.

## Note

*   Ensure you have a valid DeepSeek API key with sufficient credits.
*   Video transcript availability depends on the YouTube video settings.
