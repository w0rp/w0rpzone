The w0rp zone website
=====================

This is the source code for my website [w0rp zone](https://w0rp.com). With the
exception of webserver configuration files and a few settings, this is the
website's complete source code.

As described in the licence directory, the source code of this website is made
available under a two-clause BSD licence, which can be viewed in that directory.

Feel free to distribute and modify this website, and if you do evolve software
from this website or learn from parts of it, feel free to drop me an email at
dev@w0rp.com and tell me about it.

Installation
------------

* Install postgres and a database.
* Install Python 3.6 with virtualenv and pip.
* Run `tool/mkenv` to create the virtualenv with all required modules.
* Create a `settings.py` file with a database configuration.
* If you want to run JS tests and work on JS code, run `yarn`.
