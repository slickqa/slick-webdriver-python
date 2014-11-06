Page Classes
============

.. toctree::
   :maxdepth: 2

What Are Page Classes?
----------------------

Page classes are an abstraction that allows you to define the elements you want to use in your tests and organize
them.  Page classes are a common technique in web testing, and as the name implies you can organize the elements
by what page they are on. Pages usually refer to a particular URL, but they don't have to. You can get more fine
grained than that as well, grouping elements into page classes that belong to a subsection of a page (like a tab).

There are two common styles of page classes, and which one you use depends on how deep the structure of the web
site you are testing is.  If you want to see real code examples of both, take a look at :doc:`examples`.  The following
is more of a technical description of advantages of each style.

Static Page Classes (Flat)
--------------------------

Static page classes are named that way because the attributes of the page classes that are instances of
:class:`WebElementLocator` are statically assigned to the class instead of an instance.  This
allows for a simple hierarchy in your organization structure.  Your structure will normally have
a page class that contains instances of :class:`WebElementLocator` that refer to how to find particular elements on
that page.  This works well for small websites, or web apps with
a simple flat navigation structure.

Advantages
~~~~~~~~~~

  * Less code
  * Simpler structure
  * Easier to read the page classes, not a lot of navigation or hierarchy to go through
  * No need to create instances of any page classes anywhere


Nested Page Classes
-------------------

This style uses instances of page classes, with elements and other page classes inside each container.  Normally
you would instantiate the top node, and you get all other nested nodes created as a result.  This can help with
specifying configuration parameters to the hierarchy as well as changing element locators as a result of such
configuration.

Advantages
~~~~~~~~~~

  * Runtime configurable page classes (you can pass parameters into a constructor)
  * You can have a single root with code completion to navigate the entire site
  * Child pages and web elements know where they are in the hierarchy making logs more descriptive
  * Tests are easier to write due to logical structure of page classes (less hunting to find out if a page class has
    already been written).
  * Less accidental duplication of element definitions (less hunting to find out if a page class has already been
    written).
  * Logs look much nicer and more like the test code (easier to follow along)

