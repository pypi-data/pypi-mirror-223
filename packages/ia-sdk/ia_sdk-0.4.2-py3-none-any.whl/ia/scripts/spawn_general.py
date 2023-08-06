import docker
import docker.errors as de
import logging


logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S')
logger = logging.getLogger(__name__)


def spawn_container(container_name: str,
                    api_key: str,
                    ports: dict,
                    docker_image: str,
                    privileged: bool = False,
                    volumes: dict = None,
                    env: dict = None):

    client = docker.from_env()

    if env is None:
        env = {}

    env['API_KEY'] = api_key

    if volumes is None:
        volumes = {}

    try:
        client.containers.run(image=docker_image,
                              init=True,
                              ports=ports,
                              privileged=privileged,
                              name=container_name,
                              volumes=volumes,
                              environment=env,
                              detach=True)

    except de.ImageNotFound as e:
        logger.error(f'Image not found: {str(e)}')
        raise Exception(f'Failed to start Container: {str(e)}')

    except de.APIError as e:
        logger.error(f'Docker API Error: {str(e)}')
        raise Exception(f'Failed to start Container: {str(e)}')

    return True


def kill_container(container_name: str) -> bool:

    client = docker.from_env()

    try:
        logger.debug(f"attempting to remove container {container_name}")
        tf = client.containers.get(container_name)
        # tf.kill()
        tf.remove(force=True)
    except de.NotFound as e:
        logger.error(
            f'Container {container_name} not found: {str(e)}')
        return True
    except de.APIError as e:
        logger.error(f'Docker API Error: {str(e)}')
        raise Exception(f'Failed to kill container {str(e)}')
    return True


def connect_networks_container(networks: list, container_name: str):
    client = docker.from_env()

    try:
        container = client.containers.get(container_name)

        docker_networks = client.networks.list(names=networks)
        for net in docker_networks:
            logger.info(f'Connecting to {net.name}')
            try:
                net.connect(container)
            except de.APIError as e:
                logger.error(f'Docker API Error: {str(e)}')
                pass  # tf already connected on network
    except de.NotFound as e:
        logger.error(
            f'Container {container_name} not found: {str(e)}')
        return False
    except de.APIError as e:
        logger.error(f'Docker API Error: {str(e)}')
        raise Exception(f'docker API Error: {str(e)}')

    return True

    pass
