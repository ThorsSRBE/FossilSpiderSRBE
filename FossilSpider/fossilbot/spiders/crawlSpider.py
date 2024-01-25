import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import time


class CrawlspiderSpider(CrawlSpider):
    name = "fossilFinding"
    allowed_domains = ["tugraz.at"]
    start_urls = ["https://www.tugraz.at/"]
    deny_urls = ["sprachenzentrum.univie.ac.at", "nioo.knaw.nl/nl/zoeken", "nioo.knaw.nl/en/search"]   # make a list separated by commas, e.g. ["repository.tudelft.nl/islandora", "vondel.humanities.uva.nl/onstage/shows"]
    search_for_list = ["Shell", "Equinor", "BP", "TotalEnergies", "Chevron", "ExxonMobil", "Conoco", "Repsol", "Aramco", "Wintershall", "Vattenfall", "SABIC", "Sabic", "RWE", "ENI", "Schlumberger", "SLB", "NAM", "Gazprom", "Gasunie", "Esso", "Air Liquide", "GasTerra"]

    # no rules other than just to go to the next link
    rules = (Rule (LinkExtractor(deny=(deny_urls)), callback="parse_obj", follow=True),
    )

    def parse_obj(self, response):
        
        # get the whole website body (ignore the head)
        testItem = response.css("body").get()
        print('Accessing: ' + response.url + '\n')        

        # first, quickly check if the search terms appear (avoid expensive Beautiful Soup methods)
        mentionedCompanies = []
        for company in self.search_for_list:
            if company in testItem:
                mentionedCompanies.append(company)

        # if any of the search terms appear, look up their context
        if len(mentionedCompanies) > 0:
            soup = BeautifulSoup(testItem, features="lxml")
            soupText = soup.get_text().strip()
            context = ""
            company_list = ""
            for company in mentionedCompanies:
                index = soupText.find(company)
                if index > 0:
                    company_list += company + "\n"
                    context += soupText[index-20:index+30:1] + "...\n"
                elif company != "BP":          #the letters BP often appear in metadata but are not related to the company
                    company_list += company + "\n"
                    context += "Search term " + company + " found in metadata or image name but not in page text.\n"
            if len(company_list) > 0:
                print('Found references: ' + company_list)
                yield {
                    "URL": response.url,
                    "ParentURL": response.request.headers.get('Referer'),
                    "searchTerm": company_list,
                    "Context": context,            #first appearance of the search term
                }

        return {}

        
        
