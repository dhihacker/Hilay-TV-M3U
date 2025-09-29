import requests
import json

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)

def get_session():
    s = requests.Session()
    s.headers.update({"User-Agent": CHROME_UA})
    s.max_redirects = 5
    return s

def get_final_url(session, url):
    try:
        resp = session.head(url, allow_redirects=False, timeout=10)
        if 300 <= resp.status_code < 400 and 'Location' in resp.headers:
            return resp.headers['Location']
        return url
    except requests.exceptions.RequestException:
        return url

def generate_m3u_playlist():
    session = get_session()

    manifest_url = 'https://hilaytv.vercel.app/manifest.json'
    try:
        response = session.get(manifest_url, timeout=10)
        response.raise_for_status()
        manifest = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch manifest.json: {e}")
        return

    m3u_content = (
        "#EXTM3U\n"
        "# Generated from Hilay TV API\n"
        "# https://hilaytv.vercel.app/\n\n"
    )

    processed_count = 0
    prefixes = manifest.get('idPrefixes', [])
    for prefix in prefixes:
        channel_url = f"https://hilaytv.vercel.app/stream/tv/{prefix}.mv.json"
        try:
            response = session.get(channel_url, timeout=10)
            response.raise_for_status()
            channel_data = response.json()

            if channel_data and channel_data.get('streams'):
                stream = channel_data['streams'][0]
                name = stream.get('name', prefix)
                original_url = stream.get('url', '')

                if not original_url:
                    print(f"Skipping {prefix}: No URL found")
                    continue

                final_url = get_final_url(session, original_url)

                m3u_content += (
                    f"#EXTINF:-1 tvg-id=\"{prefix}\" tvg-name=\"{name}\" "
                    f"group-title=\"Hilay TV\",{name}\n"
                    f"{final_url}\n\n"
                )

                print(f"Processed: {name} - Original: {original_url} - Final: {final_url}")
                processed_count += 1

        except requests.exceptions.RequestException as e:
            print(f"Error processing {prefix}: {e}")
            continue
        except json.JSONDecodeError:
            print(f"Error decoding JSON for {prefix}")
            continue

    filename = 'hilaytv.m3u'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(m3u_content)

    print(f"\nM3U playlist generated: {filename}")
    print(f"Total channels processed: {processed_count}/{len(prefixes)}")

if __name__ == "__main__":
    generate_m3u_playlist()


