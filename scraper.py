import requests
from bs4 import BeautifulSoup

header = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0", 
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8" }

def get_data_from_flipkart(url):
    #TODO: validate url

    page = requests.get(url, headers=header)
    
    if(page.ok == False):
        return page.reason
    
    soup = BeautifulSoup(page.text, "html.parser")

    product_name = "N/A"
    price = "Out of Stock"
    img_url = "N/A"
    rating = "N/A"
    review_counts = "Be the first to Review this product"

    try:
        product_name = soup.find("span", class_="B_NuCI").text.strip()
    except:
        pass
    
    try:
        price = soup.find("div", class_="_30jeq3 _16Jk6d").text.strip()
        # price = int(price[1:].replace(",", ""))
    except:
        pass
    
    try:
        img = soup.find("img", class_="_396cs4 _2amPTt _3qGmMb") or soup.find("img", class_="_2r_T1I _396QI4")
        img_url = img["src"]
    except:
        pass
    
    try:
        rating = soup.find("div", class_="_3LWZlK").text
    except:
        pass
        
    try:
        review_counts = soup.find("span", class_="_2_R_DZ").span.span.text.split(" ")[0]
    except:
        pass
        
    data = {"product_name":product_name, "price": price, "img_url":img_url, "rating": rating, "review_counts": review_counts}
    return data


def get_data_from_amazon(url):
    page = requests.get(url, headers=header)

    if(page.ok == False):
        return page.reason

    soup = BeautifulSoup(page.text, "html.parser")
    
    product_name = "N/A"
    price = "Out of Stock"
    img_url = "N/A"
    rating = "N/A"
    review_counts = "N/A"

    try:
        product_name = soup.find('span', {'id': 'productTitle'}).get_text().strip()
    except:
        pass

    try:
        price = soup.find('span', class_="priceToPay").text.strip()
        # price = int(price_raw[1:].replace(",", ""))
    except:
        pass

    try:
        img = soup.find("img", id="landingImage")
        img_url = img["src"]
    except:
        pass

    try:
        rating = soup.find("span", id="acrPopover").span.span.text.strip()
    except:
        pass

    try:
        review_counts = soup.find("span", id="acrCustomerReviewText").text.replace("ratings","").strip()
    except:
        pass

    data = {"product_name":product_name, "price": price, "img_url":img_url, "rating": rating, "review_counts": review_counts}
    return data


def get_product_url_flipkart(product_name):
    search_url = "https://www.flipkart.com/search?q="+ product_name
    search_result = requests.get(search_url, headers=header)
    soup = BeautifulSoup(search_result.text, "html.parser")
    
    displyed_items = soup.find_all("div", class_="_2kHMtA") or soup.find_all("div", class_="_4ddWXP") or soup.find_all("div", class_="_1xHGtK")

    for item in displyed_items:
        if "Sponsored" not in item.text:
            item_url = "https://www.flipkart.com" + item.a["href"]
            return item_url
        
    return "no results"


def get_product_url_amazon(product_name):
    search_url = "https://www.amazon.in/s?k="+ product_name
    search_result = requests.get(search_url, headers=header)
    soup = BeautifulSoup(search_result.text, "html.parser")
    displyed_items = soup.find_all("div", class_="s-title-instructions-style")

    for item in displyed_items:
        if "Sponsored" not in item.text:
            item_url = "https://www.amazon.in/" + item.a["href"]
            return item_url
    return "no results"
