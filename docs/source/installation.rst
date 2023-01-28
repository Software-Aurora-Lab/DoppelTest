Installation
============


Hardware and Software Requirements
----------------------------------

* Intel Core i9 12900K (16-core)

* 64 GB memory and above

* Ubuntu 18.04 and above

* Docker-CE version 19.03 and above

* Python 3.8.10 and above

* NVIDIA RTX 3090 and above **(Optional)**

* NVIDIA driver version 455.32.00 and above **(Optional)**

* `NVIDIA Container Toolkit <https://github.com/NVIDIA/nvidia-docker>`_ **(Optional)**

.. note::
    Graphics card and its related support are optional because 
    the focus of this framework is on the Planning and the Prediction 
    module of the ADS, both does not require the use of a graphics card.

.. note::
    DoppelTest relies on running multiple instances of ADS simultanously 
    to generate scenarios. Therefore the prerequisite varies based on 1) 
    the minimum requirement of the ADS and 2) the number of instances you 
    wish to run at the same time. The prerequisite listed above is capable
    of running 5 instances; and we have tested running 10 instances on a 
    machine with 128GB memory.

Installing Baidu Apollo
-----------------------

1. Clone the forked version of Baidu Apollo 7.0 
   from https://github.com/YuqiHuai/apollo

    .. note:: In this forked version, we made slight adjustments that 
        are not related to the AD stack.

2. At the root directory of Baidu Apollo, start up an Apollo container 
   via ``./docker/scripts/dev_start.sh -l``

3. Find the name of the container via ``docker ps -a``

4. Enter the container in root mode via ``docker exec -it apollo_dev_your_name /bin/bash``

    .. note:: Remember to replace ``apollo_dev_your_name`` with the 
        container's actual name

5. In the container, build Apollo via ``./apollo.sh build``

6. Exit the container and create directories ``data``, 
   ``data/log``, ``data/bag``, ``data/log``, ``data/core`` under Apollo's 
   root directory.

    .. note:: This step is necessary for DoppelTest running on the host 
      machine to delete Apollo's log files. Our framework restarts modules 
      being tested after every scenario, which creates a large number of
      unnecessary log files. 
      
      Since a lot of commands are executed as root inside of the Docker 
      container, if those directories are created inside of the container,
      DoppelTest may not be able to remove those directories.

Installing DoppelTest
---------------------

1. Install the requirement Python libraries via ``pip install -r requirements.txt``

2. Replace location of directories in ``config.py``

    .. code-block:: python
        
        APOLLO_ROOT = '/xxx/xxx/apollo'
        DT_ROOT     = '/xxx/xxx/DoppelTest'

3. Verify the framework is runnable via ``python test_main.py``

    .. note:: You should start seeing 5 Apollo instances being started and 
      the scenario is visualizable via a browser. DoppelTest will provide 
      the URL to visualize each instance in the terminal.

4. Start the framework via ``python main_ga.py``

    .. note:: After running DoppelTest for extended period of time, you should
      see record file of scenarios generated under ``data/records``.