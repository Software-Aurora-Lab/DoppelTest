# INSTALL

The following guide serves as a user manual for running DoppelTest to realize
Doppelganer Testing on a production-grade ADS (Baidu Apollo). The installation
is divided into 2 parts - 1) installing the ADS and 2) installing DoppelTest.

## INSTALLING Baidu Apollo

1. Clone the forked version of Apollo 7.0 from https://github.com/YuqiHuai/apollo

> In this forked version, we made slight adjustments that are not related to the AD stack

2. At the root directory of Baidu Apollo, start up Apollo container via `./docker scripts/dev_start.sh -l`

3. Find the name of the container via `docker ps -a`

4. Enter the container in root mode via `docker exec -it apollo_dev_your_name /bin/bash`

> Remember to replace `apollo_dev_your_name` with the container's actual name

5. In the container, build Apollo via `./apollo.sh build`

6. Exit the container and create directories `data`, `data/log`, `data/bag`, `data/log`,
   `data/core` under Apollo's root directory.

> This step is necessary for DoppelTest running on the host machine to delete Apollo's log files. Our framework restarts modules being tested after every scenario, which creates a large number of unnecessary log files.

> Since a lot of commands are executed as root inside of the Docker container, if those directories are created inside of the container, DoppelTest may not be able to remove those directories.

## INSTALLING DoppelTest

1. Install the required Python libraries via `pip install -r requirements.txt`

2. Replace location of directories in `config.py`

   ```python
   APOLLO_ROOT  = '/xxx/xxx/apollo'
   DT_ROOT      = '/xxx/xxx/DoppelTest'
   ```

3. Verify the framework is runnable via `python test_main.py`

> You should start seeing 5 Apollo instances being started and the scenario is visualizable via a browser. DoppelTest will provide the URL to visualize each instance in the terminal.

4. Start the magic via `python main_ga.py` or `python main_random.py`

> After running DoppelTest for extended period of time, you should see record file of scenarios generated under `data/records`. This is also the step to replicate the results presented in the paper.
