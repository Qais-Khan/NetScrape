import pprint
import requests
from bs4 import BeautifulSoup

pgcount = input('How many Pages? ')


def get_page(count):
    res = requests.get(f'https://news.ycombinator.com/news?p={count}')
    web = BeautifulSoup(res.text, 'html.parser')
    links = web.select('.storylink')
    subtext = web.select('.subtext')
    return links, subtext


def story_sort(hnlist):
    return sorted(hnlist, key=lambda k: k['vote'], reverse=True)


def create_custom_hn():
    hn = []
    for count in range(1, int(pgcount)+1):
        links, subtext = get_page(count)
        for idx, item in enumerate(links):
            title = item.getText()
            href = item.get('href', None)
            vote = subtext[idx].select('.score')
            if len(vote):
                points = int(vote[0].getText().replace(' points', ''))
                if points > 99:
                    hn.append({'title': title, 'link': href, 'vote': points})
    return story_sort(hn)


pprint.pprint((create_custom_hn()))
