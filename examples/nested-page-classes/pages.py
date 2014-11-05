__author__ = 'jcorbett'

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
