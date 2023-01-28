# REQUIREMENTS

DoppelTest is implemented in Python to realize Doppelganer Testing for an
open-source production grade ADS, therefore its requirements depend on the
requirements of the ADS. We recommend running the framework with following
hardware/software:

## Hardware and Software Requirements

- Intel Core i9 12900K (16-core)

- 64 GB memory and above

- Ubuntu 18.04 and above

- Docker-CE version 19.03 and above

- Python 3.8.10 and above

- NVIDIA RTX 3090 and above **(Optional)**

- NVIDIA driver version 455.32.00 and above **(Optional)**

- NVIDIA Container Toolkit **(Optional)**

## Additional Information

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
