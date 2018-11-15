"""
"""

import logging
from enum import Enum
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select
from selenium import webdriver
import appium
from appium.webdriver.common.mobileby import MobileBy

from pydispatch import dispatcher
import time

__author__ = 'Jason Corbett'


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


class Find(object):
    """
    Use the class methods on this class to create instances, which are used by the WebElementLocator class
    to find elements in a browser.

    Example Usage::

        Search_Query_Text_Field = WebElementLocator("Search Box", Find.by_name("q"))

    This would create an instance of WebElementLocator called Search_Query_Text_Field that can be found
    on the page by looking for an element with the name property set to *q*.
    """

    def __init__(self, by, value):
        self.finders = [(by, value), ]
        self._and = False

    def describe(self):
        """Describe this finder in a plain english sort of way.  This allows for better logging.
        Example output would be "name q" for `Find.by_name("q")`."""
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
        elif name is MobileBy.ANDROID_UIAUTOMATOR:
            return "android ui automator \"{}\"".format(value)
        elif name is MobileBy.ACCESSIBILITY_ID:
            return "accessibility id \"{}\"".format(value)
        elif name is MobileBy.IOS_PREDICATE:
            return "ios predicate string \"{}\"".format(value)
        elif name is MobileBy.IOS_UIAUTOMATION:
            return "ios uiautomation \"{}\"".format(value)

    def Or(self, finder):
        """
        You can _or_ multiple finders together by using the Or method.  An example would be::

            Search_Query_Text_Field = WebElementLocator("Search Box", Find.by_name("q").Or(Find.by_id("q")))

        The framework iterates over the list of finders and returns the first element found.

        :param finder: Another finder to consider when looking for the element.
        :type finder: :class:`.Find`
        :return: This same instance of Find with the other finder included.
        :rtype: :class:`.Find`
        """
        self._and = False
        self.finders.extend(finder.finders)
        return self

    def allow_multiple_finds(self):
        return self._and

    def And(self, finder):
        """
        You can _and_ multiple finders together by using the And method.  An example would be::

            Search_Query_Text_Field = WebElementLocator("Search Box", Find.by_name("q").And(Find.by_id("q")))

        The framework iterates over the list of finders and returns the results.

        :param finder: Another finder to consider when looking for the element.
        :type finder: :class:`.Find`
        :return: This same instance of Find with the other finder included.
        :rtype: :class:`.Find`
        """
        self._and = True
        self.finders.extend(finder.finders)
        return self

    @classmethod
    def by_id(cls, id_value):
        """
        Find a web element using the element's _id_ attribute.

        :param id_value: the id of the web element you are looking for
        :type id_value: str
        :return: an instance of Find that uses the id as the way to find the element.
        :rtype: :class:`.Find`
        """
        return Find(By.ID, id_value)

    @classmethod
    def by_name(cls, name_value):
        """
        Find a web element using the element's _name_ attribute.

        :param name_value: the value of the name attribute of the web element you are looking for
        :type name_value: str
        :return: an instance of Find that uses the name attribute as the way to find the element.
        :rtype: :class:`.Find`
        """
        return Find(By.NAME, name_value)

    @classmethod
    def by_class_name(cls, class_name_value):
        """
        Find a web element by looking for one that uses a particular css class name.

        :param class_name_value: the name of one of the css classes of the web element you are looking for
        :type class_name_value: str
        :return: an instance of Find that uses it's css classes as the way to find the element.
        :rtype: :class:`.Find`
        """
        return Find(By.CLASS_NAME, class_name_value)

    @classmethod
    def by_link_text(cls, link_text_value):
        """
        Find a web element (a link or <a> tag) using the element's exact link text.

        :param link_text_value: the value of the link's inner text
        :type link_text_value: str
        :return: an instance of Find that uses the link's text as the way to find the element.
        :rtype: :class:`.Find`
        """
        return Find(By.LINK_TEXT, link_text_value)

    @classmethod
    def by_partial_link_text(cls, partial_link_text_value):
        """
        Find a web element (a link or <a> tag) using part of the element's link text.

        :param partial_link_text_value: a subset of the value of the link's inner text
        :type partial_link_text_value: str
        :return: an instance of Find that uses part of the link's text as the way to find the element.
        :rtype: :class:`.Find`
        """
        return Find(By.PARTIAL_LINK_TEXT, partial_link_text_value)

    @classmethod
    def by_css_selector(cls, css_selector_value):
        """
        Find a web element by using a css selector

        :param css_selector_value: the css selector that will identify the element
        :type css_selector_value: str
        :return: an instance of Find that uses a css selector to find the element
        :rtype: :class:`.Find`
        """
        return Find(By.CSS_SELECTOR, css_selector_value)

    @classmethod
    def by_xpath(cls, xpath_value):
        """
        Find a web element by using a xpath.

        :param xpath_value: the xpath expression that will identify the element
        :type xpath_value: str
        :return: an instance of Find that uses an xpath expression to find the element
        :rtype: :class:`.Find`
        """
        return Find(By.XPATH, xpath_value)

    @classmethod
    def by_tag_name(cls, tag_name_value):
        """
        Find an element using it's tag name.  This is more useful when trying to find multiple elements.

        :param tag_name_value: the name of the html tag for the element or elements your are looking for
        :type tag_name_value: str
        :return: an instance of Find that looks for all elements on a page with a particular tag name
        :rtype: :class:`.Find`
        """
        return Find(By.TAG_NAME, tag_name_value)

    @classmethod
    def by_android_uiautomator(cls, uiautomator_value):
        """
        Find a mobile element using an android UI Automator locator.  Only valid on android.

        :param uiautomator_value: The UI Automator to search for
        :type uiautomator_value: str
        :return: an instance of Find that looks for the UI Automator on the mobile device
        :rtype: :class:`.Find`
        """
        return Find(MobileBy.ANDROID_UIAUTOMATOR, uiautomator_value)

    @classmethod
    def by_accessibility_id(cls, accessibility_id):
        """
        Find a mobile element using an accessibility id. Only valid on mobile.

        :param accessibility_id: The accessibility id to look for on the mobile device.
        :type accessibility_id: str
        :return: an instance of Find the looks for the element matching the accessibility id
        :rtype: :class:`.Find`
        """
        return Find(MobileBy.ACCESSIBILITY_ID, accessibility_id)

    @classmethod
    def by_ios_predicate(cls, predicate_value):
        """
        Find a mobile element using an predicate locator.  Only valid on iOS.
        https://github.com/appium/python-client/blob/master/test/functional/ios/find_by_ios_predicate_tests.py

        :param predicate_value: The predicate to search for
        :type predicate_value: str
        :return: an instance of Find that looks for the predicate on the mobile device
        :rtype: :class:`.Find`
        """
        return Find(MobileBy.IOS_PREDICATE, predicate_value)

    @classmethod
    def by_ios_uiautomation(cls, uiautomation_value):
        """
        Find a mobile element using an uiautomation locator.  Only valid on iOS.

        :param uiautomation_value: The predicate to search for
        :type uiautomation_value: str
        :return: an instance of Find that looks for the uiautomation on the mobile device
        :rtype: :class:`.Find`
        """
        return Find(MobileBy.IOS_PREDICATE, uiautomation_value)


# there is no doc because this is not intended to be used externally (not that it can't be)
class Timer(object):
    def __init__(self, length_in_seconds):
        self.start = time.time()
        self.end = self.start + length_in_seconds

    def is_past_timeout(self):
        return time.time() > self.end


class WebElementLocator(object):
    """
    A WebElementLocator represents information about an element you are trying to find.  It has a name field for
    nice logging, and a finder field (should be of type :class:`.Find`).

    See :doc:`locators`
    """

    WAIT_FOR_ANGULAR_JS = """
    var rootSelector = ["[ng-app]","[data-ng-app]","body"];
    var callback = arguments[arguments.length - 1];
    var el = document.querySelector(rootSelector);
    try {
        if (angular.getTestability) {
            angular.getTestability(el).whenStable(callback);
        } else {
            angular.element(el).injector().get('$browser').
                    notifyWhenNoOutstandingRequests(callback);
        }
    } catch (e) {
        callback(e);
    }
    """

    def __init__(self, name, finder):
        # id=None, xpath=None, link_text=None, partial_link_text=None, name=None, href=None,
        # tag_name=None, class_name=None, css_selector=None):
        self.name = name
        self.finder = finder
        self.logger = logging.getLogger("slickwd.WebElementLocator")
        self.parent = None
        self.parent_initialized = False
        self.description = "{} found by {}".format(name, finder.describe())

    def get_page_name(self):
        if self.parent is not None:
            return self.parent.get_name()

    def find_all_elements_matching(self, wd_browser, timeout=None, log=True, angular=False, retry_interval=.25):
        """
        Find a list of elements that match a finder.  This method can be useful if you are
        :doc:`raw-webdriver` and need to select from and inspect a list of elements.

        There is no timeout because it will return an empty list if no matching elements are found.

        :param wd_browser: The raw selenium webdriver driver instance.
        :param timeout: the max time (in seconds) to wait before giving up on finding the element
        :type timeout: int or float (use float for sub-second precision)
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: list of matching elements
        :rtype: list of web element
        """
        if angular:
            for i in range(3):
                try:
                    wd_browser.execute_async_script(WebElementLocator.WAIT_FOR_ANGULAR_JS)
                    break
                except:
                    time.sleep(.2)
        retval = []
        if timeout == 0:
            if log:
                self.logger.debug("Looking for a list of elements matching {}".format(self.describe()))
            for finder in self.finder.finders:
                try:
                    elements = wd_browser.find_elements(finder[0], finder[1])
                    if not self.finder.allow_multiple_finds():
                        if elements:
                            retval = elements
                            break
                    else:
                        retval.extend(elements)

                except WebDriverException:
                    pass
            if log:
                self.logger.info("Found {} elements matching {}".format(len(retval), self.describe()))

            return retval
        else:
            timer = Timer(timeout)
            if log:
                self.logger.debug(
                    "Waiting for up to {:.2f} seconds for element {} to be available.".format(float(timeout), self.describe()))

            while not timer.is_past_timeout():
                for finder in self.finder.finders:
                    try:
                        elements = wd_browser.find_elements(finder[0], finder[1])
                        if not self.finder.allow_multiple_finds():
                            if elements:
                                retval = elements
                                break
                        else:
                            retval.extend(elements)

                    except WebDriverException:
                        pass

                if len(retval) > 0:
                    if log:
                        self.logger.debug("Found {} elements matching {}".format(len(retval), self.describe()))
                    return retval

                time.sleep(retry_interval)

            if log:
                self.logger.debug("Found {} elements matching {}".format(len(retval), self.describe()))

            return retval

    def find_element_matching(self, wd_browser, timeout=None, log=True, angular=False, retry_interval=.25):
        """
        Find a single element matching the finder(s) that make up this locator before a timeout is reached.
        This method is used internally by the framework when you call any action on a WebElementLocator, however
        like is mentioned in :doc:`raw-webdriver` you can use this method to help you get the raw webelements from
        webdriver for your own use.

        :param wd_browser: The selenium driver (webdriver) instance to use.
        :param timeout: the max time (in seconds) to wait before giving up on finding the element
        :type timeout: int or float (use float for sub-second precision)
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: a raw webdriver webelement type on success, None on failure
        """
        if timeout is None:
            timeout = 0

        if angular:
            for i in range(3):
                try:
                    wd_browser.execute_async_script(WebElementLocator.WAIT_FOR_ANGULAR_JS)
                    break
                except:
                    time.sleep(.2)

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
            timer = Timer(timeout)
            if log:
                self.logger.debug(
                    "Waiting for up to {:.2f} seconds for element {} to be available.".format(float(timeout), self.describe()))

            while not timer.is_past_timeout():
                for finder in self.finder.finders:
                    retval = None
                    try:
                        retval = wd_browser.find_element(finder[0], finder[1])
                    except WebDriverException:
                        pass

                    if retval is not None:
                        if log:
                            self.logger.info(
                                "Found element {} using locator property {} after {:.2f} seconds.".format(self.name,
                                                                                                          Find.describe_single_finder(
                                                                                                              finder[0],
                                                                                                              finder[
                                                                                                                  1]),
                                                                                                          time.time() - timer.start))
                        return retval
                time.sleep(.25)

    def find_all_elements_from_parent_element(self, parent_element, wd_browser, timeout=None, log=True, angular=False, retry_interval=.25):
        """
        Find all elements starting from a parent element
        :param parent_element:
        :param wd_browser:
        :param timeout:
        :param log:
        :param angular:
        :param retry_interval:
        :return: list of web element
        """
        if timeout is None:
            timeout = 0

        if angular:
            for i in range(3):
                try:
                    wd_browser.execute_async_script(WebElementLocator.WAIT_FOR_ANGULAR_JS)
                    break
                except:
                    time.sleep(.2)

        retval = []
        if timeout == 0:
            try:
                if log:
                    self.logger.debug("Looking for a list of elements matching: {}".format(self.describe()))

                for finder in self.finder.finders:
                    elements = parent_element.find_elements(by=finder[0], value=finder[1])
                    if not self.finder.allow_multiple_finds():
                        if elements:
                            retval = elements
                            break
                    else:
                        retval.extend(elements)

            except WebDriverException:
                pass

            if log:
                self.logger.debug("Found {} elements matching {}".format(len(retval), self.describe()))

            return retval

        else:
            timer = Timer(timeout)
            if log:
                self.logger.debug(
                    "Waiting for up to {:.2f} seconds for element {} to be available.".format(float(timeout), self.describe()))

            while not timer.is_past_timeout():
                try:
                    if log:
                        self.logger.debug("Looking for a list of elements matching: {}".format(self.describe()))

                    for finder in self.finder.finders:
                        elements = parent_element.find_elements(by=finder[0], value=finder[1])
                        if not self.finder.allow_multiple_finds():
                            if elements:
                                retval = elements
                                break
                        else:
                            retval.extend(elements)

                except WebDriverException:
                    pass

                if len(retval) > 0:
                    if log:
                        self.logger.debug("Found {} elements matching {}".format(len(retval), self.describe()))
                    return retval

                time.sleep(retry_interval)

    def describe(self):
        """
        Describe the current locator in plain english.  Used for logging.

        :return: description of element locator including name and how it is looking for it
        :rtype: str
        """
        if self.parent is not None and self.parent_initialized is False:
            self.description = "{} on page {} found by {}".format(self.name, self.parent.get_name(),
                                                                  self.finder.describe())
            self.parent_initialized = True
        return self.description


class Browser(object):
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

    SIGNAL_BEFORE_CLICK = "slickwd.Browser.signal-before-click"

    ANGULAR_EXISTS_JS = """
    var attempts = 3;
    var asyncCallback = arguments[arguments.length - 1];
    var callback = function(args) {
        setTimeout(function() {
            asyncCallback(args);
        }, 0);
    };
    var check = function(n) {
        try {
            if (window.angular) {
                callback([true, null]);
            } else if (n < 1) {
                callback([false, 'retries looking for angular exceeded']);
            } else {
                window.setTimeout(function() {check(n - 1);}, 1000);
            }
        } catch (e) {
            callback([false, e]);
        }
    };
    check(attempts);
    """

    def __init__(self, browser_type, remote_url=None, default_timeout=30):
        """
        Create a new browser session.  The only required parameter *browser_type* can be
        an instance of the *BrowserType* enum, a dictionary (like those from webdriver's desired_capabilities),
        or a string identifying the name of the browser (must correspond to a name in the *BrowserType* enum).

        If you use a remote_url, it should point to a selenium remote server.
        """
        self.default_timeout = default_timeout
        self.angular_mode = False

        # tame the huge logs from webdriver
        wdlogger = logging.getLogger('selenium.webdriver')
        wdlogger.setLevel(logging.WARNING)

        self.logger = logging.getLogger("slickwd.Browser")
        browser_name = browser_type
        if isinstance(browser_type, BrowserType):
            browser_name = browser_type.name
        elif isinstance(browser_type, dict) and 'browserName' in browser_type:
            browser_name = browser_type[browser_name]
        self.logger.debug(
            "New browser instance requested with browser_type={} and remote_url={}".format(repr(browser_name),
                                                                                           repr(remote_url)))
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
                raise WebDriverException(
                    "Browser of type \"{}\" can only be launched remotely, which means you must provide a remote_url.".format(
                        browser_type.name))

            self.remote_url = remote_url
            self.browser_type = browser_type
            self.logger.info("Creating a new browser (locally connected) of type {}".format(browser_type.name.lower()))
            self.wd_instance = browser_type.value[1]()
            ''':type: appium.webdriver.Remote'''
            self.wd_instance.set_script_timeout(15)
        else:
            if isinstance(browser_type, BrowserType):
                browser_type = browser_type.value[0]

            if not isinstance(browser_type, dict):
                raise WebDriverException(
                    "Unable to create a browser of type \"{}\", when using remote_url browser_type should be either an instance of BrowserType or a dictionary containing desired capabilities.".format(
                        repr(browser_type)))

            self.remote_url = remote_url
            self.browser_type = browser_type
            self.logger.info(
                "Creating a new browser (through remote connection \"{}\") with desired capabilities of {}".format(
                    remote_url, repr(browser_type)))
            if 'platformName' in browser_type and browser_type['platformName'] in ['Android', 'iOS']:
                self.wd_instance = appium.webdriver.Remote(remote_url, browser_type)
                ''':type: appium.webdriver.Remote'''
            else:
                self.wd_instance = webdriver.Remote(remote_url, browser_type)
                ''':type: appium.webdriver.Remote'''
                self.wd_instance.set_script_timeout(10)

    def quit(self, log=True):
        """
        Close the browser and quit the current session

        :return: this instance for chaining of methods
        :rtype: :class:`.Browser`
        """
        if log:
            self.logger.info("Calling quit on browser instance.")
        self.wd_instance.quit()
        return self

    def go_to(self, url, log=True, test_for_angular=False):
        """Navigate the browser to the url provided"""
        if log:
            self.logger.debug("Navigating to url {}.".format(repr(url)))
        self.wd_instance.get(url)
        if test_for_angular:
            self.angular_mode = self.wd_instance.execute_async_script(Browser.ANGULAR_EXISTS_JS)[0]
        else:
            self.angular_mode = False
        return self

    def wait_for_page(self, page, timeout=None, log=True):
        """
        Wait for a page class (container) to be present.
        This will cause that the page's *is_current_page* method to be called until it returns true or a timeout
        is reached.

        :param page: The page class (container) to wait for it's is_current_page to return True
        :type page: :class:`.Container`
        :param timeout: the max time (in seconds) to wait before giving up on the page existing
        :type timeout: int or float (use float for sub-second precision)
        :param log: Should the activities of this method be logged, default is True
        :type log: bool
        :return: this instance for chaining of methods
        :rtype: :class:`.Browser`
        """
        # create an instance of the page
        page_instance = None
        if isinstance(page, Container):
            page_instance = page
        else:
            page_instance = page()
        assert isinstance(page_instance, Container)

        if timeout is None:
            timeout = self.default_timeout

        if log:
            self.logger.debug(
                "Waiting for up to {:.2f} seconds for page {} to be the current page.".format(float(timeout),
                                                                                              page_instance.get_name()))

        timer = Timer(timeout)
        while not timer.is_past_timeout():
            if page_instance.is_current_page(self):
                break
            time.sleep(0.25)  # sleep a quarter of a second
        else:
            # The timer.is_past_timeout() returned true and that kicked us out of the loop
            if log:
                self.logger.warn(
                    "Waited {:.2f} seconds for page {} to exist and it never returned true from is_current_page.".format(
                        float(timeout), page_instance.get_name()))
            raise WebDriverException(
                "Waited {:.2f} seconds for page {} to exist and it never returned true from is_current_page.".format(
                    float(timeout), page_instance.get_name()))
        self.logger.debug(
            "Found page {} after {:.2f} seconds.".format(page_instance.get_name(), time.time() - timer.start))
        return self

    def exists(self, locator, timeout=None, log=True):
        """
        Check to see if an element exists on a page.  You can control how long to wait, and if the method should do
        any logging.  If you specify 0 for the timeout, the framework will only look for the element once.

        :param locator: the locator to look for (usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before returning False
        :type timeout: int or float
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: True if an element was found in the time specified
        :rtype: bool
        """
        if timeout is None:
            timeout = self.default_timeout
        return locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode) is not None

    def is_displayed(self, locator, timeout=None, log=True):
        """
        Check to see if an element is displayed on a page.  You can control how long to wait, and if the method should do
        any logging.  If you specify 0 for the timeout, the framework will only look for the element once.

        :param locator: the locator to look for (usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before returning False
        :type timeout: int or float
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: True if an element was found in the time specified
        :rtype: bool
        """
        if timeout is None:
            timeout = self.default_timeout
        self.logger.info("Checking if element: {} is displayed".format(locator.describe()))
        element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        if element is None:
            raise WebDriverException(
                "Unable to find element {} after waiting for {} seconds".format(locator.describe(), timeout))
        return element.is_displayed()

    def is_enabled(self, locator, timeout=None, log=True):
        """
        Check to see if an element is enabled.  You can control how long to wait, and if the method should do
        any logging.  If you specify 0 for the timeout, the framework will only look for the element once.

        :param locator: the locator to look for (usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before returning False
        :type timeout: int or float
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: True if an element was enabled
        :rtype: bool
        """
        if timeout is None:
            timeout = self.default_timeout
        self.logger.info("Checking if element: {} is enabled".format(locator.describe()))
        element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        if element is None:
            raise WebDriverException(
                "Unable to find element {} after waiting for {} seconds".format(locator.describe(), timeout))
        return element.is_enabled()

    def is_selected(self, locator, timeout=None, log=True):
        """
        Check to see if an element is selected.  You can control how long to wait, and if the method should do
        any logging.  If you specify 0 for the timeout, the framework will only look for the element once.

        :param locator: the locator to look for (usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before returning False
        :type timeout: int or float
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: True if an element was selected
        :rtype: bool
        """
        if timeout is None:
            timeout = self.default_timeout
        self.logger.info("Checking if element: {} is selected".format(locator.describe()))
        element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        if element is None:
            raise WebDriverException(
                "Unable to find element {} after waiting for {} seconds".format(locator.describe(), timeout))
        return element.is_selected()

    def wait_for_not_exist(self, locator, timeout=None, log=True):
        """
        Wait for an element not to exist on a page.  You can control how long to wait, and if the method should do
        any logging.

        :param locator: the locator to check if exists(usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before returning
        :type timeout: int or float
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        """
        if timeout is None:
            timeout = self.default_timeout
        timer = Timer(timeout)
        while not timer.is_past_timeout():
            if locator.find_element_matching(self.wd_instance, 0, log, self.angular_mode) is None:
                self.logger.info(
                    "Element {} no longer exists.  wait_for_not_exist has completed.".format(locator.describe()))
                return
            else:
                time.sleep(.25)
        raise Exception(
            "Element {} still existed after waiting for {:.2f} seconds".format(locator.describe(), float(timeout)))

    def _internal_raw_click(self, element):
        """
        A private internal method for
        """
        # This beauty comes courtesy of comment #85 on https://code.google.com/p/selenium/issues/detail?id=2766
        # as of 10/30/2017 this doesn't seem to work, and the normal way works
        #if (isinstance(self.browser_type, BrowserType) and self.browser_type is BrowserType.CHROME) or (
        #    isinstance(self.browser_type, dict) and 'browserName' in self.browser_type and self.browser_type['browserName'] == 'chrome'):
        #    self.wd_instance.execute_script("arguments[0].click();", element)
        #else:
        element.click()

    def _internal_click(self, locator, timeout, log, signal=False):
        """
        A private internal method for finding an element and clicking it.  The raw element is returned.
        """
        if timeout is None:
            timeout = self.default_timeout
        timer = Timer(timeout)
        element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        if element is None:
            raise WebDriverException(
                "Unable to find element {} after waiting for {:.2f} seconds".format(locator.describe(), float(timeout)))
        while not timer.is_past_timeout():
            if element.is_displayed() and element.is_enabled():
                break
            try:
                self.wd_instance.execute_script("arguments[0].scrollIntoView(true);", element)
            except:
                pass
            time.sleep(.25)
            element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        if log:
            self.logger.debug("Clicking on element {}".format(locator.describe()))
        if signal:
            dispatcher.send(signal=Browser.SIGNAL_BEFORE_CLICK, sender=self, locator=locator)

        self._internal_raw_click(element)
        return element

    def _internal_wait_for_changes_to_stop(self, locator, locate_timeout=None, change_timeout=10, log=True):
        """
        Internal method, do not call unless you know what you are doing.  This method waits for changes to an element
        (number of sub elements, text property) to stop changing for a period of time.

        :param locator:
        :param locate_timeout:
        :param change_timeout:
        :param log:
        :return:
        """
        if locate_timeout is None:
            locate_timeout = self.default_timeout
        element = locator.find_element_matching(self.wd_instance, locate_timeout, log, self.angular_mode)
        if log:
            self.logger.debug("Performing checks to make sure that {} is done changing.".format(locator.describe()))
        last_number_of_sub_elements = len(element.find_elements_by_xpath('.//*'))
        last_text = element.text
        timer = Timer(change_timeout)
        number_of_times_with_no_changes = 0
        while not timer.is_past_timeout():
            time.sleep(.1)
            element = locator.find_element_matching(self.wd_instance, self.default_timeout, False, self.angular_mode)
            if element is not None:
                current_number_of_sub_elements = len(element.find_elements_by_xpath('.//*'))
                current_text = element.text
                if current_number_of_sub_elements == last_number_of_sub_elements and current_text == last_text:
                    number_of_times_with_no_changes += 1
                    if number_of_times_with_no_changes > 2:
                        break
                else:
                    number_of_times_with_no_changes = 0
                last_number_of_sub_elements = current_number_of_sub_elements
                last_text = current_text
        else:
            if log:
                self.logger.warn("Waited 10 seconds for {} to stop changing, but it seems to still be changing".format(
                    locator.describe()))
        return element

    def click(self, locator, timeout=None, log=True):
        """
        Click on an element using the mouse.

        :param locator: the locator that specifies which element to click on (usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before throwing a not found exception
        :type timeout: int or float (float for sub-second precision)
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: The reference to this Browser instance.
        :rtype: :class:`.Browser`
        """
        self._internal_click(locator, timeout, log, signal=True)
        return self

    def move_to_and_click(self, locator, timeout=None, log=True):
        """
        Move to an element (mouse) and then click it.
        :param locator: the locator that specifies which element to click on (usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before throwing a not found exception
        :type timeout: int or float (float for sub-second precision)
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: The reference to this Browser instance.
        :rtype: :class:`.Browser`
        """
        if timeout is None:
            timeout = self.default_timeout
        element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        action = ActionChains(self.wd_instance)
        if log:
            self.logger.info("Moving to element {} and clicking it.".format(locator.describe()))
        action.move_to_element(element).click(element).perform()
        return self

    def set_checkbox_state(self, locator, checked=None, timeout=None, log=True):
        """
        Sets the state of a checkbox input type regardless of the current state.  You can control how long to wait, and if the method should do
        any logging.  If you specify 0 for the timeout, the framework will only look for the element once.

        :param locator: the locator to look for (usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param checked: True if you want the checkbox checked
        :type checked: bool
        :param timeout: The amount of time (in seconds) to look before returning False
        :type timeout: int or float
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        """
        if timeout is None:
            timeout = self.default_timeout
        timer = Timer(timeout)
        while not timer.is_past_timeout():
            element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
            if element.is_selected() and not checked:
                self._internal_click(locator, timeout=1, log=log)
                return self
            if not element.is_selected() and checked:
                self._internal_click(locator, timeout=1, log=log)
        return self

    def get_checkbox_state(self, locator, timeout=None, log=True):
        """
        Gets the state of a checkbox input type.  You can control how long to wait, and if the method should do
        any logging.  If you specify 0 for the timeout, the framework will only look for the element once.

        :param locator: the locator to look for (usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before returning False
        :type timeout: int or float
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :rtype bool
        """
        if timeout is None:
            timeout = self.default_timeout
        element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        return element.is_selected()

    def click_and_type(self, locator, keys, timeout=None, log=True):
        """
        Deprecated, just use type.
        """
        element = self._internal_click(locator, timeout, log, signal=True)
        for i in range(3):
            try:
                element.send_keys(keys)
                break
            except:
                element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        else:
            raise WebDriverException("Unable to find element {} not found.".format(locator.name))
        return self

    def type(self, locator, keys, timeout=None, log=True, clear=True, click=True):
        """
        Send key strokes to an element.  Mostly used for input elements of type text.

        :param locator: the locator that specifies which element to send keystrokes to (usually defined on a Page class)
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before throwing a not found exception
        :type timeout: int or float (float for sub-second precision)
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :param clear: Should we clear (assuming it's an input with type=text) the value first?
        :type clear: bool
        :param click: Should we click first?
        :type click: bool
        :return: The reference to this Browser instance.
        :rtype: :class:`.Browser`
        """
        if timeout is None:
            timeout = self.default_timeout
        element = None
        if click:
            element = self._internal_click(locator, timeout, log, signal=True)
        else:
            element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        if clear:
            self.logger.debug("Clearing the value of {} before typing.".format(locator.describe()))
            element.clear()
        element.send_keys(keys)
        return self

    def get_page_text(self):
        """
        Get the text from the current web page.  This tries to get the value of the "text" attribute of the html
        root element on the page.

        :return: the text of the current page
        :rtype: str
        """
        element = self.wd_instance.find_element_by_tag_name("html")
        if element is not None:
            return element.text

    def get_text(self, locator, timeout=None, log=True):
        """
        Get the text of an element on the page.

        :param locator: the locator that specifies which element to get the text of
        :type locator: :class:`.WebElementLocator`
        :param timeout: The amount of time (in seconds) to look before throwing a not found exception
        :type timeout: int or float (float for sub-second precision)
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: the text of the element on success, exception raised on inability to find the element
        :rtype: str
        """
        if timeout is None:
            timeout = self.default_timeout
        element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        if element is None:
            raise WebDriverException(
                "Unable to find element {} after waiting for {:.2f} seconds".format(locator.describe(), float(timeout)))
        text = element.text
        if log:
            self.logger.debug("Found element {}, returning text: {}".format(locator.describe(), text))
        return text

    def get_attribute_value(self, locator, attribute_name, timeout=None, log=True):
        """
        Get the value of an html element's attribute.

        :param locator: the locator that specifies which element to get the attribute value of
        :type locator: :class:`.WebElementLocator`
        :param attribute_name: the name of the attribute to get
        :type attribute_name: str
        :param timeout: The amount of time (in seconds) to look before throwing a not found exception
        :type timeout: int or float (float for sub-second precision)
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: the text of the element on success, exception raised on inability to find the element
        :rtype: str
        """
        if timeout is None:
            timeout = self.default_timeout
        element = locator.find_element_matching(self.wd_instance, timeout, log, self.angular_mode)
        if element is None:
            raise WebDriverException(
                "Unable to find element {} after waiting for {:.2f} seconds".format(locator.describe(), float(timeout)))
        value = element.get_attribute(attribute_name)
        if log:
            self.logger.debug(
                "Found element {}, attribute {} has value: {}".format(locator.describe(), attribute_name, value))
        return value

    def first_page_found(self, page_classes, timeout=None, log=True):
        """
        Look for the first page class that returns true, and return it.  This is useful when you are trying to detect
        if a particular flow is happening.  Rather than waiting for one page class, this goes through a list each time
        and as soon as one returns true, it returns that element.

        :param page_classes: The list of page classes or page class instances.  Whatever you pass in here is what will
                             be returned if found.
        :param timeout: The amount of time (in seconds) to look before throwing a not found exception
        :type timeout: int or float (float for sub-second precision)
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: A page class from the list passed in (if found), None otherwise
        """
        page_list = []
        page_names = []
        for page in page_classes:
            page_list_val = {}
            page_list_val['retval'] = page
            if isinstance(page, Container):
                page_list_val['instance'] = page
            else:
                page_list_val['instance'] = page()
            page_names.append(page_list_val['instance'].get_name())
            page_list.append(page_list_val)
        if log:
            self.logger.debug("Waiting for one of the pages [{}] to be found.".format(','.join(page_names)))
        if timeout is None:
            timeout = self.default_timeout
        timer = Timer(timeout)
        while not timer.is_past_timeout():
            for page in page_list:
                if page['instance'].is_current_page(self):
                    if log:
                        self.logger.info("Found page {} after {:.2f} seconds.".format(page['instance'].get_name(),
                                                                                      time.time() - timer.start))
                    return page['retval']
            time.sleep(0.25)  # sleep a quarter of a second
        else:
            # The timer.is_past_timeout() returned true and that kicked us out of the loop
            if log:
                self.logger.warn(
                    "Waited {:.2f} seconds for one of the pages [{}] to return true from is_current_page, but that never happend.".format(
                        float(timeout), ','.join(page_names)))
            return None

    def get_url(self, log=True):
        """
        Get the current url of the web page.

        :param log: Whether or not to log
        :type log: bool
        :return: The URL as a string (how else would you represent it?)
        :rtype: str
        """
        if log:
            self.logger.debug("Getting current URL of browser.")
        retval = self.wd_instance.current_url
        if log:
            self.logger.debug("Current URL of browser is {}".format(retval))
        return retval

    def get_title(self, log=True):
        """
        Get the current title of the page.

        :param log: Whether or not to log
        :type log: bool
        :return: the title of the page
        :rtype: str
        """
        if log:
            self.logger.debug("Getting title of current page.")
        retval = self.wd_instance.title
        if log:
            self.logger.debug("Title of current page is {}".format(retval))
        return retval

    def select_option_by_text(self, locator, option_text, timeout=None, log=True):
        """
        Select an option of a select element by partial or complete text.

        :param locator: the locator that specifies how to find the select element
        :type locator: :class:`.WebElementLocator`
        :param option_text: The text of the option to select
        :type option_text: str
        :param timeout: The amount of time (in seconds) to look before throwing a not found exception
        :type timeout: int or float (float for sub-second precision)
        :param log: Whether or not to log details of the look for the element (default is True)
        :type log: bool
        :return: The reference to this Browser instance.
        :rtype: :class:`.Browser`
        """
        if log:
            self.logger.debug(
                'Selecting option by text "{}" from select element {}'.format(option_text, locator.describe()))
        element = self._internal_wait_for_changes_to_stop(locator, timeout, log)
        select = Select(element)
        select.select_by_visible_text(option_text)
        return self

    def screenshot_as_byte(self):
        """
        Take a screenshot of the browser, and return it as a png byte array.
        :rtype: byte[]
        """
        return self.wd_instance.get_screenshot_as_png()

    def refresh(self, log=True):
        """
        Refresh the page.
        :return: The reference to this Browser instance.
        :rtype: :class:`.Browser`
        """
        if log:
            self.logger.debug("Refreshing browser page.")
        self.wd_instance.refresh()
        return self

    def tap(self, positions, log=True):
        """
        Tap (for mobile browsers) on each of the positions passed in
        :param positions: A list of x, y coordinate tuples to tap.  If you want more than one coordinate, group each
                          coordinate in a tuple of their own.  Example: [(100, 200), (300, 400)].
        :type positions: [(int, int)]
        :return: The reference to this browser instance
        :rtype: :class:`.Browser`
        """
        if log:
            self.logger.debug("Performing a mobile tap at positions: {}".format(repr(positions)))
        self.wd_instance.tap(positions)
        return self

    def android_scroll_to_element(self, element_text, log=True):
        """
        Scroll to element with element_text in the text property
        :param element_text:
        :return:
        """
        if log:
            self.logger.debug("Scrolling to element with text property: {}".format(element_text))
        self.wd_instance.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("{}").instance(0))'.format(element_text))


class Container(object):
    """
    A generic container for structuring multiple *WebElementLocator* into groupings that help programmers find the right
    shared definition.
    """

    @property
    def browser(self):
        """
        The slickwd Browser instance.
        :return: The Browser instance of itself or it's parent.
        :rtype: Browser
        """
        if hasattr(self, '_browser'):
            return self._browser
        elif hasattr(self, 'parent') and self.parent is not None:
            return self.parent.browser
        else:
            return None

    @browser.setter
    def browser(self, new_instance):
        """
        Set the browser instance
        :param new_instance: the new instance of browser to set
        :type new_instance: :class:`.Browser`
        """
        self._browser = new_instance

    def get_name(self):
        """
        Get the full name of this page.  If using nested :doc:`page-classes` this will get the full *dotted* name
        of the page class.

        :return: A string containing the best guess at the page class name.
        """
        if hasattr(self, "parent") and hasattr(self, "container_name") and self.parent is not None:
            return "{}.{}".format(self.parent.get_name(), self.container_name)
        elif hasattr(self, "container_name"):
            return self.container_name
        else:
            name = self.__class__.__name__
            if name.endswith("Page"):
                name = name[:-4]
            return name

    def is_current_page(self, browser):
        """
        You should override this method in a subclass of Container.  This method is used to see if what is in the
        browser currently matches one or more elements of this class.  This method should be quick (timeout 0 for all
        your calls).  It may get called a lot, so you may want to turn off logging for any browser methods called
        (log=False parameter).

        :param browser: A :class:`.Browser` instance to use in detecting if this is the current page.
        :return: True if the current page matches what is in the browser, False otherwise.
        """
        raise NotImplementedError("is_current_page was not implemented on class: {}".format(self.__class__.__name__))

    def __setattr__(self, key, value):
        # this magic is for naming and setting of parent -> child relationships
        if key != "parent":
            if isinstance(value, Container):
                value.parent = self
                value.container_name = key
            if isinstance(value, WebElementLocator):
                value.parent = self
        return super(Container, self).__setattr__(key, value)
