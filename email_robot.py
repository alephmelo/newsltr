import sqlite3, requests, re, time
from bs4 import BeautifulSoup
from mailer import Mailer, Message

def task():
    # Crawler
    url = "http://www.packtpub.com/packt/offers/free-learning"  # Url to be loaded.
    r = requests.get(url)  # Using requests to get content.
    data = r.text  # Take to plain text into data var.
    soup = BeautifulSoup(data, "html5lib")
    title = soup.find('div', class_='dotd-title').contents[1].string
    desc = soup.find('div', class_='dotd-main-book-summary float-left'
                     ).contents[7].string
    title = re.sub('\s+', ' ', str(title))
    desc = re.sub('\s+', ' ', str(desc))

    # Database connect
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT email FROM core_person")
    result = c.fetchall()

    # Mailer
    me = 'kofieco@gmail.com'
    gmail_smtp = 'smtp.gmail.com:587'

    # Password
    with open('data.txt', 'r') as f: # The password is stored in a plain text file
        pswd = f.read()

    # Actual emailing
    for x in result:
        message = Message(From=me, To=x[0], charset="utf-8")
        message.Subject = "Hey, there's a new ebook today."
        message.Html = """ 
        			<center>
        			<h1>%s</h2>
        			<p>%s</p>
        			<a href="http://www.packtpub.com/packt/offers/free-learning" target="_blank">Claim your book!</a>
        			</center>
        				""" % (title, desc)
        sender = Mailer(gmail_smtp, use_tls=True, usr=me, pwd=pswd)
        sender.send(message)

    time.sleep(60)

while True:
    task()