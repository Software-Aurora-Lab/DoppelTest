Quickstart
==========

We discuss the overall structure of DoppelTest and describe what each 
of the main and test scripts does. For more detailed documentation for
each of the internal modules, please refer to :ref:`internals:internals`.

Directories
-----------

* ``apollo`` directory containes code that are related to controlling 
  Apollo containers and communicating with Apollo's cyberRT bridge.

* ``data`` directory contains HD maps under ``data/maps`` and DoppelTest
  will save records to ``data/records``. When violations are detected, you
  will also see a ``data/records/summary.csv`` describing violations discovered
  for each scenario.

* ``docs`` directory contains all the documentation source code.

* ``framework`` directory contains code that are related to genetic representation
  of the scenario, and actually using those representation to run a scenario.

* ``hdmap`` directory contains code that are related to parsing HD map. HD map typically
  comes in binary form and you can parse and analyze it using protobuf.

* ``modules`` directory contains Python files compiled from all ``*.proto`` files from Apollo.
  We use these to parse and construct binary messages because the communication between cyberBridge
  uses this binary format.

* ``utils`` directory contains all the utility functions, such as logging, managing file storage,
  etc.


Main scripts
------------

* ``config.py``

  .. note:: Please refer to ``apollo/modules/common/data/vehicle_param.pb.txt`` for size of the vehicle,
    also remember to update ``APOLLO_ROOT`` and ``DT_ROOT``!
  .. automodule:: config
    :members:

* ``main_ga.py``

  A version of DoppelTest with multiple ADS instances and genetic
  algorithm. 
  Please refer to our main paper in :ref:`publication:publication` 
  for details with regard to the genetic algorithm 
  implemented.

* ``main_baseline.py``

  A baseline version used for comparison. This version
  relies on modeling road traffic participants as constant 
  speed obstacles.

* ``main_determinism.py``

  A script that helps to determine whether a scenario generated
  from a chromosome always results in the same set of violations
  or not.

* ``main_ga_performance.py``

  A modified version of ``main_ga.py`` with timers added to
  compute its implementation efficiency.

* ``main_random.py``

  A version DoppelTest with multiple ADS instance and randomly
  generated chromosomes (i.e., no genetic algorithm).


Test scripts
------------
* ``test_analyzer.py``

  A test script that runs oracles on the specified record file.

* ``test_liability_checker.py``

  A test script that tests the implementation of our liability
  checker.

* ``test_main.py``

  A test script used for verifying the installation of DoppelTest.
