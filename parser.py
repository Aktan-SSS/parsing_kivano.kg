import csv
from bs4 import BeautifulSoup
import requests
import lxml

url = "https://www.kivano.kg/mobilnye-telefony"


def get_html(url):
    response = requests.get(url)
    return response.text
    

def get_data_phone(url):    
    soup = BeautifulSoup(url, "lxml")
    all_name_phone = soup.find("div", class_="list-view").find_all("div", class_="item product_listbox oh")
    for name_phon in all_name_phone:
        try:
            title = name_phon.find(class_="listbox_title oh").text
        except:
            title = ""
        print(title)
        try:
            price = name_phon.find(class_="motive_box pull-right").find("strong").text
        except:
            price = ""
        print(price)
        try:
            image = name_phon.find(class_="listbox_img pull-left").find("a").find("img").get("src")
        except:
            image = ""
        print(image)
        
        data = {"title": title, "price": price, "image": image}

        write_to_csv(data)

def write_to_csv(data):
    with open("kivano.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((data["title"], 
                        data["price"], 
                        data["image"]))


def pagers(url):
    soup = BeautifulSoup(url, "lxml")
    pages = soup.find("li", class_="last").text
    return int(pages)


def main():
    url = "https://www.kivano.kg/mobilnye-telefony"
    page = "?page"
    pages = pagers(get_html(url))
    for pag in range(1, pages):
        new_url = url + page + str(pages)
        get_data_phone(get_html(new_url))


main()