import uuid
from typing import Iterator

import docker
from docker.errors import NotFound
import pytest

from apollo.ApolloContainer import ApolloContainer
import config


MAP_NAME = "apollo/borregas_ave"


def _docker_client() -> docker.DockerClient:
    """Return a Docker client or skip the test if Docker is unavailable."""
    client = docker.from_env()
    try:
        client.ping()
    except Exception as exc:  # pragma: no cover - environment-specific
        pytest.skip(f"Docker is unavailable: {exc}")
    return client


@pytest.fixture
def running_container() -> Iterator[ApolloContainer]:
    """Start an Apollo container and clean it up after the test."""
    username = f"DOPPELTEST_MAP_{uuid.uuid4().hex[:8]}"
    container = ApolloContainer(config.APOLLO_ROOT, username)
    client = _docker_client()

    try:
        container.start_instance()
        yield container
    finally:
        try:
            docker_container = client.containers.get(container.container_name)
        except NotFound:
            return

        try:
            container.stop_container()
        except Exception:
            pass

        docker_container.remove(force=True)


def test_install_map_generates_routing_and_sim_maps(
    running_container: ApolloContainer,
) -> None:
    """Install a real Apollo map and verify the generated artifacts exist."""
    generated_map_name = running_container.install_map(MAP_NAME)
    docker_container = _docker_client().containers.get(
        running_container.container_name
    )

    routing_result = docker_container.exec_run(
        f"test -s /apollo/modules/map/data/{generated_map_name}/routing_map.bin"
    )
    sim_result = docker_container.exec_run(
        f"test -s /apollo/modules/map/data/{generated_map_name}/sim_map.bin"
    )

    assert routing_result.exit_code == 0
    assert sim_result.exit_code == 0
