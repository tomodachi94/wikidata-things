import os
import requests
#from wikidata_fetcher.WikidataRead import _return_sparql_query_results
from qwikidata.sparql import return_sparql_query_results as _return_sparql_query_results

class PyPI():
    def get(project_name, endpoint="https://pypi.org/pypi/"):
        endpoint = os.path.join(endpoint, project_name, "json")
        response = requests.get(endpoint)
        response = response.json()
        return response

    def find_package_wikidata(
                                  package_name,
                                  sparql_endpoint="https://query.wikidata.org/sparql",
                                  entity_filter="http://www.wikidata.org/entity/",
                                  pypi_package_property = "P5568"
                                  ):
        """
        Checks if a PyPI package has an item on Wikidata.

        Returns a list with Wikidata item refs, in the format
        `Q<item id>`.
        """
        # list for results
        r = []
        # Boilerplate SPARQL query
        query_string = f"""
        SELECT $WDid
        WHERE {{
          ?WDid (wdt:{pypi_package_property})* "{package_name}"
        }}
        """

        http_data = _return_sparql_query_results(
                                                query_string,
                                                wikidata_sparql_url=sparql_endpoint  # In case a test instance is being used.
                                                )

        # This block cleans up the HTTP response and turns it into a list.
        http_data = http_data["results"]["bindings"]
        del http_data[0]
        for item in http_data:
            item["WDid"]["value"] = item["WDid"]["value"].replace(entity_filter, "")
            r.append(item["WDid"]["value"])

        return r
