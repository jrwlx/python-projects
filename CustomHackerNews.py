import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.storylink')
subtext = soup.select('.subtext')


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(l, s):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()  # Title of story
        href = item.get('href', None)  # href contains link of story
        vote = subtext[idx].select('.score')  # number of votes
        if len(vote):  # if votes is not zero
            points = int(vote[0].getText().replace('points', ''))  # converting to votes to type int
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})  # adding title, link, votes into dictionary

    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(links, subtext))
