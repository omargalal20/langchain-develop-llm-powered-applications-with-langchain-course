import requests
from bs4 import BeautifulSoup
import os

def scrape_fhir(targeted_url: str, targeted_dir: str):
    # Create the output directory if it doesn't exist
    os.makedirs(targeted_dir, exist_ok=True)

    # Fetch the main FHIR page
    response = requests.get(targeted_url)
    if response.status_code != 200:
        print(f"Failed to fetch {targeted_url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract resource links, excluding those with 'normative-flag' class
    table = soup.select_one('#tabs-1 > table')
    links = table.find_all('a', href=True)
    resource_links = [
        link for link in links
        if 'normative-flag' not in (link.get('class') or []) and
           'versions.html#maturity' not in link['href']
    ]

    # Extract href attributes for the filtered links
    fhir_resources_links = [link['href'] for link in resource_links]

    print(f"Number of FHIR Resources: {len(fhir_resources_links)}")

    for link in fhir_resources_links:
        try:
            resource_url = f"{targeted_url.rsplit('/', 1)[0]}/{link}"
            resource_response = requests.get(resource_url)
            if resource_response.status_code != 200:
                print(f"Failed to fetch {resource_url}")
                continue

            # Write the fetched HTML content to a file
            resource_name = link.split('.')[0]

            file_name = os.path.join(targeted_dir, f"{resource_name}.html")
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(resource_response.text)  # Writing HTML content

            print(f"Saved Resource: {resource_name}")

        except Exception as e:
            print(f"Error processing {link}: {e}")

if __name__ == "__main__":
    base_url = "https://hl7.org/fhir/R5/resourcelist.html"
    output_dir = "scraped_data/fhir"

    scrape_fhir(base_url, output_dir)
