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

Nested page classes can be nice for code completion (if you are using an editor or IDE with python code completion like
`PyCharm <https://www.jetbrains.com/pycharm/>`_), and it can improve your log output.  Below you'll see an example that
is very much like the above example (it does the same test), but with nested page classes stored in another python
file.  First the page classes (`pages.py <https://github.com/slickqa/slick-webdriver-python/blob/master/examples/nested-page-classes/pages.py>`_)::

    from slickwd import Container, WebElementLocator, Find

    class GoogleRootContainer(Container):
        """
        Root google page.  An instance is supposed to be created called Google.
        """

        def __init__(self, name):
            self.container_name = name
            self.Home = GoogleHomePage()
            self.SearchResults = GoogleSearchResultsPage()


    class GoogleHomePage(Container):
        """
        Google "Home" page, or www.google.com.
        """

        def __init__(self):
            self.Search_Query_Text_Field = WebElementLocator("Search Box", Find.by_name("q"))
            self.Search_Button = WebElementLocator("Search Button", Find.by_name("btnG"))

        def is_current_page(self, browser):
            return browser.exists(self.Search_Query_Text_Field, timeout=0, log=False)

    class GoogleSearchResultsPage(Container):
        """
        A page with google search results.
        """

        def __init__(self):
            self.Results_Div = WebElementLocator("Results Div", Find.by_id("ires"))

        def is_current_page(self, browser):
            return browser.exists(self.Results_Div, timeout=0, log=False)


    Google = GoogleRootContainer("Google")

And the tests (`searchtests.py <https://github.com/slickqa/slick-webdriver-python/blob/master/examples/nested-page-classes/searchtests.py>`_)::

    import sys
    import os

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

As mentioned above there are 2 primary advantages for the nested page classes: first code completion in a python IDE,
and second in the logs.  The logs are improved because every time you do an action such as clicking on an element, you
can see the hierarchy of page classes and what element a page is on.  This doesn't happen with the static layout.

Here is an example of the output you would get from the logs::

    slickwd.Browser: DEBUG: New browser instance requested with browser_type='PHANTOMJS' and remote_url=None
    slickwd.Browser: INFO: Creating a new browser (locally connected) of type phantomjs
    slickwd.Browser: DEBUG: Navigating to url 'http://www.google.com'.
    slickwd.Browser: DEBUG: Waiting for up to 30.00 seconds for page Google.Home to be the current page.
    slickwd.Browser: DEBUG: Found page Google.Home after 0.01 seconds.
    slickwd.WebElementLocator: DEBUG: Waiting for up to 30.00 seconds for element Search Box on page Google.Home found by name "q" to be available.
    slickwd.WebElementLocator: INFO: Found element Search Box using locator property name "q" after 0.01 seconds.
    slickwd.Browser: DEBUG: Clicking on element Search Box on page Google.Home found by name "q"
    slickwd.Browser: DEBUG: Typing "Slick Test Manager" into element Search Box on page Google.Home found by name "q"
    slickwd.WebElementLocator: DEBUG: Waiting for up to 30.00 seconds for element Search Button on page Google.Home found by name "btnG" to be available.
    slickwd.WebElementLocator: INFO: Found element Search Button using locator property name "btnG" after 0.01 seconds.
    slickwd.Browser: DEBUG: Clicking on element Search Button on page Google.Home found by name "btnG"
    slickwd.Browser: DEBUG: Waiting for up to 30.00 seconds for page Google.SearchResults to be the current page.
    slickwd.Browser: DEBUG: Found page Google.SearchResults after 0.01 seconds.
    slickwd.Browser: INFO: Calling quit on browser instance.

Notice each element knows what page it is on in the code, and each page knows it's *parent* in the hierarchy.  This
can help greatly when comparing code and logs, as well as navigating code.
