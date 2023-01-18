.. DoppelTest documentation master file, created by
   sphinx-quickstart on Tue Jan 17 17:57:48 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DoppelTest's documentation!
======================================

DoppelTest is a scenario-based test generation framework for revealing bugs in autonomous driving softwares. It manages and orchestrates multiple ADS instances to simultaneously operate in a scenario and discover violation that occur by or among them. Since all vehicles are controlled by an instance of the ADS under test, each of them should respect traffic rules and react properly to other road traffic participants. At least one instance will be responsible for any violation occuring.

You can get started with Installation and then get an overview with the Quickstart. There is also more detailed Tutorial that shows how to use parts of DoppelTest to create new approaches. The rest of the docs describe each component of DoppelTest in detail, with a full reference in the Internals section.

DoppelTest is implemented in Python 3.8 and depends on .... The documentation for these libraries can be found at 

DoppelTest was designed and implemented by Yuqi Huai, Yuntianyi Chen, Sumaya Almanee, Tuan Ngo, Xiang Liao, Ziwen Wan, Qi Alfred Chen and Joshua Garcia. If you have any problems using DoppelTest, please submit an issue to `our GitHub repository <https://github.com/YuqiHuai/DoppelTest>`_  or contact Yuqi at yhuai@uci.edu.

.. autofunction:: apollo.utils.generate_adc_polygon


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
=======

DoppelTest is distributed under the `The GNU General Public License v3.0 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_.