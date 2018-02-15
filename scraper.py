#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://de.wikisource.org"
BOOKS = [
    {
        "url": "https://de.wikisource.org/wiki/Kinder-_und_Haus-M%C3%A4rchen_Band_1_(1812)",
        "link_tables": 4,
    },
    {
        "url": "https://de.wikisource.org/wiki/Kinder-_und_Haus-M%C3%A4rchen_Band_2_(1815)",
        "link_tables": 4,
    },
    {
        "url": "https://de.wikisource.org/wiki/Kinder-_und_Haus-M%C3%A4rchen_Band_1_(1857)",
        "link_tables": 4,
    },
    {
        "url": "https://de.wikisource.org/wiki/Kinder-_und_Haus-M%C3%A4rchen_Band_2_(1857)",
        "link_tables": 4,
    },
    {
        "url": "https://de.wikisource.org/wiki/Deutsche_Sagen_(Br%C3%BCder_Grimm,_Band_1)",
        "link_tables": 10,
    },
    {
        "url": "https://de.wikisource.org/wiki/Deutsche_Sagen_(Br%C3%BCder_Grimm,_Band_2)",
        "link_tables": 6
    },
]
OUTPUT_FILE = "german_text.txt"
FORBIDDEN = ["jude"]


if __name__ == '__main__':
    paragraphs = []
    for band in BOOKS:
        band_url = band["url"]
        r = requests.get(band_url)
        s = BeautifulSoup(r.content, "lxml")
        band_title = s.title.text
        print(f"Scraping {band_title}")

        paragraphs_html = s.select("#mw-content-text > div > div:nth-of-type(2) > p")
        paragraphs += [par.text for par in paragraphs_html]

        num_link_tables = band["link_tables"]
        links = []
        for i in range(1, num_link_tables + 1):
            a_tags = s.select(f"#mw-content-text > div > div:nth-of-type(2) > table:nth-of-type({i}) a")
            links += [BASE_URL + a_tag.get("href") for a_tag in a_tags]

        num_links = len(links)
        plural_s = "s" if num_links != 1 else ""
        print(f"Scraping {num_links} link{plural_s} from {band_title}.")
        for link in links:
            link_r = requests.get(link)
            link_s = BeautifulSoup(link_r.content, "lxml")
            link_paragraphs = link_s.select("#mw-content-text > div > div:nth-of-type(2) > p")
            paragraphs += [par.text for par in link_paragraphs]

        current_num_paragraphs = len(paragraphs)
        print(f"Total text paragraphs found: {current_num_paragraphs}.")
        print("#####################################")
        print("")

    print("Finding unique paragraphs.")
    paragraphs = set(paragraphs)
    paragraphs = [par for par in paragraphs if not any(forbidden in par.lower() for forbidden in FORBIDDEN)]
    current_num_paragraphs = len(paragraphs)
    print(f"Total unique text paragraphs found: {current_num_paragraphs}.")
    print(f"Writing to {OUTPUT_FILE}.")
    with open("german_text.txt", "w") as f:
        f.write("\n".join(paragraphs))
    print("Done!")
