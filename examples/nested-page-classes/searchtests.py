__author__ = 'jcorbett'

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from slickwd import BrowserType, Browser
from pages import Google
from nose import with_setup
from nose.tools import assert_regexp_matches


browser = None


def s():
    global browser
    if browser is not None:
        browser.quit()
    browser = Browser(BrowserType.PHANTOMJS)

def cleanup():
    global browser
    if browser is not None:
        browser.quit()

@with_setup(s, cleanup)
def test_google_search():
    global browser
    browser.go_to('http://www.google.com')
    browser.wait_for_page(Google.Home)
    browser.click_and_type(Google.Home.Search_Query_Text_Field, "Slick Test Manager")
    browser.click(Google.Home.Search_Button)
    browser.wait_for_page(Google.SearchResults)
    assert_regexp_matches(browser.get_page_text(), '.*SlickQA:.*')