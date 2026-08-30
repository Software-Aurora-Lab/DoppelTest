# DoppelTest

## Introduction

DoppelTest is a Python framework implemented to evaluate a novel autonomous driving software (ADS) testing approach discussed in the paper titled Doppelganger Test Generation for Revealing Bugs in Autonomous Driving Software. This research artifact implements a framework that orchestrates multiple instances of the same ADS and generates virtual scenarios with those instances. Since all vehicles in the virtual scenario are controlled by different instances of the ADS under test, any actual violation that occurs by or among them inherently reveals ADS misbehavior, thus revealing ADS bugs.

The documentation of DoppelTest can be found under `docs` directory, you can build the it locally by running `cd docs && make html`.

The DOI for this repository is: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7575582.svg)](https://doi.org/10.5281/zenodo.7575582)

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

In this section we will be discussing steps to replicate the results discussed in the paper

### INSTALLING Baidu Apollo

> You can now use `scripts/install_apollo.sh` to automatically install Apollo!

DoppelTest runs against the `v7_mozart` branch of
[YuqiHuai/BaiduApollo](https://github.com/YuqiHuai/BaiduApollo/tree/v7_mozart),
a fork of Apollo 7.0 that ships the cyber bridge and the standalone SimControl
this framework depends on. The DoppelTest-specific pieces that branch does not
carry live in `apollo_patches/` in this repository and are copied into the
Apollo checkout at install time. `scripts/install_apollo.sh` performs all of the
steps below:

1. Clone the fork into this repository's root as `apollo-doppeltest`

   ```bash
   git clone https://github.com/YuqiHuai/BaiduApollo.git \
     --branch v7_mozart --depth 1 apollo-doppeltest
   ```

2. At the root directory of Baidu Apollo, create directories `data/log`, `data/bag`, `data/core`, and `records`

> This step is necessary for DoppelTest running on the host machine to delete Apollo's log files. Our framework restarts modules being tested after every scenario, which creates a large number of unnecessary log files.

> Since a lot of commands are executed as root inside of the Docker container, if those directories are created inside of the container, DoppelTest may not be able to remove those directories.

3. Copy the contents of `apollo_patches/` into the Apollo checkout

   ```bash
   cp -a apollo_patches/. apollo-doppeltest/
   ```

> This installs three things: `scripts/bootstrap_doppeltest.sh` (starts/stops routing, prediction, planning, and `simplified_planning`; invoked by `apollo/ApolloContainer.py`); `modules/custom_nodes/`, whose `simplified_planning` node republishes a trimmed `ADCTrajectory` on `/apollo/planning/simplified` (the full planning message does not fit the cyber bridge client's single-`recv` framing, so DoppelTest subscribes to the simplified channel instead); and `modules/sim_control/main.cc`, which drops the branch's boot-time `sim_control_->Start()`. DoppelTest enables SimControl by publishing each instance's initial localization, and starting it at boot would latch a dummy map start point and make that a no-op.

> This must happen before the build so bazel picks up `//modules/custom_nodes` and the patched `sim_control_main`.

4. At the root directory of Baidu Apollo, start a container dedicated to building

   ```bash
   DEV_CONTAINER=doppeltest_installer ./docker/scripts/dev_start.sh -l -y --fastest
   ```

> The build container is named `doppeltest_installer` so it cannot collide with `apollo_dev_$USER`, which other projects on the same machine use. DoppelTest starts its own `apollo_dev_ROUTE_*` containers at run time.

> `--fastest` skips the map and other Docker volumes. Those volumes are mounted over `modules/map/data/<map>` and would shadow the HD maps installed by `scripts/install_hd_maps.sh`.

5. In the container, build Apollo

   ```bash
   docker exec -u $USER doppeltest_installer \
     bash -c "source /apollo/scripts/apollo.bashrc && bash /apollo/apollo.sh build"
   ```

6. Remove the build container via `docker rm -f doppeltest_installer`

> The build output lives in `apollo-doppeltest/.cache` on the host, so the container is disposable.

### INSTALLING DoppelTest

> You can now use `uv sync` to setup DoppelTest's Python dependencies!

1. Install the required Python libraries via `pip install -r requirements.txt`

> If you run into issues when installing Shapely library, please first run `sudo apt-get install libgeos-dev` to install its dependencies.

2. Replace location of directories in `config.py`

   ```python
   APOLLO_ROOT  = '/xxx/xxx/apollo'
   DT_ROOT      = '/xxx/xxx/DoppelTest'
   ```

3. Verify the framework is runnable via `python test_main.py`

> You should start seeing 3 Apollo instances being started and the scenario is visualizable via a browser. DoppelTest will provide the URL to visualize each instance in the terminal.

4. Start the framework via `python main_ga.py`

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

## Known Issues

1. CPU overclocking has caused segmentation faults, freezing, and failure to build Apollo. See [DoppelTest/Issue#5](https://github.com/Software-Aurora-Lab/DoppelTest/issues/5). Many thanks to Lejin Li from Kyushu University for the investigation.
