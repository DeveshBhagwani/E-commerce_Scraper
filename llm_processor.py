import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("[-] CRITICAL ERROR: API Key not found in .env file.")

def analyze_review_with_llm(raw_text):
    # A list of currently reliable free models on OpenRouter
    models = [
        "google/gemini-2.0-flash-lite-001:free",
        "mistralai/mistral-small-24b-instruct-2501:free",
        "qwen/qwen-2.5-72b-instruct:free"
    ]

    prompt = f"""
    Analyze the following product review:
    "{raw_text}"
    Return STRICT JSON:
    {{
        "pros": ["list", "of", "3"],
        "cons": ["list", "of", "3"],
        "sentiment_summary": "one sentence"
    }}
    """

    for model_id in models:
        try:
            print(f"[*] Trying model: {model_id}...")
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Devesh Scraper"
                },
                data=json.dumps({
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                clean_json = content.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json)
            
            elif response.status_code == 429:
                print(f"[!] Rate limited on {model_id}. Switching...")
                continue # Try the next model in the list
            
            else:
                print(f"[-] Model {model_id} failed with status {response.status_code}")
                
        except Exception as e:
            print(f"[-] Error with {model_id}: {e}")
            continue

    return None

if __name__ == "__main__":
    test_text = "The screen is beautiful but the battery dies in 4 hours."
    analysis = analyze_review_with_llm(test_text)
    if analysis:
        print("\n[+] SUCCESS:")
        print(json.dumps(analysis, indent=4))
    else:
        print("\n[-] All models are currently rate-limited. Try again in 60 seconds.")