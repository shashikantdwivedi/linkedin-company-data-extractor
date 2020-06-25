from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import re
import json
import pyfiglet


# Entry
print(pyfiglet.figlet_format("Welocme To"))
print(pyfiglet.figlet_format("LinkedIn Company Data Extractor"))

# Basic Inputs
keyword = input('Enter Keyworkd To Search - ').split(' ')
locations = input('Enter location - ')
keyword = '%20'.join(keyword)


# Initiate Chrome Driver
chromedriver = "chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


# Login Into LinkedIn Account
driver.get(
    "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")


driver.find_element_by_id("username").send_keys(os.environ['linkedinUsername'])
driver.find_element_by_id("password").send_keys(os.environ['linkedinPassword'])
driver.find_element_by_xpath(
    '//button[@data-litms-control-urn="login-submit"]').click()

page = 1
count = 0
page_read_count = 0
companies = []
page_visited = 0
already_visited = []

for x in range(page, 101):
    print('📃📃📃📃📃📃Opening Page Number - {}📃📃📃📃📃📃'.format(x))
    all_links = []
    all_fields = []
    driver.get(
        "https://www.linkedin.com/search/results/companies/?keywords={}%20&origin=SWITCH_SEARCH_VERTICAL&page={}".format(
            keyword, x))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_links = soup.findAll('a', {'class': 'search-result__result-link'})
    all_fields = soup.findAll('p', {'class': 'subline-level-1'})
    for k in range(0, len(all_links)):
        if all_links[k]['href'].split('/')[-2] in already_visited:
            print(all_links[k]['href'].split('/')[-2])
            continue
        else:
            already_visited.append(all_links[k]['href'].split('/')[-2])
        all_headers = []
        company_of_choice = False
        print(
            '⌨⌨⌨⌨⌨⌨Opening Company Page - {}⌨⌨⌨⌨⌨⌨'.format(all_links[k]['href'].split('/')[-2]))
        driver.get('https://www.linkedin.com{}'.format(all_links[k]['href']))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        all_headers = soup.findAll(
            'div', {'class': 'org-top-card-summary-info-list__info-item'})
        for z in all_headers:
            company_details = {}
            page_visited += 1
            if re.search(locations + '$', z.get_text().strip()):
                count += 1
                driver.get(
                    'https://www.linkedin.com{}about'.format(all_links[k]['href']))
                soup1 = BeautifulSoup(driver.page_source, 'html.parser')
                company_details['code'] = all_links[k]['href'].split('/')[-2]
                company_details['name'] = all_headers[0].get_text().strip()
                overview = soup1.find('p', {
                    'class': 'break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal'})
                if overview is not None:
                    company_details['overview'] = overview.get_text().strip()
                bold_fields = soup1.findAll('dt',
                                            {'class': 'org-page-details__definition-term t-14 t-black t-bold'})
                normal_fields = soup1.findAll('dd', {
                    'class': 'org-page-details__definition-text t-14 t-black--light t-normal'})
                company_size = soup1.find('dd', {
                    'class': 'org-about-company-module__company-size-definition-text t-14 t-black--light mb1 fl'})
                sal = 0
                for val in range(0, len(bold_fields)):
                    if bold_fields[val].get_text().strip() == 'Company size':
                        if company_size:
                            company_details['Company size'] = company_size.get_text(
                            ).strip()
                    else:
                        company_details[bold_fields[val].get_text(
                        ).strip()] = normal_fields[sal].get_text().strip()
                        sal += 1
                companies.append(company_details)
                with open('companies.json', 'w') as fp:
                    json.dump(companies, fp)

        page_read_count += 1
        print('💥💥💥💥💥💥Company Number - {}💥💥💥💥💥💥'.format(page_read_count))

