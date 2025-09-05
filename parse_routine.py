from bs4 import BeautifulSoup

TABLE_ID = "table_22"

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

def parse_routine(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": TABLE_ID})
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