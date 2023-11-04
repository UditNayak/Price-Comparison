from flask import Flask, render_template, request, redirect, session
from scraper import get_data_from_amazon, get_data_from_flipkart, get_product_url_amazon, get_product_url_flipkart

app = Flask(__name__) #creating the Flask class object   

@app.route('/', methods = ['POST','GET']) #decorator drfines the   
def home():
    flipkart_data = None
    amazon_data = None
    flipkart_error = ""
    amazon_error = ""

    if request.method == "POST":
        flipkart_url = request.form.get('flipkart')
        amazon_url = request.form.get('amazon')
        product_name = request.form.get('product_name')

        if product_name:
            amazon_url = get_product_url_amazon(product_name)
            flipkart_url = get_product_url_flipkart(product_name)

        if flipkart_url.startswith("https://www.flipkart.com") == False:
            flipkart_error = "invalid url, please try again"
        else:
            flipkart_data = get_data_from_flipkart(flipkart_url)

        if amazon_url.startswith("https://www.amazon.in") == False:
            amazon_error = "invalid url, please try again"
        else:
            amazon_data = get_data_from_amazon(amazon_url)


    return render_template('index.html', flipkart_data = flipkart_data, amazon_data=amazon_data, user_data = request.form, flipkart_error = flipkart_error, amazon_error = amazon_error)


if __name__ =='__main__':  
    app.run(debug = True)  