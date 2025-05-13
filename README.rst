
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-dht/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/dht/en/latest/
    :alt: Documentation Status


.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_DHT/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_DHT/actions
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython support for the DHT11 and DHT22 temperature and humidity devices.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

.. note::
     This library uses the `pulseio` module in CircuitPython. As of CircuitPython 7.0.0, `pulseio` is
     no longer available on the smallest CircuitPython builds,
     such as the Trinket M0, Gemma M0, and Feather M0 Basic boards.
     You can substitute a more modern sensor, which will work better as well.
     See the guide `Modern Replacements for DHT11 and DHT22 Sensors
     <https://learn.adafruit.com/modern-replacements-for-dht11-dht22-sensors>`_
     for suggestions.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-dht/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-dht

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-dht

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-dht

Usage Example
==============

Hardware Set-up
----------------

Designed specifically to work with the Adafruit DHT series sensors:

* Adafruit `DHT22 temperature-humidity sensor + extras <https://www.adafruit.com/products/385>`_
* Adafruit `DHT11 temperature-humidity sensor + extras <https://www.adafruit.com/products/386>`_

.. note::
    DHT11 and DHT22 devices both need a pull-resistor on the data signal wire. This resistor is in the range of 1k to 5k


* Please check the device datasheet for the appropriate value.
* Be sure that you are running the Buster Operating System.
* Make sure that your user is part of the ``gpio`` group.


Known Issues
------------

* The library may or may not work in Linux 64-bit platforms.
* The Raspberry PI Zero does not provide reliable readings.
* Readings in FeatherS2 does not work as expected.

.. note::
     Using a more modern sensor will avoid these issues.
     See the guide `Modern Replacements for DHT11 and DHT22 Sensors
     <https://learn.adafruit.com/modern-replacements-for-dht11-dht22-sensors>`_.

Basics
-------

Of course, you must import the library to use it:

.. code:: python

    import adafruit_dht

The DHT type devices use single data wire, so import the board pin

.. code:: python

    from board import <pin>

Now, to initialize the DHT11 device:

.. code:: python

    dht_device = adafruit_dht.DHT11(<pin>)

OR initialize the DHT22 device:

.. code:: python

    dht_device = adafruit_dht.DHT22(<pin>)

Read temperature and humidity
------------------------------

Now get the temperature and humidity values

.. code:: python

    temperature = dht_device.temperature
    humidity = dht_device.humidity

These properties may raise an exception if a problem occurs.  You should use try/raise
logic and catch RuntimeError and then retry getting the values after at least 2 seconds.
If you try again to get a result within 2 seconds, cached values are returned.

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/dht/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_DHT/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
