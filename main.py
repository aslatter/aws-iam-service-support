#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from typing import List, Tuple
import traceback
import csv
import io
import re


def fetch_webpage(url: str) -> str:
    """Fetch webpage content."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def extract_table_data(
    html: str, table_index: int = 0
) -> Tuple[List[str], List[List[str]]]:
    """Extract headers and rows from the specified table."""
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")

    if not tables or table_index >= len(tables):
        raise ValueError(f"Table index {table_index} not found")

    target_table = tables[table_index]

    # Extract headers
    thead = target_table.find("thead")
    if thead is None:
        raise ValueError("Could not find thead in table")

    header_row = thead.find("tr")
    if header_row is None:
        raise ValueError("Could not find tr in thead")

    headers = []
    for th in header_row.find_all("th"):
        text = th.get_text(strip=True)
        text = re.sub(r"\s+", " ", text)
        headers.append(text)

    # Extract rows - look for tr elements directly in table, excluding those in thead
    rows = []
    for tr in target_table.find_all("tr"):
        # Skip header row(s)
        if tr.parent == thead:
            continue

        row = []
        for td in tr.find_all("td"):
            text = td.get_text(strip=True)
            text = re.sub(r"\s+", " ", text)
            row.append(text)
        if row:  # Only add non-empty rows
            rows.append(row)

    return headers, rows


def convert_to_markdown(headers: List[str], rows: List[List[str]]) -> str:
    """Convert table data to markdown format."""
    # Create the header row
    markdown = "| " + " | ".join(headers) + " |\n"

    # Create the separator row
    markdown += "| " + " | ".join(["---" for _ in headers]) + " |\n"

    # Create the data rows
    for row in rows:
        markdown += "| " + " | ".join(row) + " |\n"

    return markdown


def convert_to_csv(headers: List[str], rows: List[List[str]]) -> str:
    """Convert table data to csv format."""

    w = io.StringIO()
    cw = csv.writer(w)
    cw.writerow(headers)
    cw.writerows(rows)

    return w.getvalue()


def main():
    url = "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html"

    try:
        # Fetch and parse the webpage
        html_content = fetch_webpage(url)
        headers, rows = extract_table_data(html_content)

        # Save markdown
        with open("aws_iam_table.md", "w", encoding="utf-8") as f:
            markdown_table = convert_to_markdown(headers, rows)
            f.write(markdown_table)

        # Save csv
        with open("aws_iam_table.csv", "w", encoding="utf-8") as f:
            csv_data = convert_to_csv(headers, rows)
            f.write(csv_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc())

        try:
            soup = BeautifulSoup(html_content, "html.parser")
            tables = soup.find_all("table")
            print(f"\nFound {len(tables)} tables on the page")
            for i, table in enumerate(tables):
                print(f"\nTable {i}:")
                print(f"Has thead: {table.find('thead') is not None}")
                print(f"Has tbody: {table.find('tbody') is not None}")
                print(f"Number of rows (tr): {len(table.find_all('tr'))}")
        except Exception as debug_e:
            print(f"Debug error: {str(debug_e)}")


if __name__ == "__main__":
    main()
