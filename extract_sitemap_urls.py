import requests
import xml.etree.ElementTree as ET
import time
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
}

DELAY_RANGE = (1, 3)  # Delay between requests in seconds

def fetch_sitemap_urls(sitemap_url, depth=0):
    urls = []
    try:
        time.sleep(random.uniform(*DELAY_RANGE))  # be polite
        response = requests.get(sitemap_url, headers=HEADERS)
        
        if response.status_code == 429:
            print(f"[!] Received 429 Too Many Requests. Waiting longer before retrying: {sitemap_url}")
            time.sleep(10)
            return fetch_sitemap_urls(sitemap_url, depth)

        response.raise_for_status()
        content = response.content

        root = ET.fromstring(content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Check if it's a sitemap index
        if root.tag.endswith('sitemapindex'):
            for sitemap in root.findall('ns:sitemap', namespace):
                loc = sitemap.find('ns:loc', namespace)
                if loc is not None:
                    child_urls = fetch_sitemap_urls(loc.text, depth + 1)
                    urls.extend(child_urls)
        elif root.tag.endswith('urlset'):
            for url in root.findall('ns:url', namespace):
                loc = url.find('ns:loc', namespace)
                if loc is not None:
                    urls.append(loc.text)
    except Exception as e:
        print(f"Error fetching {sitemap_url}: {e}")
    return urls

def save_urls_to_file(urls, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(f"{url}\n")

if __name__ == "__main__":
    sitemap_url = input("Enter sitemap URL: ").strip()
    output_file = "sitemap_urls.txt"

    print("Fetching URLs. Please be patient...")
    all_urls = fetch_sitemap_urls(sitemap_url)
    save_urls_to_file(all_urls, output_file)

    print(f"✅ Extracted {len(all_urls)} URLs to {output_file}")

