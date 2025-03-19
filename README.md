```md
# RFBC Scraper

## 📌 Overview
RFBC Scraper is a web crawler that:
- ✅ Scrapes all pages of listed websites
- ✅ Retrieves archived versions from Wayback Machine
- ✅ Compares archived content vs. live content
- ✅ Detects removed DEI-related keywords & sentence changes

---

## 📂 Project Structure
```
rfbc_scraper/
│
├── rfbc_scraper/  
│   ├── spiders/
│   │   ├── rfbc_spider.py  <-- Main Scrapy spider
│   ├── settings.py  
│
├── scrapy.cfg  <-- Scrapy configuration file  
├── websites.json  <-- List of websites & archive date  
├── results_live.json  <-- Scraped live website content  
├── results_archive.json  <-- Scraped archived content  
├── removed_keywords.json  <-- Detected keyword removals  
├── process_results.py  <-- Compares live vs. archive data  
├── compare_changes.py  <-- Additional comparison script  
├── run_scrapy.sh  <-- Runs live & archive scrapers  
└── README.md  <-- This file  
```

---

## ⚙️ Installation
### 1️⃣ Clone the repository
```sh
git clone https://github.com/your-repo/rfbc_scraper.git  
cd rfbc_scraper  
```

### 2️⃣ Create a virtual environment
```sh
python3 -m venv venv  
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 3️⃣ Install dependencies
```sh
pip install -r requirements.txt
```

---

## 🚀 Usage
### 1️⃣ Scrape Live Websites
```sh
scrapy crawl rfbc -a mode=live -o results_live.json
```

### 2️⃣ Scrape Archived Websites (Before Jan 20, 2025)
```sh
scrapy crawl rfbc -a mode=archive -o results_archive.json
```

### 3️⃣ Compare Live vs. Archived Data
```sh
python process_results.py
```

### 4️⃣ Run Both Scrapers at Once
```sh
./run_scrapy.sh
```

---

## 📊 Output Files
| File Name               | Description |
|-------------------------|-------------|
| `results_live.json`     | Scraped live website content |
| `results_archive.json`  | Scraped archived content |
| `removed_keywords.json` | Detected keyword removals & sentence changes |
| `scrapy_errors.log`     | Logs errors during scraping |
| `process_results.log`   | Logs comparison results |

---

## 🛠 Configuration
Modify `websites.json` to:
- Add or remove websites
- Change the archive date for Wayback Machine

Example:
```json
{
    "websites": [
        "https://example1.com/",
        "https://example2.com/"
    ],
    "archive_date": "20240101"
}
```

---

## 📝 Troubleshooting
### 1️⃣ Check Log Files for Errors
```sh
cat scrapy_errors.log
cat process_results.log
```
If `removed_keywords.json` is empty, verify that `results_archive.json` contains valid website content.

### 2️⃣ Ensure Proper Cleaning of Archived Data
If archived content contains **Wayback Machine UI junk**, modify `rfbc_spider.py` to remove unnecessary text.

---

## 📌 License
This project is licensed under the **MIT License**.

---

## 🙋‍♂️ Support
For issues or improvements, please open an issue on **GitHub**.
```

This `README.md` provides **complete documentation** in a structured format. 🚀 Let me know if you need any updates!# rfbc
