Locators
========

.. toctree::
   :maxdepth: 2

What are Locators
-----------------

Locators are the most basic element in Slick Webdriver.  The idea is that a locator defines how to find an element
that you want to take action on.  How you define your locators can help make the difference between easy and
very difficult maintenance levels for your tests.  The good news is that it's easy to make your maintenance easy.

Locators are instances of the :class:`slickwd.WebElementLocator`, but are most often created by using methods
on the :class:`slickwd.Find` class.

Common Strategies
-----------------

If you can keep your locators defined simply, they are less likely to break when something else in the product
changes.  It can be frustrating to have your tests break because an unrelated area of the product was changed.  To
avoid this you want to define your locators using information that doesn't depend on other areas of the web page.

In the end, your are looking for something unique about the element you are trying to locate.  Most often web
developers need to identify the element uniquely for styling or attaching javascript event listeners, so you
shouldn't have too much trouble.

More Complex Strategies
-----------------------

If the element your trying to uniuqely identify on the page has nothing unique, you may have to rely on other
elements in the hierarchy to uniquely identify it.  This could be a pattern of how the element is laid out,
an ancestor that is uniquely identifiable, etc.
