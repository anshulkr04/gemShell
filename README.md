# gemSHELL
gemShell is a terminal-based interface for interacting with Google's Gemini 2.0 AI model directly from your command line.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/anshulkr/gpter.git
    cd gpter
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Configuration

1. Get your API key from the [Google AI Studio](https://aistudio.google.com/)
2. Create a `.env` file in the root directory and add your API key:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

## Usage

Start the application with:
```bash
python3 main.py
```

## Features

- Interact with Gemini 2.0 in your terminal
- Natural language conversations
- Code generation and explanation

