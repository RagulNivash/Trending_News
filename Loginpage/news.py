# import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
from flask import jsonify
import io
# import nltk
# nltk.download('punkt')




def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news

    # news_img = sp_page.find_all('link.text')
    # news_data = Article(news_img)
    # image= fetch_news_poster(news_data.top_image)


    return news_list
    # return news_list, image


def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news

    # news_img = sp_page.find_all('link.text')
    # news_data = Article(news_img)
    # image= fetch_news_poster(news_data.top_image)

    return news_list
    # return news_list, image


def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news

    # news_img = sp_page.find_all('link.text')
    # news_data = Article(news_img)
    # image= fetch_news_poster(news_data.top_image)

    return news_list
    # return news_list, image

def fetch_location_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/geo/{}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news

    # news_img = sp_page.find_all('link.text')
    # news_data = Article(news_img)
    # image= fetch_news_poster(news_data.top_image)

    # return news_list, image
    return news_list

def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        return jsonify({'msg':'success','size':[image.width,image.height]})

    except:
        image = Image.open('./no_image.jpg')
        return jsonify({'msg':'success','size':[image.width,image.height]})