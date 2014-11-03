Getting Started Tutorial
========================

.. toctree::
   :maxdepth: 2

Web Testing Overview
--------------------

Web testing is quite simple.  This is mostly because of open standards, and excellent tools (such as 
`Selenium <http://seleniumhq.org>`_ on which this project is based).  Because it is so simple, it is
also real easy to get yourself into a maintenance nightmare.  This document will hopefully help you
to get started in a way that will make things easy to grow and maintain.

Best Practices
--------------

There are several things you will want to do to help you scale your testing from a couple of tests here and there to
hundreds, possibly even thousands of tests.

Creating Page Classes
---------------------

You will want to create page classes to organize your web testing.  This allows for code
re-use between tests.  It also unclutters your tests, removing possibly repeated hard coded
locators for web elements you are going to use in your testing.

Writing Tests
-------------

When writing your tests, if you've already created the page classes, this part should be easy.
Tests should be readable and easy to understand.  If you notice you are repeating yourself
a lot, or your tests are confusing, stop and refactor!
