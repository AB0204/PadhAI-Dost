# 🚀 Launch Your World-Beater App

You have two parts to launch:
1.  **The App:** (Chatbot) hosted on Streamlit Cloud.
2.  **The Website:** (Premium Landing Page) hosted on GitHub Pages.

## Part 1: Launch The Website (2 Minutes)
1.  Go to your GitHub Repository: `https://github.com/AB0204/PadhAI-Dost`
2.  Click **Settings** (Top Tab).
3.  Scroll down to **Pages** (Left Sidebar).
4.  Under **Build and deployment**, set:
    *   **Source:** `Deploy from a branch`
    *   **Branch:** `main`
    *   **Folder:** `/docs` (IMPORTANT: Change from /(root) to /docs)
5.  Click **Save**.
6.  Wait 1 minute. Your premium website will be live at:
    👉 `https://ab0204.github.io/PadhAI-Dost/`

## Part 2: Launch The App (3 Minutes)
1.  Go to [Streamlit Community Cloud](https://share.streamlit.io/).
2.  Sign in with GitHub.
3.  Click **New App**.
4.  Select your repository: `AB0204/PadhAI-Dost`.
5.  Set **Main file path**: `app.py`.
6.  **CRITICAL:** Click "Advanced Settings" (or "Settings") -> **Secrets**.
    *   Paste your contents from `.env` here:
    ```
    GEMINI_API_KEY=your_actual_api_key_here
    ```
7.  Click **Deploy**.

## Part 3: Connect Them
1.  Once your Streamlit App is live, copy its URL (e.g., `https://padhai-dost.streamlit.app`).
2.  Edit `docs/index.html` in your repo.
3.  Find the `Launch App` button and replace the link:
    ```html
    <a href="YOUR_STREAMLIT_URL_HERE" target="_blank" class="btn-primary">Launch App</a>
    ```
4.  Git commit & push. Your website now directs traffic to your AI tool!
