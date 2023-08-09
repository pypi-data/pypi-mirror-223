import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import random
from tqdm import tqdm
import logging


class scraper:
    def __init__(self, logger=None):
        self.options = FirefoxOptions()
        self.options.add_argument("--headless")  # Run the browser in headless mode (no GUI)
        self.options.set_preference("permissions.default.image", 2)  # do not load page images
        self.driver = webdriver.Firefox(options=self.options)
        # # Use requests to fetch the initial HTML content of the page
        # response = requests.get(url)
        # initial_html = response.text
        self.driver.implicitly_wait(5)

        self.optionsjson = FirefoxOptions()
        self.optionsjson.set_preference('devtools.jsonview.enabled', False)
        self.optionsjson.set_preference("permissions.default.image", 2)  # do not load page images
        self.optionsjson.add_argument("--headless")  # Run the browser in headless mode (no GUI)
        self.driver_json = webdriver.Firefox(options=self.optionsjson)
        self.driver_json.implicitly_wait(5)

        self.session = requests.Session()

        self.user_agents_list = [
            'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        ]

        self.last_call_time = time.time()

    def get_sub_sitemaps(self, sitemap_url_list, filter_string=None, speedlimit=1000, proxy=None):
        try:
            for sitemap_url in sitemap_url_list:
                self.speedlimit(speedlimit)
                # Step 1: Download the sitemap file
                response = self.get_response(sitemap_url, proxy)

                if response.status_code == 200:
                    sitemap_xml = response.text
                else:
                    print(f"Error: Failed to fetch sitemap. Status code: {response.status_code}")
                    return []

                # Step 2: Parse the XML content
                root = ET.fromstring(sitemap_xml)

                # Step 3: Extract the URLs of the sub sitemaps containing the specific string
                sub_sitemaps = []
                for element in root:
                    loc = element.findtext('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    if filter_string is None or (filter_string in loc):
                        sub_sitemaps.append(loc)

                if not sub_sitemaps:
                    print("No sub sitemaps found.")

                return sub_sitemaps



        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_links_from_sitemaps(self, sitemap_urls, filter_string=None, speedlimit=1000):
        all_product_links = []

        try:
            for sitemap_url in tqdm(sitemap_urls, desc="Parsing Sitemap For Links : ", unit=" Sitemap", leave=False):
                # Download the sitemap XML file

                response = self.get_response(sitemap_url)

                if not response.ok:
                    print(f"Failed to download sitemap from {sitemap_url}")
                    continue

                # Parse the XML data
                xml_data = response.content
                root = ET.fromstring(xml_data)

                # Extract product links from the sitemap XML
                product_links = []
                for child in root:
                    for grandchild in child:
                        if 'loc' in grandchild.tag:
                            product_link = grandchild.text.strip()
                            if not filter_string or filter_string in product_link:
                                product_links.append(product_link)

                all_product_links.extend(product_links)
                self.speedlimit(speedlimit)

        except Exception as e:
            self.logger.warning(f"Scraper Util - Warning Getting Links From Sitemap: {e}")

        return all_product_links

    def get_rendered_page(self, url):
        try:

            self.driver.get(url)

            # Get the fully rendered HTML after JavaScript execution
            rendered_html = self.driver.page_source
            return rendered_html

        except Exception as e:
            self.logger.warning(f"Scraper Util - Warning Getting Rendered Page: {e}")
            return None

    def find_element_by_attribute_equals(self, html, tag_name, attribute_name, attribute_value, return_inner):
        """
        Parse the HTML and find the first element with the specified tag name, attribute name, and attribute value.

        Parameters:
            html (str): The HTML content to be parsed.
            tag_name (str): The tag name of the element to search for.
            attribute_name (str): The name of the attribute to match.
            attribute_value (str): The value of the attribute to match.
            return_inner (bool): Should return only inner HTML

        Returns:
            str: The inner HTML of the first matched element, or None if no element is found.
        """
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find(tag_name, {attribute_name: attribute_value})

        if return_inner:
            return element.text if element else None

        else:
            return element if element else None

    def get_rendered_page_json(self, url):
        try:

            self.driver_json.get(url)

            # Get the fully rendered HTML after JavaScript execution
            rendered_json = self.driver_json.page_source

            return rendered_json

        except Exception as e:
            self.logger.warning(f"Scraper Util - Warning Getting Rendered Page Json: {e}")
            return None

    def get_contents_of_element_by_tag(self, html, tag):
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find(tag)
        return element.contents

    def get_response(self, get_url, proxy=None, debug=False):
        try:
            if proxy:
                response = self.session.get(get_url, timeout=30, proxies={"http": proxy, "https": proxy},
                                            headers={'User-Agent': random.choice(self.user_agents_list)})
            else:
                response = self.session.get(get_url, timeout=30,
                                            headers={'User-Agent': random.choice(self.user_agents_list)})

            if debug:
                self.logger.debug(" ")
                self.logger.debug(f"ScraperUtil - Get Response Debug: URL: {get_url}")
                self.logger.debug("---------------Start Response----------------")
                self.logger.debug(response)
                self.logger.debug("---------------End Response----------------")
                self.logger.debug(" ")
            return response

        except Exception as e:
            self.logger.warning(" ")
            self.logger.warning(f"ScraperUtil - Get Json Request Warning: {e} URL: {get_url}")
            self.logger.warning("---------------Start Response----------------")
            self.logger.warning(response)
            self.logger.warning("---------------End Response----------------")
            self.logger.warning(" ")
            return None

    def get_json_request(self, get_url, proxy=None, debug=False):
        try:
            if proxy:
                response = self.session.get(get_url, timeout=30, proxies={"http": proxy, "https": proxy},
                                            headers={'User-Agent': random.choice(self.user_agents_list)})
            else:
                response = self.session.get(get_url, timeout=30,
                                            headers={'User-Agent': random.choice(self.user_agents_list)})

            if debug:
                print(" ")
                print(f"ScraperUtil - Get Json Request Debug: URL: {get_url}")
                print("---------------Start Response----------------")
                print(response)
                print("---------------End Response----------------")
                print(" ")




                self.logger.debug(" ")
                self.logger.debug(f"ScraperUtil - Get Json Request Debug: URL: {get_url}")
                self.logger.debug("---------------Start Response----------------")
                self.logger.debug(response)
                self.logger.debug("---------------End Response----------------")
                self.logger.debug(" ")

            return response.json()

        except Exception as e:
            self.logger.warning(" ")
            self.logger.warning(f"ScraperUtil - Get Json Request Warning: {e} URL: {get_url}")
            self.logger.warning("---------------Start Response----------------")
            self.logger.warning(response)
            self.logger.warning("---------------End Response----------------")
            self.logger.warning(" ")
            return None

    def speedlimit(self, milliseconds):
        current_time = time.time()
        loop_time = (current_time - self.last_call_time) * 1000  # Convert to milliseconds
        # TODO Add randomize time ability
        if loop_time < milliseconds:
            time.sleep((milliseconds - loop_time) / 1000)  # Convert back to seconds

        self.last_call_time = time.time()
