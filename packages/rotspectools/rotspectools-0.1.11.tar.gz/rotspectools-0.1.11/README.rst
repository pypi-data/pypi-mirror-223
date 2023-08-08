=============================
Rotational Spectroscopy Tools
=============================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
        :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/rotspectools.svg
        :target: https://pypi.python.org/pypi/rotspectools

.. image:: https://readthedocs.org/projects/rotspectools/badge/?version=latest
        :target: https://rotspectools.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black


Package for automating data analysis and presentation for rotational spectroscopy datasets generated using Pickett's SPFIT/SPCAT programs.

Currently, it only supports simple asymmetrical rotors and the plotting of data distribution plots of measured spectral lines.


* Free software: MIT license
* Documentation: https://rotspectools.readthedocs.io.


Features
--------
Data Analysis
************************
* Clean datasets by eliminating high error lines, at a specified threshold error.
* Remove duplicate lines from SPFIT .lin files.

Data Visualization
********************************
* Generate data distribution plots of measured lines, with a-, b-, and c-type transitions differentiated by color. This visualization was inspired by Kisiel's AC.exe program and GLE script.

TODO
**********
- Add in support for other types of molecules
- Support presentation of predicted spectra using SPCAT's .cat file format
- Add capability to use SPFIT/SPCAT as a backend to generate files/classes.

Credits
-------

Thanks to the McMahon-Woods Research Group for continually breaking this tool and making it better.
