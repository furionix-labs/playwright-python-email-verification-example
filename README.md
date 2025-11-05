# Playwright Email Verification (Python)

This project demonstrates how to write an end-to-end (E2E) registration and email verification test using [Playwright](https://playwright.dev/) and [Tigrmail](https://tigrmail.com?utm_source=github-pw-example&utm_medium=readme) as the email API.

## Prerequisites
- Python 3.11+
- npm is **not** required for this folder, but you need the Playwright browsers (`playwright install`) after installing Python dependencies.
- [Tigrmail](https://tigrmail.com?utm_source=github-pw-python-example&utm_medium=readme) account (for API token)

## Setup
1. **Create a virtual environment**
   ```shell
   python3 -m venv .venv
   source .venv/bin/activate
   ```
1. **Install dependencies**
   ```shell
   pip install -r requirements.txt
   playwright install
   ```
2. **Get a Tigrmail API token**
   - Sign up or log in at [https://console.tigrmail.com](https://console.tigrmail.com?utm_source=github-pw-example&utm_medium=readme)
   - Copy your API token
3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Paste your Tigrmail API token as the value for `TIGRMAIL_TOKEN` in `.env`

The test loads `.env` automatically via `python-dotenv`.

## Running the Test in Headed Mode with Slow Motion
```bash
pytest --headed --slowmo 1000
```

The bundled `pytest.ini` sets the base URL to `https://sandbox.tigrmail.com`, so relative paths like `/sign-up` resolve automatically.


