Page Classes
============

.. toctree::
   :maxdepth: 2

What Are Page Classes?
----------------------

Page classes are an abstraction that allows you to define the elements you want to use in your tests and organize
them.  Page classes are a common technique in web testing, and as the name implies you can organize the elements
by what page they are on.  You can get more fine grained than that as well, defining which tab (whithin a page)
an element is on as an example.

There are two common styles of page classes, and which one you use depends on how deep the structure of the web
site you are testing is.

Static Page Classes (Flat)
--------------------------

Static page classes are named that way because the web element locators in them are typically static.  This
allows mostly for a simple hierarchy in your organization structure.  Your structure will normally have
a page class that containes elements on that page.  This works well for small websites, or web apps with
a simple flat navigation structure.

Nested Page Classes
-------------------

This style uses instances of page classes, with elements and other page classes inside each container.  Normally
you would instantiate the top node, and you get all other nested nodes created as a result.  This can help with
specifying configuration parameters to the hierarchy as well as changing element locators as a result of such
configuration.
