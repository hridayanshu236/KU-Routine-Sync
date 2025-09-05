import requests, hashlib, os
from bs4 import BeautifulSoup
from get_latest_url import get_latest_routine_url

TABLE_ID = "table_22"  # Only watch this table

def routine_changed():
    # Get the latest routine URL
    URL = get_latest_routine_url()
    html = requests.get(URL).text

    # Parse HTML and extract only the target table
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": TABLE_ID})
    if table is None:
        raise ValueError(f"No table with id {TABLE_ID} found on the page.")

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
        return True, str(table)  # return only the table HTML
    return False, str(table)
