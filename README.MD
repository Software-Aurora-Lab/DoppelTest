# DoppelTest

## Introduction

DoppelTest is a Python framework implemented to evaluate a novel autonomous driving software (ADS) testing approach discussed in the paper titled Doppelganger Test Generation for Revealing Bugs in Autonomous Driving Software. This research artifact implements a framework that orchestrates multiple instances of the same ADS and generates virtual scenarios with those instances. Since all vehicles in the virtual scenario are controlled by different instances of the ADS under test, any actual violation that occurs by or among them inherently reveals ADS misbehavior, thus revealing ADS bugs.

The documentation of DoppelTest can be found at https://www.ics.uci.edu/~yhuai/DoppelTest/

The DOI for this repository is: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7575583.svg)](https://doi.org/10.5281/zenodo.7575583)

## Hardware and Software Requirements

- Intel Core i9 12900K (16-core)

- 64 GB memory and above

- Ubuntu 18.04 and above

- Docker-CE version 19.03 and above

- Python 3.8.10 and above

- NVIDIA RTX 3090 and above **(Optional)**

- NVIDIA driver version 455.32.00 and above **(Optional)**

- NVIDIA Container Toolkit **(Optional)**

### Additional Information

Doppelganger Testing relies on simultaneously running multiple instances of
the same ADS, therefore the requirement for running DoppelTest varies based
on 1) the minimum requirement of the ADS and 2) number of instances you wish
to run. Note the prerequisites listed above are mostly the same as the minimum
requirements to run the ADS under test with the exception of better CPU and
memory due to the need to concurrently run multiple instances. We have tested
DoppelTest on personal workstations with the following configuration:

- C1 - 5 instances on Intel Core i9 12900KF (16-core) with 32 GB DDR5 memory,
  equipped with NVIDIA GeForce 3090 Ti.

- C2 - 10 instances on Intel Core i9 12900K (16-core) with 128 GB DDR4 memory,
  equipped with NVIDIA GeForce 3090.

## Installing

### INSTALLING Baidu Apollo

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

### INSTALLING DoppelTest

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

## Citing

If you use the project in your work, please consider citing the following work:

```
@inproceedings{doppeltest,
	address = {Melbourne, Australia},
	title = {Doppelganger {Test} {Generation} for {Revealing} {Bugs} in {Autonomous} {Driving} {Software}},
	author = {Huai, Yuqi and Chen, Yuntianyi and Almanee, Sumaya and Ngo, Tuan and Liao, Xiang and Wan, Ziwen and Chen, Qi Alfred and Garcia, Joshua},
    booktitle = {{ACM}/{IEEE} 45th {International} {Conference} on {Software} {Engineering}},
	year = {2023},
}
```
