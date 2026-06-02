import uuid
from typing import Iterator

import docker
from docker.errors import NotFound
import pytest

from apollo.ApolloContainer import ApolloContainer
import config


@pytest.fixture
def apollo_container() -> Iterator[ApolloContainer]:
    """Provide an Apollo container and remove it after the test."""
    username = f'DOPPELTEST_TEST_{uuid.uuid4().hex[:8]}'
    container = ApolloContainer(config.APOLLO_ROOT, username)
    yield container

    try:
        docker_container = docker.from_env().containers.get(
            container.container_name
        )
    except NotFound:
        return

    docker_container.remove(force=True)


def test_stop_and_remove_container(apollo_container: ApolloContainer) -> None:
    """Start, stop, and remove an Apollo Docker container."""
    apollo_container.start_instance()
    assert apollo_container.is_running()

    apollo_container.stop_container()
    assert not apollo_container.is_running()

    apollo_container.remove_container()
    with pytest.raises(NotFound):
        docker.from_env().containers.get(apollo_container.container_name)
