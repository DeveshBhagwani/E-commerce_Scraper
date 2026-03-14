import asyncio
import csv
import os
from scraper import navigate_and_load, parse_reviews
from llm_processor import analyze_review_with_llm

async def run_pipeline():
    # 1. Scraping Phase
    TARGET_URL = "https://www.scrapethissite.com/pages/ajax-javascript/"
    TARGET_YEAR = "2015"
    
    print(f"[*] Phase 1 & 2: Scraping {TARGET_YEAR} data...")
    raw_html = await navigate_and_load(TARGET_URL, TARGET_YEAR)
    items = parse_reviews(raw_html)
    
    if not items:
        print("[-] No items found to process. Exiting.")
        return

    # 2. Processing Phase
    final_dataset = []
    # Testing with a subset (first 5) to ensure we don't hit 429 errors immediately
    limit = 5 
    print(f"[*] Phase 3: Analyzing top {limit} items with AI...")

    for i, item in enumerate(items[:limit]):
        print(f"[>] ({i+1}/{limit}) Processing: {item['raw_text']}")
        
        # Call the LLM (which now uses your fallback logic)
        analysis = analyze_review_with_llm(item['raw_text'])
        
        if analysis:
            # Merge scraped data with AI-generated insights
            combined_entry = {
                "Title": item['raw_text'],
                "Year": item['date'],
                "Awards": item['rating'],
                "Sentiment": analysis.get("sentiment_summary", "N/A"),
                "Pros": " | ".join(analysis.get("pros", [])),
                "Cons": " | ".join(analysis.get("cons", []))
            }
            final_dataset.append(combined_entry)
        
        # Polite delay to help avoid 429 Rate Limits
        await asyncio.sleep(1)

    # 3. Export Phase
    if final_dataset:
        output_file = "competitor_intelligence.csv"
        keys = final_dataset[0].keys()
        
        print(f"[*] Phase 4: Exporting to {output_file}...")
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(final_dataset)
        
        print(f"\n[!] SUCCESS: Created {output_file} with {len(final_dataset)} enriched records.")
    else:
        print("[-] No data was successfully processed by the LLM.")

if __name__ == "__main__":
    asyncio.run(run_pipeline())