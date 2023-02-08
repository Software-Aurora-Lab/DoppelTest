# STATUS

The authors are applying for the following badges:

1. Artifacts Evaluated - Reusable
2. Artifacts Available - Available

The artifact deserves those badges because of the following reasons:

1. The artifact has been tested on 5 machines to produce the results
   in the main paper, therefore demonstrating its functionality. We
   also provide an Oracle VM VirtualBox image [^1] for reviewers to easily
   verify its functionality.

2. The artifact is carefully designed and implemented, dividing code
   into individual modules, some specific to the framework and some
   reusable when developing an entirely new framework. For example,
   `CyberBridge` allows direct communication between the testing approach
   and the ADS, which typically requires an external simulator to
   accomplish; `MessageBroker` is a light-weight module that can orchestrate
   multiple ADS instances so that a virtual scenario with multiple ADS
   instsances can be generated.

3. The provided artifact includes detailed documentation on what each file
   does. We also provide tutorials on how to extend the oracles defined
   in Doppeltest [^2] and how to reuse a component of DoppelTest for other
   purposes [^3].

4. The authors have placed the artifact on a publicly accessible archival
   repository [^4]. The DOI for this artifact is `10.5281/zenodo.7575582`.

[^1]: https://doi.org/10.5281/zenodo.7622731
[^2]: https://www.ics.uci.edu/~yhuai/DoppelTest/tutorials/new_oracle.html
[^3]: https://www.ics.uci.edu/~yhuai/DoppelTest/tutorials/cyber_bridge.html
[^4]: https://doi.org/10.5281/zenodo.7575582
