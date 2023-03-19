import requests
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd

url = 'https://www.flipkart.com/dayneo-twsl21-mini-wireless-bluetooth-headset-earphone/product-reviews/itmac7e0ccb65926?pid=ACCFU3G2HEJYHKSS&lid=LSTACCFU3G2HEJYHKSSRKLSUW&marketplace=FLIPKART'

# Set headers to mimic a browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Get the number of pages from the Flipkart website
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
num_pages = soup.find('div', {'class': '_2MImiq _1Qnn1K'})
num_pages = int(num_pages.find_next('span').text.split()[-1])
#print(num_pages)

with open('fknew.csv', 'w', encoding='utf-8') as f:
    f.write('NAMES,RATINGS,REVIEWS\n')  # Write header row to file
    
    for pg in range(1, num_pages+1):
        url = f'https://www.flipkart.com/dayneo-twsl21-mini-wireless-bluetooth-headset-earphone/product-reviews/itmac7e0ccb65926?pid=ACCFU3G2HEJYHKSS&lid=LSTACCFU3G2HEJYHKSSRKLSUW&marketplace=FLIPKART&page={pg}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for item in soup.find_all('div', class_='_1AtVbE col-12-12'):
            name = item.find('p', class_='_2sc7ZR _2V5EHH')
            if name:
                name = name.get_text().strip()
            else:
                name = 'NA'
            #rating
            try:
                rank = item.find('div', class_='_3LWZlK _1BLPMq').get_text().strip()
            except:
                try:
                    rank = item.find('div', class_='_3LWZlK _1rdVr6 _1BLPMq').get_text().strip()
                except:
                    rank = item.find('div', class_='_3LWZlK _32lA32 _1BLPMq')
                    if rank:
                        rank = rank.get_text().strip()
                    else:
                        rank = 'NA'               
            #reviews    
            review = item.find('p', class_='_2-N8zT')
            if review:
                review = review.get_text().strip()
            else:
                review = 'NA'
            f.write(f"{name},{rank},{review}\n")
            print(name, '=',rank, review)
            
        time.sleep(2)
        