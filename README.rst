=====================
labd.localemiddleware
=====================


Status
======

W.I.P. 

Installation
============

.. code-block:: shell
   pip install labd.localemiddleware
..

add to MIDDLEWARE in your django settings:

.. code-block:: python

   MIDDLEWARE = [
    ...
    "labd.middleware.locale.LocaleMiddleware",
    ...
   ]
..
