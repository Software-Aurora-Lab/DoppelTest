Welcome to DoppelTest's documentation!
======================================

DoppelTest is a scenario-based test generation framework for revealing bugs in autonomous driving softwares. It manages and orchestrates multiple ADS instances to simultaneously operate in a scenario and discover violation that occur by or among them. Since all vehicles are controlled by an instance of the ADS under test, each of them should respect traffic rules and react properly to other road traffic participants. At least one instance will be responsible for any violation occuring.

.. You can get started with Installation and then get an overview with the Quickstart. There is also more detailed Tutorial that shows how to use parts of DoppelTest to create new approaches. The rest of the docs describe each component of DoppelTest in detail, with a full reference in the Internals section.

DoppelTest is implemented in Python 3.8.10 and depends on ``cyber_record``, ``DEAP``, ``docker``, ``NetworkX``, ``NumPy``, ``pandas``, ``protobuf``, ``Shapely``, and ``websocket-client``. More information for these libraries can be found at 

* `cyber_record - Apollo's cyberRT record file offline parse tool <https://pypi.org/project/cyber-record/>`_
* `DEAP - Evolutionary computation framework <https://pypi.org/project/deap/>`_
* `Docker - Docker Engine API <https://pypi.org/project/docker/>`_
* `NetworkX - Creation, manipulation, and study of structure, dynamics, and functions of complex networks. <https://pypi.org/project/networkx/>`_
* `NumPy - Scientific computing with Python <https://pypi.org/project/numpy/>`_
* `pandas - Python data analysis toolkit <https://pypi.org/project/pandas/>`_
* `protobuf - Python implementation of Google's data interchange format <https://pypi.org/project/protobuf/3.19.0/>`_
* `Shapely - Manipulation and analysis of planar geometric objects <https://pypi.org/project/shapely/>`_
* `websocket-client - WebSocket client for Python <https://pypi.org/project/websocket-client/>`_


DoppelTest was designed and implemented by Yuqi Huai, Yuntianyi Chen, Sumaya Almanee, Tuan Ngo, Xiang Liao, Ziwen Wan, Qi Alfred Chen and Joshua Garcia. If you have any problems using DoppelTest, please submit an issue to `our GitHub repository <https://github.com/YuqiHuai/DoppelTest>`_  or contact Yuqi at yhuai@uci.edu.

Known Issues
============
1. DoppelTest is optimized for small maps. While we provide 7 HD maps
   in the release, its performance is significantly better on ``borregas_ave``.

2. The initial analylsis of HD map may take more time to analyze. Its efficiency is
   based on the number of lanes the map has. It mainly checks
   the relation between each pair of lanes to determine whether a valid
   path exists between them. You do not have to do this analysis if you trust the 
   HD map provided. (More details in 
   `Apollo Issue #14529 <https://github.com/ApolloAuto/apollo/issues/14529>`_)

Table of Contents
=================

.. toctree::
   :maxdepth: 1
   :caption: Introduction

   installation

.. toctree::
   :maxdepth: 1
   :caption: Tool reference

   quickstart
   internals

.. toctree::
   :maxdepth: 1
   :caption: Tutorials

   tutorials/new_oracle

.. toctree::
   :maxdepth: 1
   :caption: General Information

   publication

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
=======

DoppelTest is distributed under the `The GNU General Public License v3.0 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_.