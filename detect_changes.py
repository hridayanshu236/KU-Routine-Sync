import requests, hashlib, os
from bs4 import BeautifulSoup
from get_latest_url import get_latest_routine_url

INSTITUTION = "Kathmandu University, School of Engineering, Department of Computer Science and Engineering"
NAME = "III CE-III/II"

def find_target_table(soup):
    for table in soup.find_all("table"):
        caption = table.find("caption")
        if not caption:
            continue
        institution = caption.find("span", class_="institution")
        name = caption.find("span", class_="name")
        if institution and name:
            if institution.get_text(strip=True) == INSTITUTION and name.get_text(strip=True) == NAME:
                return table
    return None

def routine_changed():
    # Get the latest routine URL
    URL = get_latest_routine_url()
    html = requests.get(URL).text

    # Parse HTML and extract only the target table
    soup = BeautifulSoup(html, "html.parser")
    table = find_target_table(soup)
    if table is None:
        raise ValueError("Target routine table not found on the page.")

    table_html = str(table)  # convert table to string for hashing
    hash_val = hashlib.md5(table_html.encode()).hexdigest()

    # Compare with previous hash
    if os.path.exists("last_hash.txt"):
        with open("last_hash.txt", "r") as f:
            old_hash = f.read().strip()
    else:
        old_hash = ""

    if hash_val != old_hash:
        with open("last_hash.txt", "w") as f:
            f.write(hash_val)
        return True, table_html  # return only the table HTML
    return False, table_html