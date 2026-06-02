import json
import sys
import traceback

from absl import app
import docker

from apollo.ApolloContainer import ApolloContainer
import config
from framework.scenario import Scenario
from framework.scenario.ScenarioRunner import ScenarioRunner
from hdmap.MapParser import MapParser

def run_scenario(scenario_json: str, g_name: str, s_name: str):
    MapParser.get_instance(config.HD_MAP)

    scenario = Scenario.from_json(scenario_json)
    scenario.gid = 0
    scenario.cid = 0

    print(f'Loaded scenario: {scenario.to_dict()}')

    num_ad_agents = len(scenario.ad_section.adcs)

    containers = [
        ApolloContainer(config.APOLLO_ROOT, f'ROUTE_{i}')
        for i in range(num_ad_agents)
    ]

    # Start containers
    for ctn in containers:
        print(f'{ctn.container_name}: starting')
        ctn.start_instance()
        ctn.start_dreamview()
        print(f'Dreamview at http://{ctn.ip}:{ctn.port}')

    # Run scenario
    srunner = ScenarioRunner(containers)
    srunner.set_scenario(scenario)
    srunner.init_scenario()
    srunner.run_scenario(g_name, s_name, True)
    
    # stop apollo_dev_X containers
    docker_client = docker.from_env()
    for container in docker_client.containers.list():
        if container.name.startswith('apollo_dev_'):
            print(f'Stopping container: {container.name}')
            container.stop()
            print(f'Removing container: {container.name}')
            container.remove()



def main(argv: list) -> None:
    if len(argv) != 4:
        raise app.UsageError(
            "Expected arguments: <scenario_json> <g_name> <s_name>"
        )

    try:
        run_scenario(*argv[1:])

    except Exception as exc:
        # Structured error output (very useful for subprocess caller)
        error_payload = {
            "status": "error",
            "error_type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc()
        }

        print(json.dumps(error_payload), file=sys.stderr)

        sys.exit(1)  # non-zero exit → subprocess knows it failed

    else:
        # Optional success signal
        print(json.dumps({"status": "success"}))
        sys.exit(0)


# CLI entrypoint
if __name__ == "__main__":
    app.run(main)
