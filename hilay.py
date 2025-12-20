import requests

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)

M3U_URL = "https://hilay.tv/play.m3u"
OUTPUT_FILE = "hilaytv.m3u"

def download_m3u():
    headers = {
        "User-Agent": CHROME_UA
    }

    try:
        response = requests.get(M3U_URL, headers=headers, timeout=15)
        response.raise_for_status()

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"M3U playlist downloaded successfully: {OUTPUT_FILE}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download M3U: {e}")

if __name__ == "__main__":
    download_m3u()
