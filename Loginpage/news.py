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
    news_list = news_list[0:10]
    poster_list = getPosterList(news_list)

    return news_list,poster_list

    # return news_list, image


def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    news_list = news_list[0:10]
    poster_list = getPosterList(news_list)

    return news_list,poster_list



def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    news_list = news_list[0:10]
    poster_list = getPosterList(news_list)

    return news_list,poster_list


def fetch_location_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/geo/{}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    news_list = news_list[0:10]
    # print(sp_page)
    poster_list = getPosterList(news_list)

    return news_list,poster_list

def getPosterList(news_list):
    print("Posterlist called")
    poster_list = list()
    for news in news_list:
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            print(e)
        # print(news_data.top_image)
        poster_list.append(news_data.top_image)
    print("len - ",len(poster_list))
    return poster_list