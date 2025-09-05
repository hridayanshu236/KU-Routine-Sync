from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

BASE_URL = "https://docse.netlify.app/"

def get_latest_routine_url():
    html = requests.get(BASE_URL).text
    soup = BeautifulSoup(html, "html.parser")

    # Find the "Groups" row
    row = soup.find("th", string="Groups")
    if row:
        # The link is inside the 3rd <td> of this row
        td = row.find_next_sibling("td").find_next_sibling("td")
        a = td.find("a", href=True)
        if a:
            return urljoin(BASE_URL, a["href"])

    raise ValueError("No routine link found on homepage.")
