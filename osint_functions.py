import requests
from bs4 import BeautifulSoup
import math
import re

def get_amount_of_stargazers(repo_url):
    req = requests.get(repo_url + "/stargazers")
    soup = BeautifulSoup(req.text, features="lxml")
    stargazer_links = soup.find_all("a", class_="js-selected-navigation-item selected tabnav-tab")

    new_soup = BeautifulSoup(str(stargazer_links[0]), features="lxml")
    spans = new_soup.find_all("span")
    followers = spans[0].text
    followers = followers.replace(",", "")


    return int(followers)


def find_accounts(repo_url, amnt_stargazers):
    pages = math.ceil(amnt_stargazers / 48)
    accounts = []
    c_page = 0
    while (c_page <= pages):
        req = requests.get(str(repo_url) + "/stargazers?page=" + str(c_page))

        soup = BeautifulSoup(req.text, features="lxml")
        for link in soup.find_all("a", attrs={"data-hovercard-type":True}):
            if (link.get("href") not in accounts):
                accounts.append(link.get('href'))
                print("Found Github Account: @" + link.get('href')[1:])
                yield link.get('href')
            


        c_page = c_page + 1



def find_emails(accounts):
    already_found = []
    for acc in accounts:
        req = requests.get("https://github.com" + acc)
        emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', req.text)

        if len(emails) > 0:
            if (emails[0] not in already_found):
                print("New email found:" + emails[0])
                already_found.append(emails[0])
                yield emails[0]
            else:
                print("No email found: @" + str(acc)[1:])
                yield

        else:
            print("No email found: @" + str(acc)[1:])
            yield
