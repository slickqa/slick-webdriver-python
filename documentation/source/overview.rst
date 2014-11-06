Overview
========

.. toctree::
   :maxdepth: 2

Web Testing in General
----------------------

Web testing is quite simple.  This is mostly because of open standards, and excellent tools (such as 
`Selenium <http://seleniumhq.org>`_ on which this project is based).  Because it is so simple, it is
also real easy to get yourself into a maintenance nightmare.  This document will hopefully help you
to get started in a way that will make things easy to grow and maintain.

To do web testing using this library you are going to want:

  1. A Browser, `Firefox <http://getfirefox.com>`_ is one of the easiest to get started with selenium.
  2. Python (I assume you have this or why else are you looking at this?)
  3. This library installed into python (use pip to install it)
  4. `Nose <http://nose.readthedocs.org>`_ though technically you can test with the builtin unittest module, nose makes
     running the tests easier.

Best Practices
--------------

There are several things you will want to do to help you scale your testing from a couple of tests here and there to
hundreds, possibly even thousands of tests.  Below are suggestions, the framework does not restrict you to following
them, but they will help.

  1. Put your page classes in a separate place from your tests.  Make sure they are usable from multiple sets
     of tests, even if you don't have multiple sets of tests yet. See :doc:`page-classes`.
  2. Don't put assertions in your page classes / framework code.  Assertions belong in tests, not framework.
  3. Don't try to model everything your product does, model what you need for your test.  Spend time working on tests,
     the *framework* is just part of the test that has to be written for efficiency reasons (sharing code).
  4. Group your tests, and keep track of meta-data (however your framework chooses to do so).  It'll come in handy when
     you need it later.
  5. Make your locators and page classes as simple as possible, this simpler it is, the easier it is to maintain.
  6. Don't use record / playback tools, they create horrific unmaintainable code!
  7. Browser dev tools are great for helping you to inspect elements to automate.
  8. Make sure your tests read well, your test should look like a list of actions and assertions.  If you have a lot
     of boilerplate code, consider refactoring.

Writing Tests
-------------

The process for writing tests involves working with 2 different types of code: page classes and *framework*, and test
code.  You can easily write both at the same time.  Here is the typical workflow I do for writing a test:

  1. Write the code (or reuse the code) to launch the browser, and manually open the browser.
  2. Go to the URL in the browser, and once again, write the code to go to the correct url.
  3. Go through any other setup procedure manually, and make sure you have code to match.  This is an excellent place
     for framework code, reusable setup code (like logging in).
  4. Look for the first web action to do, inspect the element.  Your looking for something that uniquely identifies the
     element.  An **id** is the easiest, but they are not always there, especially on repeated elements.  For forms,
     names can usually identify the elements.  As soon as you find what identifies it, create or add it to a page class.
     See :doc:`page-classes` and :doc:`locators` for more details.
  5. Keep adding code to exercise the web site, but look for places where you need to assert that things are progressing.
     Don't be afraid to add assertions in the middle, make sure every step works properly.

I think that writing the automation, while manually executing the test is the easiest way to create a good test.
However, with this method you need to watch out for where it would break, or show errors when it's not working.  You
might need to look for elements that are there to display errors and assert that they are empty.

Tests should be readable and easy to understand.  If you notice you are repeating yourself a lot, or your tests
are confusing, stop and fix it!

