Using the Webdriver APIs
========================

Only a fool would be convinced that they wrote everything that anyone would ever need.  As this project is a wrapper
of existing webdriver apis, I know that I won't provide everything you might need.  There is easy access to
the underlying webdriver instances.

Why you might need them
-----------------------

Sometimes you have encountered a problem which is not yet handled by the wrapper, or you are trying to do something
outside the scope of the wrapper.  One simple example is that the wrapper is not (yet) well suited to acting
on a list of elements.  Don't fret, the webdriver apis are there, and they are pretty good.

How to get to them
------------------

An attribute of the :class:`slickwd.Browser` class is the driver instance: *wd_instance*.  This should give you most
of what you need.  If you want to find a list of elements, or a single element for which you already have a locator,
you can do use the :meth:`slickwd.WebElementLocator.find_element_matching`.
