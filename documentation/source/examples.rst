Examples
========

.. toctree::
   :maxdepth: 2

Below you will find various examples.  These examples are explained here (in detail), but the source for them is 
available from `Github <https://github.com/slickqa/slick-webdriver-python/tree/master/examples>`_.

Simple Example
--------------

The following is the simple example, which is a python test (written using 
`nose <https://nose.readthedocs.org/en/latest/>`_).  The test in this example loads the google home page, 
and searches for *Slick Test Manager* and ensures a particular page is in the results::

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

This may seem like a lot, but normally the :doc:`page-classes` would be in a different module that you would import.
Let's start with the page classes and explain what they are here.


Nested Page Class Example
-------------------------

There are multiple files to analyze here so we will go through them one by one.  First our test, it's fairly simple.
