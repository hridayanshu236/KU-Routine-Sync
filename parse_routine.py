from bs4 import BeautifulSoup

PERIOD_TIMES = {
    1: "07:00-08:00",
    2: "08:00-09:00",
    3: "09:00-10:00",
    4: "10:00-11:00",
    5: "11:00-12:00",
    6: "12:00-13:00",
    7: "13:00-14:00",
    8: "14:00-15:00",
    9: "15:00-16:00",
}

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

def parse_routine(html):
    soup = BeautifulSoup(html, "html.parser")
    table = find_target_table(soup)
    if not table:
        raise ValueError("Target routine table not found!")

    rows = table.find_all("tr")
    routine = []

    for row in rows[1:-1]:  # skip header and footer rows
        day = row.find("th", {"class": "yAxis"}).get_text(strip=True)
        cells = row.find_all("td")

        period_index = 1  # track current period

        for cell in cells:
            colspan = int(cell.get("colspan", 1))

            if "notAvailable" in cell.get("class", []) or "empty" in cell.get("class", []):
                period_index += colspan
                continue

            subject = cell.find("span", {"class": "subject"})
            teacher = cell.find("div", {"class": "teacher"})
            room = cell.find("div", {"class": "room"})

            subject_text = subject.get_text(strip=True) if subject else ""
            teacher_text = teacher.get_text(strip=True) if teacher else ""
            room_text = room.get_text(strip=True) if room else ""

            start_time = PERIOD_TIMES[period_index].split("-")[0]
            end_time = PERIOD_TIMES[period_index + colspan - 1].split("-")[1]
            time_range = f"{start_time}-{end_time}"

            routine.append((day, time_range, subject_text, teacher_text, room_text))

            period_index += colspan

    return routine