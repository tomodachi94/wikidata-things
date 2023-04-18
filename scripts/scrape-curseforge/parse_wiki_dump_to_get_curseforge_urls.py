from bs4 import BeautifulSoup

from tomodb import Database # local

db = Database("./urls.sqlite3")

def parse_curseforge_urls(xml_file):
    with open(xml_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")

    results = []
    for page in soup.find_all("page"):
        title = page.find("title").text
        content = page.find("text").text

        # Extract URLs using regex
        import re
        urls = re.findall(r"\bhttps?://(?:www\.)?curseforge\.com\/minecraft\S+\b", content)

        for url in urls:
            results.append({"title": title, "curseforge_url": url})

    return results

urls = parse_curseforge_urls("./dump.xml")

for item in urls:
    if not db.get(item['curseforge_url']):
        db.store(item)
    else:
        print(f"ERR: {item['title']} has duplicate")

db.close()
