"""
DCS 211 Lab 3 — Parsing HTML: DCS Minors Info
Group: Max Cory and Sara Maquera

"""

import sys
import os
from bs4 import BeautifulSoup
from Student import Student


def parseMinors(soup):
    """
    Accepts a BeautifulSoup object containing the DCS minors HTML page.
    Returns a tuple (by_year, by_advisor) of dictionaries.


    """

    by_year = {}
    by_advisor = {}
    rows = soup.find_all("tr")

    for row in rows[1:]:
        cells = row.find_all("td")

        if len(cells) < 7:
            continue

        name = cells[0].text.strip()

        email_tag = cells[1].find("a")
        email = email_tag["href"].replace("mailto:", "") if email_tag else ""

        year_text = cells[2].text.strip()
        year = year_text if not year_text.isdigit() else int(year_text)


        majors = [p.strip() for p in cells[3].text.split(",") if p.strip() and p.strip() != "0000"]
        minors = [p.strip() for p in cells[4].text.split(",") if p.strip() and p.strip() != "0000"]
        gecs   = [p.strip() for p in cells[5].text.split(",") if p.strip() and p.strip() != "0000"]

        advisor = cells[6].text.strip()

        stu = Student(name, email, year, majors, minors, gecs, advisor)

        if year not in by_year:
            by_year[year] = []
        by_year[year].append(stu)

        if advisor not in by_advisor:
            by_advisor[advisor] = []
        by_advisor[advisor].append(stu)

        for student_list in list(by_year.values()) + list(by_advisor.values()):
            student_list.sort(key=get_name)

    return (by_year, by_advisor)


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == "--help":
        print("Usage: python dcs211_lab3.py <write CSV? False/True> <optional: HTML filename>")
        sys.exit(0)

    write_csv = False
    if len(sys.argv) > 1:
        write_csv = bool(eval(sys.argv[1].title()))

    if len(sys.argv) > 2:
        html_filename = sys.argv[2]
    else:
        html_files = sorted([f for f in os.listdir() if f.endswith(".html")])
        if not html_files:
            sys.exit("No HTML files found in the current directory.")
        print("HTML files found:\n")
        for f in html_files:
            print(f)
        html_filename = input(
            f"\nEnter name of HTML source (return for default '{html_files[0]}'): "
        ).strip() or html_files[0]

    try:
        with open(html_filename, "r", encoding="utf-8") as f:
            html_text = f.read()
    except Exception:
        sys.exit(f"Error: cannot open or read file '{html_filename}'")

    soup = BeautifulSoup(html_text, "html.parser")

    by_year, by_advisor = parseMinors(soup)

    print("Parsed", sum(len(v) for v in by_year.values()), "students total.")
    print("Years found:", list(by_year.keys()))
    print("Advisors found:", list(by_advisor.keys()))


if __name__ == "__main__":
    main()