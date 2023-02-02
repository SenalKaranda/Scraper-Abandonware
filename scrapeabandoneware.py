import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

#totalPages = int(input("Enter the number of pages to scrape: "))
#genre = input("Enter the genre: ")



scrape_params = {
    "action" : 31,
    "adventure" : 18,
    "arcade" : 32,
    "classics" : 1,
    "economics" : 3,
    "educational" : 3,
    "fighting" : 2,
    "FPS" : 7,
    "logical" : 4,
    "platform" : 10,
    "point and click" : 8,
    "puzzle" : 7,
    "racing" : 10,
    "RTS" : 5,
    "shooter" : 10,
    "simulator" : 8,
    "sports" : 7,
    "strategy" : 16,
    "TPP" : 3,
    "turn-based" : 1
}

scrape_genres = list(scrape_params.keys())
scrape_pages = list(scrape_params.values())

url = ""
file_name = ""

for x in range((len(scrape_genres) + 1)):
    totalPages = int(scrape_pages[x])
    genre = str(scrape_genres[x])

    
    file_name = "scraped_data_" + genre + ".xlsx"

    new_sheet_name = genre.capitalize()

    # Append data to existing file
    writer = pd.ExcelWriter(file_name, engine='openpyxl')
    if new_sheet_name not in writer.book.sheetnames:
        writer.book.create_sheet(new_sheet_name)

    # Loop through all pages
    for i in range(1, totalPages + 1):
        url = "https://abandonwaregames.net/browse/games/" + str(i) + "/genre/" + str(genre)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        elements = soup.find_all(class_="text-white mb-1")
        data = [element.text for element in elements]
        df = pd.DataFrame(data)

        start_row = int(writer.book[new_sheet_name].max_row) + 1

        df.to_excel(writer, sheet_name=new_sheet_name,index=False, startrow=start_row, header=False)

    if "Sheet1" in writer.book.sheetnames:
        del writer.book["Sheet1"]

    writer.save()
