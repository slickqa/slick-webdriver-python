"""
"""

__author__ = 'jcorbett'

import logging
from enum import Enum
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import time


class BrowserType(Enum):
    """
    This enum is to help identify browsers to launch.  The values are the desired capabilities.  All
    values are static properties on the BrowserType class.

    Example Use::

        from slickwd import Browser, BrowserType

        browser = Browser(BrowserType.CHROME)

    """
    CHROME = (DesiredCapabilities.CHROME, webdriver.Chrome)
    """
    Chrome Browser (you must download
    `chromedriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_ separately and place in path)
    """
    FIREFOX = (DesiredCapabilities.FIREFOX, webdriver.Firefox)
    """Firefox Browser"""
    IE = (DesiredCapabilities.INTERNETEXPLORER, webdriver.Ie)
    """
    Internet Explorer Browser (you must download `internet explorer driver
    <https://code.google.com/p/selenium/wiki/InternetExplorerDriver>`_ separately and place it in your path)"""
    OPERA = (DesiredCapabilities.OPERA, webdriver.Opera)
    """Opera Browser"""
    SAFARI = (DesiredCapabilities.SAFARI, webdriver.Safari)
    """Safari Browser"""
    HTMLUNITWITHJS = (DesiredCapabilities.HTMLUNITWITHJS, None)
    """HTMLUnit with Javascript enabled, only for use with Remote"""
    IPHONE = (DesiredCapabilities.IPHONE, None)
    IPAD = (DesiredCapabilities.IPAD, None)
    ANDROID = (DesiredCapabilities.ANDROID, None)
    PHANTOMJS = (DesiredCapabilities.PHANTOMJS, webdriver.PhantomJS)
    """PhantomJS headless browser (must download separately, `phantomjs homepage <http://phantomjs.org/>`_)"""


class Find:
    """
    This is a factory to make it easy to create ways of finding elements.
    """

    def __init__(self, by, value):
        self.finders = [(by, value),]


    def describe(self):
        """Describe this finder (including any or'ed finders)"""
        return " or ".join([Find.describe_single_finder(finder[0], finder[1]) for finder in self.finders])

    @classmethod
    def describe_single_finder(cls, name, value):
        if name is By.ID:
            return "id \"{}\"".format(value)
        elif name is By.NAME:
            return "name \"{}\"".format(value)
        elif name is By.CLASS_NAME:
            return "class name \"{}\"".format(value)
        elif name is By.LINK_TEXT:
            return "link text \"{}\"".format(value)
        elif name is By.PARTIAL_LINK_TEXT:
            return "link text containing \"{}\"".format(value)
        elif name is By.CSS_SELECTOR:
            return "css selector \"{}\"".format(value)
        elif name is By.XPATH:
            return "xpath {}".format(value)
        elif name is By.TAG_NAME:
            return "tag name \"{}\"".format(value)

    def Or(self, finder):
        self.finders.extend(finder.finders)

    @classmethod
    def by_id(cls, id_value):
        return Find(By.ID, id_value)

    @classmethod
    def by_name(cls, name_value):
        return Find(By.NAME, name_value)

    @classmethod
    def by_class_name(cls, class_name_value):
        return Find(By.CLASS_NAME, class_name_value)

    @classmethod
    def by_link_text(cls, link_text_value):
        return Find(By.LINK_TEXT, link_text_value)

    @classmethod
    def by_partial_link_text(cls, partial_link_text_value):
        return Find(By.PARTIAL_LINK_TEXT, partial_link_text_value)

    @classmethod
    def by_css_selector(cls, css_selector_value):
        return Find(By.CSS_SELECTOR, css_selector_value)

    @classmethod
    def by_xpath(cls, xpath_value):
        return Find(By.XPATH, xpath_value)

    @classmethod
    def by_tag_name(cls, tag_name_value):
        return Find(By.TAG_NAME, tag_name_value)


class Timer:
    """A Timer tracks the start time (at creation) and will tell you if it is past the timeout value."""

    def __init__(self, length_in_seconds):
        self.start = time.time()
        self.end = self.start + length_in_seconds

    def is_past_timeout(self):
        return time.time() > self.end


class WebElementLocator:
    """
    """

    def __init__(self, name, finder):
        # id=None, xpath=None, link_text=None, partial_link_text=None, name=None, href=None,
        # tag_name=None, class_name=None, css_selector=None):
        self.name = name
        self.finder = finder
        self.description = "{} found by {}".format(name, finder.describe())
        self.logger = logging.getLogger("slickwd.WebElementLocator")

    def find_all_elements_matching(self, wd_browser, timeout, log=True):
        """Find any web elements matching any one of the finders.  This method returns a list."""

    def find_element_matching(self, wd_browser, timeout, log=True):
        """Find a single element matching the finder(s) that make up this locator."""
        if timeout == 0:
            if log:
                self.logger.debug("Attempting 1 time to find element {} .".format(self.describe()))
            for finder in self.finder.finders:
                try:
                    return wd_browser.find_element(finder[0], finder[1])
                except WebDriverException:
                    pass
            else:
                if log:
                    self.logger.warn("Unable to find element {}".format(self.describe()))
                return None
        else:
            retval = None
            timer = Timer(timeout)
            if log:
                self.logger.debug("Waiting for up to {:.2f} seconds for element {} to be available.".format(float(timeout), self.describe()))
            while not timer.is_past_timeout():
                for finder in self.finder.finders:
                    try:
                        retval =  wd_browser.find_element(finder[0], finder[1])
                    except WebDriverException:
                        pass
                    if retval is not None:
                        if log:
                            self.logger.info("Found element {} using locator property {} after {:.2f} seconds.".format(self.name, Find.describe_single_finder(finder[0], finder[1]), time.time() - timer.start))
                        return retval
                time.sleep(.25)

    def describe(self):
        """Describe the current element."""
        return self.description

class Browser:
    """
    The Browser is the primary interface you have to automate a browser.  An instance of Browser has the same
    methods no matter which browser it is you launch.  It also abstracts away the creation of remote browser
    instances when using `Selenium Grid <https://code.google.com/p/selenium/wiki/Grid2>`_ or `Selenium Server
    <http://selenium-python.readthedocs.org/en/latest/installation.html#downloading-selenium-server>`_.

    Most actions that the Browser has takes an argument called locator, which should be an instance of
    :class:`.WebElementLocator`.  These are normally arranged into Page classes to make them reusable
    by multiple tests / functions.  See :doc:`page-classes`.

    To create an instance of Browser, provide the browser type you would like, and the remote_url (if any)::

        from slickwd import Browser, BrowserType

        browser = Browser(BrowserType.PHANTOMJS)
        browser.go_to("http://www.google.com")

    For more examples, see :doc:`examples`.
    """

    def __init__(self, browser_type, remote_url=None, default_timeout=30):
        """
        Create a new browser session.  The only required parameter *browser_type* can be
        an instance of the *BrowserType* enum, a dictionary (like those from webdriver's desired_capabilities),
        or a string identifying the name of the browser (must correspond to a name in the *BrowserType* enum).

        If you use a remote_url, it should point to a selenium remote server.
        """
        self.default_timeout = default_timeout

        # tame the huge logs from webdriver
        wdlogger = logging.getLogger('selenium.webdriver')
        wdlogger.setLevel(logging.WARNING)

        self.logger = logging.getLogger("slickwd.Browser")
        browser_name = browser_type
        if isinstance(browser_type, BrowserType):
            browser_name = browser_type.name
        elif isinstance(browser_type, dict) and 'browserName' in browser_type:
            browser_name = browser_type[browser_name]
        self.logger.debug("New browser instance requested with browser_type={} and remote_url={}".format(repr(browser_name), repr(remote_url)))
        if isinstance(browser_type, str):
            try:
                browser_type = BrowserType[browser_type.upper()]
            except:
                raise WebDriverException("Invalid browser name: \"{}\"".format(browser_type))

        if remote_url is None:
            if isinstance(browser_type, dict) and 'browserName' in browser_type:
                browser_name = browser_type['browserName']
                if browser_name == 'internet explorer':
                    browser_name = 'ie'
                if browser_name == 'htmlunit':
                    browser_name = 'htmlunitwithjs'
                try:
                    browser_type = BrowserType[browser_name.upper()]
                except:
                    raise WebDriverException("Invalid browser: \"{}\"".format(browser_name))
            if not isinstance(browser_type, BrowserType):
                raise WebDriverException("Unable to create browser of type \"{}\"".format(repr(browser_type)))
            if browser_type.value[1] is None:
                raise WebDriverException("Browser of type \"{}\" can only be launched remotely, which means you must provide a remote_url.".format(browser_type.name))

            self.remote_url = remote_url
            self.browser_type = browser_type
            self.logger.info("Creating a new browser (locally connected) of type {}".format(browser_type.name.lower()))
            self.wd_instance = browser_type.value[1]()
        else:
            if isinstance(browser_type, BrowserType):
                browser_type = browser_type.value[0]

            if not isinstance(browser_type, dict):
                raise WebDriverException("Unable to create a browser of type \"{}\", when using remote_url browser_type should be either an instance of BrowserType or a dictionary containing desired capabilities.".format(repr(browser_type)))

            self.remote_url = remote_url
            self.browser_type = browser_type
            self.logger.info("Creating a new browser (through remote connection \"{}\") with desired capabilities of {}".format(remote_url, repr(browser_type)))
            self.wd_instance = webdriver.Remote(remote_url, browser_type)

    def quit(self, log=True):
        """Close the browser and quit the current session"""
        if log:
            self.logger.info("Calling quit on browser instance.")
        self.wd_instance.quit()
        return self

    def go_to(self, url, log=True):
        """Navigate the browser to the url provided"""
        if log:
            self.logger.debug("Navigating to url {}.".format(repr(url)))
        self.wd_instance.get(url)
        return self

    def wait_for_page(self, page, timeout=None, log=True):
        """
        Wait for a page class (container) to be present.
        This will cause that the page's *is_current_page* method to be called until it returns true or a timeout
        is reached.
        """
        # create an instance of the page
        page_instance = page()
        assert isinstance(page_instance, Container)

        if timeout is None:
            timeout = self.default_timeout

        if log:
            self.logger.debug("Waiting for up to {:.2f} seconds for page {} to be the current page.".format(float(timeout), page_instance.name()))

        timer = Timer(timeout)
        while not timer.is_past_timeout():
            if page_instance.is_current_page(self):
                break
            time.sleep(0.25) # sleep a quarter of a second
        else:
            # The timer.is_past_timeout() returned true and that kicked us out of the loop
            if log:
                self.logger.warn("Waited {:.2f} seconds for page {} to exist and it never returned true from is_current_page.".format(float(timeout), page_instance.name()))
            raise WebDriverException("Waited {:.2f} seconds for page {} to exist and it never returned true from is_current_page.".format(float(timeout), page_instance.name()))
        self.logger.debug("Found page {} after {:.2f} seconds.".format(page_instance.name(), time.time() - timer.start))
        return self

    def exists(self, locator, timeout=None, log=True):
        if timeout is None:
            timeout = self.default_timeout
        return locator.find_element_matching(self.wd_instance, timeout, log) is not None

    def click(self, locator, timeout=None, log=True):
        if timeout is None:
            timeout = self.default_timeout
        element = locator.find_element_matching(self.wd_instance, timeout, log)
        if element is None:
            raise WebDriverException("Unable to find element {} after waiting for {:.2f} seconds".format(locator.describe(), float(timeout)))
        if log:
            self.logger.debug("Clicking on element {}".format(locator.describe()))
        element.click()
        return self

    def click_and_type(self, locator, keys, timeout=None, log=True):
        if timeout is None:
            timeout = self.default_timeout
        element = locator.find_element_matching(self.wd_instance, timeout, log)
        if element is None:
            raise WebDriverException("Unable to find element {} after waiting for {:.2f} seconds".format(locator.describe(), float(timeout)))
        if log:
            self.logger.debug("Clicking on element {}".format(locator.describe()))
        element.click()
        if log:
            self.logger.debug("Typing \"{}\" into element {}".format(keys, locator.describe()))
        element.send_keys(keys)
        return self

    def get_page_text(self):
        element = self.wd_instance.find_element_by_tag_name("html")
        if element is not None:
            return element.text




class Container:
    """
    A generic container for structuring multiple *WebElementLocator* into groupings that help programmers find the right
    shared definition.
    """

    def name(self):
        name = self.__class__.__name__
        if name.endswith("Page"):
            name = name[:-4]
        return name

    def is_current_page(self, browser):
        raise NotImplementedError("is_current_page was not implemented on class: {}".format(self.__class__.__name__))



