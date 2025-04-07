import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_shl_catalog():
    url = "https://www.shl.com/solutions/products/product-catalog/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    assessments = []
    
    # This is a simplified example - you'd need to adapt this to the actual
    # structure of the SHL website
    product_cards = soup.find_all('div', class_='product-card')
    
    for card in product_cards:
        name = card.find('h3').text.strip()
        url = card.find('a')['href']
        description = card.find('p', class_='description').text.strip()
        
        # Extract other details (type, duration, etc.)
        details = card.find('div', class_='details')
        test_type = details.find('span', class_='type').text.strip()
        duration = details.find('span', class_='duration').text.strip()
        
        # Determine remote and adaptive support (simplified)
        remote_support = "Remote" in details.text
        adaptive_support = "Adaptive" in details.text or "IRT" in details.text
        
        assessments.append({
            'name': name,
            'url': url,
            'description': description,
            'test_type': test_type,
            'duration': duration,
            'remote_testing_support': remote_support,
            'adaptive_irt_support': adaptive_support
        })
    
    df = pd.DataFrame(assessments)
    df.to_csv('shl_assessments.csv', index=False)
    print(f"Scraped {len(assessments)} assessments")

if __name__ == "__main__":
    scrape_shl_catalog()