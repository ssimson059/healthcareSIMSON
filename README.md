# Healthcare Assistant

Simple domain-specific chatbot for **Healthcare**. Frontend is plain HTML/CSS/JS, backend is Python (Flask) calling the Gemini API.

## Setup

1. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your real Gemini API key:
   ```
   cp .env.example .env
   ```
   Get a key from https://aistudio.google.com/apikey

4. Load the .env file (Flask app reads from `os.environ`, so either export the
   variables yourself or run with a tool like `python-dotenv`):
   ```
   export $(cat .env | xargs)   # macOS/Linux
   python app.py
   ```
   On Windows, set the variables manually or use a package like `python-dotenv`
   in a one-line addition to app.py (`from dotenv import load_dotenv; load_dotenv()`).

5. Open your browser at http://localhost:5000

## Notes

- This bot only answers **Healthcare**-related questions by design (system prompt scopes it).
- This assistant gives general health information only and is not a substitute for professional medical advice.
- Replace the placeholder key in `.env` before running — never commit real API keys.
