#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://de.wikisource.org"

band1 = "https://de.wikisource.org/wiki/Kinder-_und_Haus-M%C3%A4rchen_Band_1_(1812)"
band2 = "https://de.wikisource.org/wiki/Kinder-_und_Haus-M%C3%A4rchen_Band_2_(1815)"

paragraphs = []
for band in (band1, band2):
    r = requests.get(band)
    s = BeautifulSoup(r.content, "lxml")

    paragraphs_html = s.select("#mw-content-text > div > div:nth-of-type(2) > p")
    paragraphs += [par.text for par in paragraphs_html]

    links = []
    for i in range(1, 5):
        a_tags = s.select(f"#mw-content-text > div > div:nth-of-type(2) > table:nth-of-type({i}) a")
        links += [BASE_URL + a_tag.get("href") for a_tag in a_tags]

    for link in links:
        link_r = requests.get(link)
        link_s = BeautifulSoup(link_r.content, "lxml")
        link_paragraphs = link_s.select("#mw-content-text > div > div:nth-of-type(2) > p")
        paragraphs += [par.text for par in link_paragraphs]

    with open("german_text.txt", "w") as f:
        f.write("\n".join(paragraphs))
