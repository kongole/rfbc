import json
import re
import logging

# Configure logging
log_file = "compare_errors.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Keywords to detect
dei_keywords = {"equitable", "inclusive", "inclusion", "underinvested", "underserved", 
                "diversity", "minority", "BIPOC", "DEI"}

def load_results(filename):
    """Load scraped data from JSON."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
        return []

def find_removed_keywords(new_text, old_text, url):
    """Find removed DEI keywords and their sentence context."""
    removed_changes = []
    old_sentences = re.split(r'(?<=[.!?])\s+', old_text)
    
    for sentence in old_sentences:
        for keyword in dei_keywords:
            if keyword in sentence and keyword in old_text and keyword not in new_text:
                removed_changes.append({
                    "url": url,
                    "keyword": keyword,
                    "old_sentence": sentence,
                    "new_sentence": find_replacement(sentence, new_text)
                })

    return removed_changes

def find_replacement(old_sentence, new_text):
    """Find the closest replacement sentence."""
    new_sentences = re.split(r'(?<=[.!?])\s+', new_text)
    
    for sentence in new_sentences:
        if len(set(sentence.split()) & set(old_sentence.split())) > 3:
            return sentence  # Return closest match
    
    return "No replacement found"

def compare_results():
    """Compare live site vs archive."""
    live_data = load_results("results_live.json")
    archive_data = load_results("results_archive.json")

    live_dict = {entry["url"]: entry["content"] for entry in live_data}
    archive_dict = {entry["url"]: entry["content"] for entry in archive_data}

    removed_changes = []

    for url, old_text in archive_dict.items():
        new_text = live_dict.get(url, "")

        if old_text and new_text:
            changes = find_removed_keywords(new_text, old_text, url)
            removed_changes.extend(changes)

    # Save results
    with open("removed_keywords.json", "w", encoding="utf-8") as f:
        json.dump(removed_changes, f, indent=4)

    logging.info("Keyword analysis complete. Check 'removed_keywords.json'.")

compare_results()
