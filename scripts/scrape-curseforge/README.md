# `scrape-curseforge`

This is a set of scripts to scrape the [Feed The Beast Wiki](https://ftb.fandom.com) for [CurseForge](https://curseforge.com) links, scrape those links for CurseForge project IDs, then create a [OpenRefine project](https://openrefine.org) batch which imports them into Wikidata. This is entirely done in SQLite.

## Instructions

1. Download an export from the wiki's `Special:Export` page. Save the resulting file to `dump.xml` in this folder.
2. Install dependencies using `pip install -r requirements.txt`. You will also need a copy of Firefox installed.
4. Execute `python3 parse_wiki_dump_to_get_curseforge_urls.py` to begin the process. This should be pretty quick.
5. Execute `python3 curseforge_urls_to_project_ids.py` to begin web scraping. This could take up to a few hours (for me it took 2).
6. Open the SQLite database in OpenRefine. There is a 'history' of OpenRefine commands used available in the `openrefine.json` file.
7. Export to QuickStatements or commit the edits directly in OpenRefine.

