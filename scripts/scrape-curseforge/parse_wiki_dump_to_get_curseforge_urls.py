from bs4 import BeautifulSoup

from tomodb import Database  # local


def parse_curseforge_urls(
    xml_file,
    regex=r"\b(https|http)?://(?:(www|minecraft)\.)?curseforge\.com\/minecraft\S+\b",
    field_name="curseforge_url",
):
    """A function which parses a MediaWiki export for CurseForge URLs.

    This function's parameters can be replaced with other values to scrape
    other services from the wiki; look at the `regex` and `field_name` params.
    """
    soup = BeautifulSoup(xml_file, "xml")

    results = []
    for page in soup.find_all("page"):
        title = page.find("title").text
        content = page.find("text").text

        # Extract URLs using regex
        import re

        urls = re.findall(regex, content)

        for url in urls:
            results.append({"title": title, field_name: url})

    return results


def store_curseforge_urls():
    db = Database("./urls.sqlite3")
    with open("./dumps.xml", encoding="utf-8") as xml_file:
        urls = parse_curseforge_urls(xml_file)

    for item in urls:
        if not db.get(item["curseforge_url"]):
            db.store(item)
        else:
            print(f"ERR: {item['title']} has duplicate")

    db.close()
