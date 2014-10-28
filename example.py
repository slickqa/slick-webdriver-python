#!vpy/bin/python

__author__ = 'jcorbett'

from slickwd import BrowserType, Browser, Container, WebElementLocator
from nose import with_setup
from nose.tools import assert_regexp_matches

# Page Classes --------------------------------------------------
class GoogleSearchPage(Container):
    Search_Query_Text_Field = WebElementLocator("Search Box", name="q")
    Search_Button = WebElementLocator("Search Button", id="gbqfba")

    def is_current_page(self, browser: Browser):
        return browser.exists(GoogleSearchPage.Search_Query_Text_Field)

class SearchResultsPage(Container):
    Results_Div = WebElementLocator("Results Div", id="ires")

    def is_current_page(self, browser: Browser):
        return browser.exists(SearchResultsPage.Results_Div)

# Tests ---------------------------------------------------------
browser = None

def setup():
    global browser
    if browser is not None:
        browser.quit()
    browser = Browser(BrowserType.PHANTOMJS)

@with_setup(setup)
def test_google_search():
    global browser
    browser.go_to('http://www.google.com')
    browser.wait_for_page(GoogleSearchPage)
    browser.click_and_type(GoogleSearchPage.Search_Query_Text_Field, "Slick Test Manager")
    browser.click(GoogleSearchPage.Search_Button)
    browser.wait_for_page(SearchResultsPage)
    assert_regexp_matches(browser.get_page_text(), '.*SlickQA:.*')
