#!/usr/bin/env python3
import time
import requests

import pypi_fetcher  # local

print("Provide the Python package name: ")
inp = input("> ")
print("Getting package information on Wikidata...")

while True:
    try:
        wikidata_result = pypi_fetcher.PyPI.find_package_wikidata(inp)
        if len(wikidata_result) == 0:
            print("Entry on Wikidata not found.")
        break
    except requests.exceptions.ConnectionError:
        print("Failed. Retrying...")
        time.sleep(1)

while True:
    try:
        print("Getting package information on PyPI...")
        pypi_result = pypi_fetcher.PyPI.get(inp)
        # print(pypi_result)  # Prints out the entire HTTP response, useful for reverse engineering the API
        break
    except requests.exceptions.ConnectionError:
        print("Failed. Retrying...")
        time.sleep(1)

print("--- Results ---")

if len(wikidata_result) == 1:
    print("Wikidata match: " + wikidata_result[0])
elif len(wikidata_result) == 0:
    print("No Wikidata match found.")
else:
    print("Wikidata matches:")
    for item in wikidata_result:
        print("  " + item)
    print("  Note: You might want to merge these items on the Wikidata web editor, or this might be normal.")

if pypi_result["info"]:
    try:
        print("Classifiers: ")
        for item in pypi_result["info"]["classifiers"]:
            print("  " + item)
    except:
        pass

    try:
        print("Homepage: " + pypi_result["info"]["project_urls"]["Homepage"])
    except:
        pass
    # source = shared._not_none(pypi_result["info"]["project_urls"]["Source"], pypi_result["info"]["project_urls"]["Source (GitHub)"])
    # print("Source code repository: " + source)
    # try:
        # print("License: " ["info"]["license"])
    # except:
        # pass

    try:
        print("Depends on: ")
        for item in pypi_result["info"]["requires_dist"]:
            print("  " + item)
    except:
        pass
