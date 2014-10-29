#!vpy/bin/python

__author__ = 'jcorbett'

from slickwd import BrowserType, Browser, Container, WebElementLocator, Find
from nose import with_setup
from nose.tools import assert_regexp_matches

# Page Classes --------------------------------------------------
class GoogleSearchPage(Container):
    Search_Query_Text_Field = WebElementLocator("Search Box", Find.by_name("q"))
    Search_Button = WebElementLocator("Search Button", Find.by_name("btnG"))

    def is_current_page(self, browser):
        return browser.exists(GoogleSearchPage.Search_Query_Text_Field, timeout=0, log=False)

class SearchResultsPage(Container):
    Results_Div = WebElementLocator("Results Div", Find.by_id("ires"))

    def is_current_page(self, browser):
        return browser.exists(SearchResultsPage.Results_Div, timeout=0, log=False)

# Tests ---------------------------------------------------------
browser = None


def s():
    global browser
    if browser is not None:
        browser.quit()
    browser = Browser(BrowserType.FIREFOX)

def cleanup():
    global browser
    if browser is not None:
        browser.quit()

@with_setup(s, cleanup)
def test_google_search():
    global browser
    browser.go_to('http://www.google.com')
    browser.wait_for_page(GoogleSearchPage)
    browser.click_and_type(GoogleSearchPage.Search_Query_Text_Field, "Slick Test Manager")
    browser.click(GoogleSearchPage.Search_Button)
    browser.wait_for_page(SearchResultsPage)
    assert_regexp_matches(browser.get_page_text(), '.*SlickQA:.*')
