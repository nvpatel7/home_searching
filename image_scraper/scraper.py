from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download an image
def download_image(image_url, folder_path, image_name):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(folder_path, image_name), 'wb') as file:
            for chunk in response:
                file.write(chunk)

# Function to extract the largest image URL from srcset
def get_largest_image_url(srcset):
    urls = srcset.split(',')
    largest_image_url = max(urls, key=lambda url: int(url.split()[-1][:-1]))  # get the URL with the largest width
    return largest_image_url.split()[0]

# Main function to scrape images
def scrape_images(url, base_folder='images', sub_folder='801BrendaDrive'):
    # Path to the geckodriver executable
    geckodriver_path = '../../Downloads/geckodriver'  # Update this path

    # Set up the Selenium WebDriver for Firefox
    service = Service(geckodriver_path)
    options = webdriver.FirefoxOptions()
    # Remove the headless option to see the browser window
    # options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)

    # Open the URL
    driver.get(url)
    time.sleep(5)  # wait for the page to load

    # Click the button to show all photos
    try:
        show_photos_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "StyledGallerySeeAllPhotosButton-fshdp-8-100-2__sc-167rdz3-0"))
        )
        show_photos_button.click()
        print("Clicked 'See all photos' button. Please manually scroll down.")
        time.sleep(30)  # Wait 30 seconds for manual scrolling
    except Exception as e:
        print(f"Failed to click the 'see all photos' button: {e}")
        driver.quit()
        return

    # Create the base folder and subfolder
    create_directory(base_folder)
    folder_path = os.path.join(base_folder, sub_folder)
    create_directory(folder_path)

    # Wait until all <li> elements with the class are present
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.Tile__StyledTile-fshdp-8-100-2__sc-gw6377-0'))
    )

    # Find all image elements
    li_elements = driver.find_elements(By.CSS_SELECTOR, 'li.Tile__StyledTile-fshdp-8-100-2__sc-gw6377-0')

    downloaded_urls = set()  # Set to track downloaded URLs
    image_counter = 1  # Counter for image numbering

    for li in li_elements:
        try:
            picture = li.find_element(By.TAG_NAME, 'picture')
            if picture:
                sources = picture.find_elements(By.TAG_NAME, 'source')
                for source in sources:
                    if 'image/webp' in source.get_attribute('type'):
                        srcset = source.get_attribute('srcset')
                        if srcset:
                            img_url = get_largest_image_url(srcset)
                            if img_url not in downloaded_urls:
                                downloaded_urls.add(img_url)
                                img_name = f"image_{image_counter}.webp"
                                download_image(img_url, folder_path, img_name)
                                print(f"Downloaded {img_name}")
                                image_counter += 1
                            else:
                                print(f"Skipped duplicate image: {img_url}")
                            break
        except Exception as e:
            print(f"Error processing element: {e}")

    driver.quit()

# Example usage
scrape_images('https://www.zillow.com/homedetails/801-Brenda-Dr-Mansfield-TX-76063/349659105_zpid/')
