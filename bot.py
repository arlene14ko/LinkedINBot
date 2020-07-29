import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class LinkedINBot:
    
    #calling chromedriver
    def __init__(self, username, password):
        self.driver = webdriver.Chrome('./chromedriver.exe')

        self.base_url = 'https://www.linkedin.com'
        self.login_url = self.base_url + '/login'
        self.feed_url = self.base_url + '/feed'
        self.search_people_url = self.base_url + '/search/results/people/?keywords={}'

        self.username = username
        self.password = password

    #navigate
    def _nav(self, url):
        self.driver.get(url)
        time.sleep(3)

    #logging in to linkedin
    def login(self, username, password):
        self._nav(self.login_url)
        self.driver.find_element_by_id('username').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Sign in')]").click()

    #making a post
    def post(self, text):
        self.driver.find_element_by_class_name('share-box__open').click()
        self.driver.find_element_by_class_name('mentions-texteditor__content').send_keys(text)
        self.driver.find_element_by_class_name('share-actions__primary-action').click()
    
    #search option
    def search_people(self, text, connect=False):
        self._nav(self.search_people_url.format(text))

        #search = self.driver.find_element_by_class_name('search-global-typeahead__input')
        #search.send_keys(text)
        #search.send_keys(Keys.ENTER)
        
        #waiting to load
        time.sleep(3)

        if connect:
            self._search_connect()

    #sending connections
    def _search_connect(self):
        connect_btn = self.driver.find_element_by_class_name('search-result__action-button')
        connect_btn.click()
        time.sleep(4)

        connect_option =  self.driver.find_element_by_class_name('ml1')
        connect_option.click()

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('./config.ini')

    username = config['CREDS']['username']
    password = config['CREDS']['password']
    post_text = config['CREDS']['post']
    search_text = config['CREDS']['search']

    bot = LinkedINBot(username, password)
    bot.login(username, password)
    bot.post(post_text)
    bot.search(search_text, connect=True)
