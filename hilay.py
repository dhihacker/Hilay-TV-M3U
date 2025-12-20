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
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

    try:
        response = requests.get(
            M3U_URL,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"M3U playlist downloaded successfully: {OUTPUT_FILE}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download M3U: {e}")

if __name__ == "__main__":
    download_m3u()

