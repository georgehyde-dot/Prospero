import requests
import xml.etree.ElementTree as ET
import json
from data.models import Thread, User
from django.utils.dateparse import parse_datetime
from bs4 import BeautifulSoup



def fetch_and_parse_xml(thread_id):
    url = f"https://boardgamegeek.com/xmlapi2/thread?id={thread_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return ET.fromstring(response.content)
    else:
        print("Failed to fetch data")
        return None

def extract_posts_data(xml_root):
    posts_data = []
    for article in xml_root.findall('articles/article'):

        subject_element = article.find('subject')
        article_title = subject_element.text if subject_element is not None else "No Title"

        post_data = {
            'date_posted': article.attrib.get('postdate'),
            'user': article.attrib.get('username'),
            'article_title': article_title,
            'body': article.find('body').text
        }
        posts_data.append(post_data)
    return posts_data

def clean_html(html_content):
    try:
        soup = BeautifulSoup(html_content, "lxml")
        text = soup.get_text()
        return text
    except Exception as e:
        print(f'Exception {e}')


def save_data_to_model(posts_data, thread_id):
    for post in posts_data:
        # Convert date_posted string to datetime object
        date_posted = parse_datetime(post['date_posted'])
        # print(f'Date Posted: {date_posted.date()}')
        
        cleaned_body = clean_html(post['body'])
        # print(f'Cleaned Body: {cleaned_body}')
        user, _ = User.objects.get_or_create(username=post['user'])
        
        article_title = post['article_title'] if post['article_title'] is not None else "No Title"
        if article_title.startswith('Re: '):
            article_title = article_title[4:]
        # print(f'Article: {article_title}')
        thread_id = int(thread_id)
        # print(thread_id)
        Thread.objects.create(
            user=user,
            date_posted=date_posted.date(),  
            thread_id=thread_id,
            article=article_title,
            body=cleaned_body
        )

def main(thread_id):
    try:
        xml_root = fetch_and_parse_xml(thread_id)
        
        if xml_root is not None:
            posts_data = extract_posts_data(xml_root)
            save_data_to_model(posts_data, thread_id)
            print('Data saved in Thread Model')
            return True
    except Exception as e:
        return f'Exception processing Thread: {e}'    

# Example usage
# thread_id = '3257097'
# main(thread_id)
