import requests
from bs4 import BeautifulSoup
import os
import logging

# Configure logging for debug purposes
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def scrape_images(url, save_folder="images"):
    try:
        # Debug: URL being scraped
        logger.debug(f"Starting to scrape images from URL: {url}")
        
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()
        logger.debug("Successfully fetched the webpage content.")
        
        # Parse the webpage content
        soup = BeautifulSoup(response.content, "html.parser")
        logger.debug("Webpage content parsed with BeautifulSoup.")
        
        # Create the save folder if it doesn't exist
        os.makedirs(save_folder, exist_ok=True)
        logger.debug(f"Directory '{save_folder}' is ready to save images.")
        
        # Find all image tags
        img_tags = soup.find_all("img")
        logger.debug(f"Found {len(img_tags)} image tags on the webpage.")
        
        for index, img_tag in enumerate(img_tags):
            try:
                # Get the image source URL
                img_url = img_tag.get("src")
                print("\n\nhellworld\n\n\n",img_url)
                print("",img_tag,"\n")
                if not img_url:
                    logger.debug(f"Image tag {index + 1} has no 'src' attribute. Skipping.")
                    continue
                
                # Handle relative URLs
                if not img_url.startswith(("http://", "https://")):
                    img_url = requests.compat.urljoin(url, img_url)
                logger.debug(f"Resolved image URL: {img_url}")
                
                # Get the image content
                img_response = requests.get(img_url)
                img_response.raise_for_status()
                logger.debug(f"Successfully fetched image from URL: {img_url}")
                
                # Save the image to the folder
                img_name = os.path.join(save_folder, f"image_{index + 1}.jpg")
                with open(img_name, "wb") as img_file:
                    img_file.write(img_response.content)
                    logger.debug(f"Saved image as: {img_name}")
            except requests.RequestException as e:
                logger.error(f"Error fetching image {index + 1} from {img_url}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error while processing image {index + 1}: {e}")
    except requests.RequestException as e:
        logger.error(f"Error fetching webpage: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")

if __name__ == "__main__":
    # Example usage
    target_url = "https://unojapano.com/listening-scripts-jlpt-n4-07-2024/"  # Replace with your target URL
    scrape_images(target_url)
