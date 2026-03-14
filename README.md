# Dynamic E-Commerce Competitor Intelligence Scraper

## 🚀 Overview
A sophisticated Python-based data engineering pipeline designed to navigate dynamic, JavaScript-rendered websites and transform unstructured data into structured competitor intelligence. 

This project demonstrates an advanced scraping workflow by integrating **Playwright** for browser automation and **LLMs (via OpenRouter)** to perform automated sentiment analysis and feature extraction.

## 🛠️ Tech Stack
- **Automation:** Playwright (Chromium)
- **Parsing:** BeautifulSoup4
- **Intelligence:** OpenRouter API (Gemini 2.0 Flash / Mistral / Qwen)
- **Environment:** `python-dotenv` for Secure Secret Management
- **Concurrency:** `asyncio` for non-blocking browser operations

## ✨ Key Features
- **Dynamic Navigation:** Handles AJAX/JavaScript-loaded content by waiting for specific DOM elements to populate after interactions (like "Load More" or Year filters).
- **AI-Powered Extraction:** Utilizes a model-rotation strategy to handle API rate limits (429 errors) and ensure high availability of the intelligence layer.
- **Robust Parsing:** Uses BeautifulSoup to clean and structure raw HTML into a clean Python dictionary format before AI processing.
- **Secure Architecture:** Built with a strict separation between code and credentials using environment variables.

## 📁 Project Structure
- `scraper.py`: Manages Playwright browser sessions and BeautifulSoup parsing logic.
- `llm_processor.py`: Orchestrates LLM communication with fallback model logic for maximum reliability.
- `main.py`: The master controller script that executes the full end-to-end pipeline.
- `.env`: (Local only) Stores your OpenRouter API keys.

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/DeveshBhagwani/E-commerce_Scraper.git](https://github.com/DeveshBhagwani/E-commerce_Scraper.git)
   cd E-commerce_Scraper
   ```
2. **Setup Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/Scripts/activate  # Windows: .\venv\Scripts\activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install playwright beautifulsoup4 requests python-dotenv
    playwright install chromium
    ```

4. **Configuration:**
- Create a .env file in the root directory and add your OpenRouter key:

- `OPENROUTER_API_KEY=paste_private_sk_key_here`

5. **Run the Scraper:**

    ```bash
    python main.py
    ```

## 📊 Sample Intelligence Output
The pipeline generates a competitor_intelligence.csv containing:
| Column | Description |
| :--- | :--- |
| Title | The scraped item or product name |
| Year/Date | Extracted temporal data |
| Sentiment | 1-sentence AI-generated summary of the data |
| Pros | Top 3 advantages extracted by the LLM |
| Cons | Top 3 drawbacks extracted by the LLM |

## 🛡️ Security
This project follows industry-standard security practices. The .env file is explicitly ignored in the .gitignore to prevent accidental leakage of API credentials to GitHub.
