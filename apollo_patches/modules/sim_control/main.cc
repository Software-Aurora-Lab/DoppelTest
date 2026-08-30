#include <iostream>
#include <memory>
#include <unistd.h>
#include "cyber/common/global_data.h"
#include "cyber/init.h"
#include "modules/dreamview/backend/common/dreamview_gflags.h"
#include "modules/dreamview/backend/map/map_service.h"
#include "modules/sim_control/sim_control.h"

// bazel build //modules/sim_control:sim_control_main
// /apollo/bazel-bin/modules/sim_control/sim_control_main
// pkill -f 'sim_control_main'

int main(int argc, char *argv[]) {
    apollo::cyber::Init(argv[0]);

    // Pick up --map_dir from the flagfile so the map set by
    // scripts/set_hd_map.sh is honored.
    google::ReadFromFlagsFile("/apollo/modules/common/data/global_flagfile.txt",
                              argv[0], true);

    std::unique_ptr<apollo::dreamview::MapService> map_service_;
    std::unique_ptr<apollo::dreamview::SimControl> sim_control_;

    map_service_.reset(new apollo::dreamview::MapService());
    sim_control_.reset(new apollo::dreamview::SimControl(map_service_.get()));

    // Deliberately NOT calling sim_control_->Start() here. DoppelTest starts
    // each instance by publishing its initial localization, and SimControl's
    // localization callback calls Start() itself. Enabling it at boot would
    // latch a dummy start point from the map and make the later Start() a
    // no-op, so the ADC would not spawn where DoppelTest asked.

    std::cout << "SimControl" << std::endl;

    apollo::cyber::WaitForShutdown();
    return 0;
}
