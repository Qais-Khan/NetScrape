# import modules
import pprint
import requests
from bs4 import BeautifulSoup

# determine number of pages to scrape
pgcount = input('How many Pages? ')


# change page to scrape the next page
def get_page(count):
    res = requests.get(f'https://news.ycombinator.com/news?p={count}')
    web = BeautifulSoup(res.text, 'html.parser')
    links = web.select('.storylink')
    subtext = web.select('.subtext')
    return links, subtext


# use scraped data and "clean", leaving only articles within given params
def clean_scraped_page():
    articles = []
    for count in range(1, int(pgcount) + 1):  # repeat for each page
        links, subtext = get_page(count)
        for idx, item in enumerate(links):
            title = item.getText()
            href = item.get('href', None)
            vote = subtext[idx].select('.score')
            if len(vote):  # ignore articles with no votes at all to avoid errors
                points = int(vote[0].getText().replace(' points', ''))
                if points > 99:  # only append articles with over 100 votes
                    articles.append({'title': title, 'link': href, 'vote': points})
    return story_sort(articles)


# sort scraped and "cleaned" articles for easier viewing
def story_sort(articles):
    return sorted(articles, key=lambda k: k['vote'], reverse=True)


pprint.pprint((clean_scraped_page()))
