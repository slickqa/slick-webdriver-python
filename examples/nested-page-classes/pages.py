__author__ = 'jcorbett'

from slickwd import Container, WebElementLocator, Find

class GoogleRootContainer(Container):
    """
    Root google page.  An instance is supposed to be created called Google.
    """

    def __init__(self, name):
        super(GoogleRootContainer, self).__init__(parent=None, name=name)
        self.Home = GoogleHomePage(self, "Home")
        self.SearchResults = GoogleSearchResultsPage(self, "SearchResults")


class GoogleHomePage(Container):
    """
    Google "Home" page, or www.google.com.
    """

    def __init__(self, parent, name):
        super(GoogleHomePage, self).__init__(parent=parent, name=name)
        self.Search_Query_Text_Field = WebElementLocator("Search Box", Find.by_name("q"), parent=self)
        self.Search_Button = WebElementLocator("Search Button", Find.by_name("btnG"), parent=self)

    def is_current_page(self, browser):
        return browser.exists(self.Search_Query_Text_Field, timeout=0, log=False)

class GoogleSearchResultsPage(Container):
    """
    A page with google search results.
    """

    def __init__(self, parent, name):
        super(GoogleSearchResultsPage, self).__init__(parent=parent, name=name)
        self.Results_Div = WebElementLocator("Results Div", Find.by_id("ires"), parent=self)

    def is_current_page(self, browser):
        return browser.exists(self.Results_Div, timeout=0, log=False)


Google = GoogleRootContainer("Google")
