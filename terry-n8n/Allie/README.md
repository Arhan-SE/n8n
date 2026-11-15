# Allie - Mortgage Assistant

A Streamlit-based chat interface for Allie, your AI-powered mortgage assistant.

## Features

- Clean, responsive chat interface
- Dark/Light mode support
- Message history
- Source attribution for responses
- Mobile-friendly design

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Usage

- Type your mortgage-related questions in the input box and press Enter
- Use the sidebar to change themes or clear the chat history
- View source information for AI-generated responses when available

## Configuration

You can customize the application by modifying the `app.py` file. The following environment variables can be set in a `.env` file:

```
# n8n webhook URL (if different from default)
N8N_WEBHOOK_URL=https://tshelton.app.n8n.cloud/webhook/ba394493-d92a-4ec4-b493-ea237bffa2aa
```
