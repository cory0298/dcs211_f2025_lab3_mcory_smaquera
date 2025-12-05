"""
DCS 211 Lab 3 — Parsing HTML: DCS Minors Info
Group: Max Cory and Sara Maquera

"""

import sys
import os
import csv
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
from Student import Student
from prettytable import PrettyTable


def parseMinors(soup) -> Tuple[Dict, Dict]:
    """
    Accepts a BeautifulSoup object containing the DCS minors HTML page.
    Returns a tuple (by_year, by_advisor) of dictionaries.
    
    Arguments:
        soup: BeautifulSoup object containing parsed HTML
        
    Returns:
        Tuple containing:
        - by_year: Dictionary mapping year (str/int) -> list of Student objects
        - by_advisor: Dictionary mapping advisor name (str) -> list of Student objects
    """
    by_year = {}
    by_advisor = {}
    
    rows = soup.find_all("tr")
    
    for row in rows[1:]: 
        cells = row.find_all("td")
        
        if len(cells) < 10:
            continue
        
        #Extract student information
        name_cell = cells[1]
        name_link = name_cell.find("a", class_="view_port")
        if name_link and name_link.get("title"):
            name = name_link["title"].strip()
        else:
            name = name_cell.text.strip()
        
        #Skip if name doesn't have a comma
        if not name or "," not in name:
            continue

        #Search the entire row for email
        email_link = row.find("a", href=lambda x: x and x.startswith("mailto:"))
        email = email_link["href"].replace("mailto:", "") if email_link else ""
        
        #Search for year
        year_text = cells[3].text.strip()
        year = year_text if not year_text.isdigit() else int(year_text)

        #Search for majors, minors, and GECs
        majors = [p.strip() for p in cells[6].text.split(",") if p.strip() and p.strip() != "0000"]
        minors = [p.strip() for p in cells[7].text.split(",") if p.strip() and p.strip() != "0000"]
        gecs   = [p.strip() for p in cells[8].text.split(",") if p.strip() and p.strip() != "0000"]

        #Search for advisor
        advisor_cell = cells[9]
        #Remove any hidden spans - showed advisor twice without
        for hidden in advisor_cell.find_all("span", style=lambda x: x and "display:none" in x):
            hidden.decompose()
        advisor = advisor_cell.text.strip()

        stu = Student(name, email, year, majors, minors, gecs, advisor)

        if year not in by_year:
            by_year[year] = []
        by_year[year].append(stu)

        if advisor not in by_advisor:
            by_advisor[advisor] = []
        by_advisor[advisor].append(stu)

    return (by_year, by_advisor)


def printOutput(by_year: Dict, by_advisor: Dict, write_csv: bool) -> None:
    """
    Either writes CSV files (one per graduation year) or prints tables to screen.
    
    Arguments:
        by_year: Dictionary mapping year -> list of Students
        by_advisor: Dictionary mapping advisor -> list of Students
        write_csv: If True, write CSV files; if False, print tables
    """
    if write_csv:
        #Write one CSV file per graduation year
        for year in sorted(by_year.keys()):
            filename = f"dcs_minors_{year}.csv"
            print(f"Writing {filename}...")
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                #Write header row
                writer.writerow(['Last Name', 'First Name', 'Email', 'Year', 
                               'Majors', 'Minors', 'GECs', 'Advisor'])
                
                #Write each student, sorted by name
                sorted_students = sorted(by_year[year], key=lambda s: s.getCSVList()[0])
                for student in sorted_students:
                    writer.writerow(student.getCSVList())
    
    else:
        
        #TABLE 1: All DCS Minors sorted by year, then by name
        table1 = PrettyTable()
        table1.field_names = ["Student", "Email", "Year", "Major(s)", "Minor(s)", "Advisor"]
        table1.align["Student"] = 'l'
        table1.align["Email"] = 'l'
        table1.align["Advisor"] = 'l'
        
        #Add all students, sorted by year then name
        for year in sorted(by_year.keys()):
            #Sort students within each year by last name
            sorted_students = sorted(by_year[year], key=lambda s: s.getCSVList()[0])
            for student in sorted_students:
                csv_data = student.getCSVList()
                
                #Extract data from CSV list
                last_name = csv_data[0]
                first_name = csv_data[1]
                email = csv_data[2]
                year_str = str(csv_data[3])
                majors = csv_data[4]
                minors = csv_data[5]
                advisor = csv_data[7]
                
                #Format name
                name = f"{last_name}, {first_name}"
                
                table1.add_row([name, email, year_str, majors, minors, advisor])
        
        print(table1)
        
        #TABLE 2: Number of DCS Minors per graduation year
        table2 = PrettyTable()
        table2.field_names = ["Year", "# DCS Minors"]
        
        for year in sorted(by_year.keys()):
            table2.add_row([year, len(by_year[year])])
        
        print(table2)
        
        #TABLE 3: Number of DCS Minors per advisor
        table3 = PrettyTable()
        table3.field_names = ["Advisor", "# DCS Minors"]
        table3.align["Advisor"] = 'l'
        
        #Sort advisors by last name
        sorted_advisors = sorted(by_advisor.keys(), 
                                key=lambda name: name.split(',')[0].strip())
        
        for advisor in sorted_advisors:
            table3.add_row([advisor, len(by_advisor[advisor])])
        
        print(table3)

def main():
    """
    Main function to run the DCS Minors utility.
    Handles command-line arguments, reads HTML file, parses data, and outputs results.
    """
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

    printOutput(by_year, by_advisor, write_csv)


if __name__ == "__main__":
    main()