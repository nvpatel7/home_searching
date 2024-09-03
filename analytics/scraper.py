import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to fetch and parse Zillow page
def fetch_zillow_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting the data
    try:
        address = soup.find("h1", {"class": "Text-c11n-8-100-2__sc-aiai24-0"}).get_text(strip=True)
    except AttributeError:
        address = None
    
    try:
        price = soup.find("span", {"class": "Price__StyledHeading-fshdp-8-100-2__sc-1me8eh6-0"}).get_text(strip=True).replace("$", "").replace(",", "")
    except AttributeError:
        price = None
    
    # Extract number of beds, baths, and square footage
    try:
        num_beds = soup.find("span", string="beds").find_previous_sibling().get_text(strip=True)
    except AttributeError:
        num_beds = None
    
    try:
        num_baths = soup.find("span", string="baths").find_previous_sibling().get_text(strip=True)
    except AttributeError:
        num_baths = None
    
    try:
        square_footage = soup.find("span", string="sqft").find_previous_sibling().get_text(strip=True).replace(",", "")
    except AttributeError:
        square_footage = None
    
    # Extracting the first image URL
    try:
        image_url = soup.find("li", {"class": "Tile__StyledTile-fshdp-8-100-2__sc-gw6377-0"}).find("img")['src']
    except AttributeError:
        image_url = None
    
    # Compiling the extracted data
    data = {
        "address": address,
        "price": price,
        "square_footage": square_footage,
        "num_beds": num_beds,
        "num_baths": num_baths,
        "image_url": image_url
    }
    return data

# List of Zillow URLs to scrape
urls = [
    "https://www.zillow.com/homedetails/1105-Stonewall-Dr-Mansfield-TX-76063/243024182_zpid/",
    "https://www.zillow.com/homedetails/609-Royal-Minister-Blvd-Lewisville-TX-75056/124873382_zpid/",
    "https://www.zillow.com/homedetails/39-Village-Ln-Colleyville-TX-76034/337078083_zpid/",
    "https://www.zillow.com/homedetails/114-Blackburn-Dr-Coppell-TX-75019/118219570_zpid/",
    "https://www.zillow.com/homedetails/703-Acadia-St-Mansfield-TX-76063/163413886_zpid/",
    "https://www.zillow.com/homedetails/8501-Fresh-Meadows-Rd-North-Richland-Hills-TX-76182/308880133_zpid/",
    "https://www.zillow.com/homedetails/2153-Balcones-Dr-Carrollton-TX-75010/243578540_zpid/",
    "https://www.zillow.com/homedetails/2157-Lookout-Ct-Hurst-TX-76054/83802933_zpid/",
    "https://www.zillow.com/homedetails/804-Glenmont-Rd-Keller-TX-76248/83784526_zpid/",
    "https://www.zillow.com/homedetails/450-Settlers-Ridge-Dr-Keller-TX-76248/79935940_zpid/",
    "https://www.zillow.com/homedetails/1717-Latera-Cir-Flower-Mound-TX-75028/249585436_zpid/",
    "https://www.zillow.com/homedetails/725-Royal-Minister-Blvd-Lewisville-TX-75056/125697873_zpid/",
    "https://www.zillow.com/homedetails/810-Brenda-Dr-Mansfield-TX-76063/340851152_zpid/",
    "https://www.zillow.com/homedetails/1009-Franklin-Dr-Mansfield-TX-76063/2062731626_zpid/"
    # Add more URLs as needed
]

# Fetch data for each URL
data_list = []
for url in urls:
    data = fetch_zillow_data(url)
    data_list.append(data)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file
df.to_csv('zillow_data.csv', index=False)

print("Data has been saved to zillow_data.csv")
