# DoppelTest 

A doppelgänger testing approach for automatically finding bug-revealing violations of autonomous driving systems

## Set Up Instruction
Please follow the following steps to set up the framework.
### Set up Apollo 7.0, with a standalone Sim Control 
1. Clone the forked version of Apollo 7.0 from [URL removed for ICSE submission]
> In our version, we separated Sim Control from Dreamview, because Dreamview can suffer from unknown issues due to high number of websocket communication.
2. Start up Apollo container via `./docker/scripts/dev_start.sh -l`
3. Find the name of container via `docker ps -a`
4. Enter the container in root mode `docker exec -it apollo_dev_your_name /bin/bash`
> Remember to replace `apollo_dev_your_name` with the name of your container.
5. In the container, build Apollo via `./apollo.sh build`
6. Exit the container and create directories `data`, `data/log`, `data/bag`, `data/log`, `data/core` under Apollo's root directory.
> This step is necessary for our framework running on the host machine to delete Apollo's log files. 
> Our framework restarts modules being tested after every scenario, which creates a large number of unnecessary log files.
7. In the container, start up Dreamview via `./scripts/bootstrap.sh`
8. Exit the container, and find the IP address of the container via `docker inspect apollo_dev_your_name`
9. Verify Dreamview is accessible at `http://172.17.0.2:8888` (your container IP address may be different)


### Set up DoppelTest
1. Install the required Python libraries: numpy, Shapely, DEAP, pandas, networkx, [docker](https://docker-py.readthedocs.io/en/stable/) and [cyber_record](https://github.com/daohu527/cyber_record)
2. Replace directories in `config.py`
https://github.com/YuqiHuai/DoppelTest/blob/04d63ec063bf17162113f7cc0111fe63c7ff422d/config.py#L19-L20
3. Verify that the framework is runnable via `python test_main.py`
> You might be prompted to downgrade Python protobuf via `pip install protobuf==3.20.1`
4. Start the magic via `python main_ga.py` or `python main_random.py`
