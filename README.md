Webdriver wrapper for SlickQA Project
=====================================

Don't let the name fool you, this wrapper can be used by any project.  It was written by the people who brought you
the slick project, hence the name.  This wrapper has the purpose of making the selenium interface more reliable
for tests with less, more readable code by:

  * Wrapping all actions with log statements (using python's builtin logging framework) that detail everything it's doing
  * Providing a nice readable api, making your tests readable
  * Waiting for elements to exist (with customizable timeout) so that you don't have to
  * Providing a Page api that allows for easy organization of locators
  * Page api allows for flat (Page -> locator) and nested (FrameworkElement -> Page -> Container -> Locator) api
  * No need to instantiate every page class individually (that makes code look stupid)
  * Event based api where you can add your own pre and post actions as part of standard calls (like taking a screenshot on click)
  * more good tidbits


Example Usage
-------------

What does a test using this fabulous framework look like?  Let me show you:

    from slickwd import Browser, Container, WebElementLocator
    from nose import with_setup
    from nose.tools import assert_regexp_matches

    # Page Classes --------------------------------------------------
    class SearchPage(Container):
        Search_Query_Text_Field = WebElementLocator("Search Box", name="q")
        Search_Button = WebElementLocator("Search Button", id="gbqfba")

        def is_current_page(self, browser):
            return browser.exists(SearchPage.Search_Query_Text_Field)

    class SearchResultsPage(Container):
        Results_Div = WebElementLocator("Results Div", id="ires")

        def is_current_page(self, browser):
            return browser.exists(SearchResultsPage.Results_Div)

    # Tests ---------------------------------------------------------
    browser = None

    def setup():
        global browser
        if browser is not None:
            browser.quit()
        browser = Browser(Browser.CHROME)

    @with_setup(setup)    
    def test_google_search():
        global browser
        browser.go_to('http://www.google.com')
        browser.wait_for_page(SearchPage)
        browser.click_and_type(SearchPage.Search_Query_Text_Field, "Slick Test Manager")
        browser.click(SearchPage.Search_Button)
        browser.wait_for_page(SearchResultsPage)
        assert_regexp_matches(browser.get_page_text(), '.*SlickQA:.*')


The test is written so the code can be read, easily modified if something in the page is changed,
and allow for code reuse (page classes).  Normally page classes would be held in a different module
for better organization.  This is what is referred to in the documentation as the "static page class
model".  There is also a different way to structure page classes that allows for nesting of containers
(page classes) to make a hierarchy and enable code completion in IDEs.

