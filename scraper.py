#!/usr/bin/env python3
"""
This is a template for a Python scraper on morph.io (https://morph.io)
including some code snippets below that you should find helpful

Based on https://github.com/planningalerts-scrapers/noosa_council
"""
import os
import sys
# import scraperwiki
import lxml.html
import requests
from morph_planningalerts import DevelopmentApplication, MorphDatabase

DEFAULT_START_URL = "http://engage.bayswater.wa.gov.au/planning-applications-public-advertising"

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".

def main(url):
    MorphDatabase.init()

    html = requests.get(url)
    tree = lxml.html.fromstring(html.content)
    print(tree)
    sys.exit(0)

    count_new = total = 0
    for application_url in get_application_links(url):

        if not application_url:
            # Skipped entry...
            total += 1
            continue

        # html = scraperwiki.scrape(url)

        # XPath
        #This will create a list of buyers:
        buyers = tree.xpath('//div[@title="buyer-name"]/text()')
        #This will create a list of prices
        prices = tree.xpath('//span[@class="item-price"]/text()')

        # Find something on the page using css selectors
        # root.cssselect("div[align='left']")
        #
        data = extract_application_details(application_url)

        application, created = DevelopmentApplication.get_or_create(**data)

        total += 1

        if not created:
            print("* Skipping {0.council_reference}".format(application))
        else:
            print("Saved {0.council_reference}".format(application))
            count_new += 1

    print("Added {0} records out of {1} processed.".format(count_new, total))


if __name__ == "__main__":
    main(os.environ.get('MORPH_START_URL', DEFAULT_START_URL))

