import docker
import logging


########################################################################
class Swarm:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, base_url='unix://var/run/docker.sock', advertise_addr=''):
        """Constructor"""
        self.client = docker.DockerClient(base_url=base_url)

        try:
            logging.warning("Starting swarm...")
            if not self.client.swarm.attrs.get('ID'):
                swarm_init_response = self.client.swarm.init(advertise_addr=advertise_addr)
                logging.warning(f"Swarm started, ID: {swarm_init_response}")
            else:
                logging.warning(f"Swarm is already running, ID: {self.client.swarm.attrs.get('ID')}")
        except docker.errors.APIError as e:
            logging.warning("Error:", str(e))
            return

        self.create_networks()

    # ----------------------------------------------------------------------
    def create_networks(self):
        """"""
        self.networks = ['hci_network']
        logging.warning("Creating networks...")
        for network in self.networks:
            if network not in [n.name for n in self.client.networks.list()]:
                self.client.networks.create(network, driver="overlay")
                logging.warning(f"Created network '{network}'")

    # ----------------------------------------------------------------------
    def create_volume(self, volume_name):
        """"""
        logging.warning("Creating volumes...")
        if not volume_name in self.volumes:
            if not volume_name.endswith('-volume'):
                volume_name = f'{volume_name}-volume'
            self.client.volumes.create(name=volume_name)
        else:
            logging.warning(f"Volume '{volume_name}' already exists")

        return volume_name

    # ----------------------------------------------------------------------
    @property
    def services(self, attr='name'):
        """"""
        return [getattr(service, attr) for service in self.client.services.list()]

    # # ----------------------------------------------------------------------
    # def desribe_service(self, service, attr='name'):
        # """"""
        # return [getattr(service, attr) for service in self.client.services.list()]

    # ----------------------------------------------------------------------
    @property
    def containers(self, attr='id'):
        """"""
        return [getattr(container, attr) for container in self.client.containers.list()]

    # # ----------------------------------------------------------------------
    # def containers_get(self, attr='id'):
        # """"""
        # return [getattr(container, attr) for container in self.client.containers.list()]

    # ----------------------------------------------------------------------
    @property
    def volumes(self):
        """"""
        return [v.name for v in self.client.volumes.list() if v.name.endswith('-volume')]

    # ----------------------------------------------------------------------
    def stop_service(self, service_name):
        """"""
        service = self.client.services.get(service_name)
        service.remove()

    # ----------------------------------------------------------------------
    def stop_all_services(self):
        """"""
        for service in self.services:
            self.stop_service(service)

    # ----------------------------------------------------------------------
    def stats(self, service_name):
        """"""
        service = self.client.services.get(service_name)
        stats = []
        for task in service.tasks():
            container_id = task['Status']['ContainerStatus']['ContainerID']
            if container_id in self.containers:
                stats.append(self.client.containers.get(container_id).stats(stream=False))
        return stats

    # ----------------------------------------------------------------------
    def start_jupyter(self, service_name="jupyterlab-service", port=8888, restart=False):
        """"""
        if restart and (service_name in self.services):
            self.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in self.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        volume_name = self.create_volume(service_name)
        service = self.client.services.create(
            image="dunderlab/python311:latest",
            name=service_name,
            networks=self.networks,
            command=["jupyter", "lab", "--notebook-dir='/app'",
                     "--ip=0.0.0.0", "--port=8888",
                     "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"],
            endpoint_spec=docker.types.EndpointSpec(ports={8888: port}),
            mounts=[
                docker.types.Mount(
                    type='bind',
                    source='/var/run/docker.sock',
                    target='/var/run/docker.sock'
                ),
                docker.types.Mount(
                    target='/app',
                    source=volume_name,
                    type="volume",
                    read_only=False
                ),
            ]
        )
        return service_name in self.services

    # ----------------------------------------------------------------------
    def start_kafka(self, kafka_service_name="kafka-service",
                    zookeeper_service_name="zookeeper-service",
                    kafka_port=9092, kafka_port_external=19092,
                    zookeeper_port=2181, restart=False):
        """"""
        if restart and (kafka_service_name in self.services):
            self.stop_service(kafka_service_name)
            logging.warning(f"Restarting service '{kafka_service_name}'")

        if restart and (zookeeper_service_name in self.services):
            self.stop_service(zookeeper_service_name)
            logging.warning(f"Restarting service '{zookeeper_service_name}'")

        if not kafka_service_name in self.services:
            kafka_service = self.client.services.create(
                image="dunderlab/kafka:latest",
                # restart_policy=docker.types.RestartPolicy(condition='any'),
                name=kafka_service_name,
                networks=self.networks,
                endpoint_spec=docker.types.EndpointSpec(ports={kafka_port: kafka_port,
                                                               kafka_port_external: kafka_port_external, }),
                env=[
                    f"KAFKA_ZOOKEEPER_CONNECT={zookeeper_service_name}:{zookeeper_port}",
                    f"KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT",
                    f"KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://{kafka_service_name}:{kafka_port},PLAINTEXT_HOST://localhost:{kafka_port_external}",
                ],
            )
        else:
            logging.warning(f"Service '{kafka_service_name}' already exist")

        if not zookeeper_service_name in self.services:
            zookeeper_service = self.client.services.create(
                image="dunderlab/zookeeper:latest",
                name=zookeeper_service_name,
                networks=self.networks,
                endpoint_spec=docker.types.EndpointSpec(ports={zookeeper_port: zookeeper_port}),
                env=[
                    f"ZOOKEEPER_CLIENT_PORT={zookeeper_port}",
                ],
            )
        else:
            logging.warning(
                f"Service '{zookeeper_service_name}' already exist")

        return kafka_service_name in self.services, zookeeper_service_name in self.services

    # ----------------------------------------------------------------------
    def start_kafka_logs(self, kafka_service_name="kafka-logs-service",
                         zookeeper_service_name="zookeeper-logs-service",
                         kafka_port=9093, kafka_port_external=19093,
                         zookeeper_port=2182, restart=False):
        """"""
        return self.start_kafka(kafka_service_name, zookeeper_service_name, kafka_port, kafka_port_external, zookeeper_port, restart)

    # ----------------------------------------------------------------------
    def start_timescaledb(self, service_name="timescaledb-service", port=5432, volume_name=None, restart=False):
        """"""
        if restart and (service_name in self.services):
            self.stop_service(service_name)
            logging.warning(f"Restarting service '{service_name}'")
        elif service_name in self.services:
            logging.warning(f"Service '{service_name}' already exist")
            return

        if volume_name is None:
            volume_name = self.create_volume(service_name)
        else:
            volume_name = self.create_volume(volume_name)

        timescaledb_service = self.client.services.create(
            image="timescale/timescaledb:latest-pg15",
            name=service_name,
            networks=self.networks,
            env=[
                "POSTGRES_PASSWORD=password",
                "POSTGRES_USER=postgres",
                "POSTGRES_DB=timescaledb",
                "POSTGRES_MAX_CONNECTIONS=500"
            ],
            endpoint_spec=docker.types.EndpointSpec(ports={5432: port}),
            mounts=[
                docker.types.Mount(
                    target='/var/lib/postgresql/data',
                    source=volume_name,
                    type="volume",
                    read_only=False
                ),
            ]
        )
        return service_name in self.services

    # ----------------------------------------------------------------------
    def get_join_command(self):
        """"""
        swarm_info = self.client.info().get('Swarm')
        if swarm_info and swarm_info.get('ControlAvailable'):
            worker_join_token = self.client.swarm.attrs['JoinTokens']['Worker']
            manager_addr = swarm_info.get('RemoteManagers')[0].get('Addr')
            return f'docker swarm join --token {worker_join_token} {manager_addr}'

    # ----------------------------------------------------------------------
    def advertise_addr(self):
        """"""
        swarm_info = self.client.info().get('Swarm')
        if swarm_info and swarm_info.get('ControlAvailable'):
            # worker_join_token = self.client.swarm.attrs['JoinTokens']['Worker']
            manager_addr = swarm_info.get('RemoteManagers')[0].get('Addr')
            return manager_addr






