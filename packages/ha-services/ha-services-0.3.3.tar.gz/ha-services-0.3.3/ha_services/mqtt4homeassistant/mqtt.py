import json
import logging
import socket

import paho.mqtt.client as mqtt
from bx_py_utils.anonymize import anonymize
from rich import print
from rich.pretty import pprint

from ha_services import __version__
from ha_services.cli_tools.rich_utils import human_error
from ha_services.mqtt4homeassistant.data_classes import HaMqttPayload, MqttSettings


logger = logging.getLogger(__name__)


def get_client_id():
    hostname = socket.gethostname()
    client_id = f'ha_services v{__version__} on {hostname}'
    return client_id


class OnConnectCallback:
    def __init__(self, verbosity: int):
        self.verbosity = verbosity

    def __call__(self, client, userdata, flags, rc):
        if self.verbosity:
            print(f'MQTT broker connect result code: {rc}', end=' ')

        if rc == 0:
            if self.verbosity:
                print('[green]OK')
        else:
            print('\n[red]MQTT Connection not successful!')
            print('[yellow]Please check your credentials\n')
            raise RuntimeError(f'MQTT connection result code {rc} is not 0')

        if self.verbosity:
            print(f'\t{userdata=}')
            print(f'\t{flags=}')


def get_connected_client(settings: MqttSettings, verbosity: int, timeout=10):
    client_id = get_client_id()

    if verbosity:
        print(f'\nConnect [cyan]{settings.host}:{settings.port}[/cyan] as "[magenta]{client_id}[/magenta]"', end='...')

    socket.setdefaulttimeout(timeout)  # Sadly: Timeout will not used in getaddrinfo()!
    try:
        info = socket.getaddrinfo(settings.host, settings.port)
    except socket.gaierror as err:
        human_error(
            message=f'{err}\n(Hint: Check you host/port settings)',
            title=f'[red]Error get address info from: [cyan]{settings.host}:{settings.port}[/cyan]',
            exception=err,
            exit_code=1,
        )
    else:
        if not info:
            print('[red]Resolve error: No info!')
        elif verbosity:
            print('Host/port test [green]OK')

    mqttc = mqtt.Client(client_id=client_id)
    mqttc.on_connect = OnConnectCallback(verbosity=verbosity)
    mqttc.enable_logger(logger=logger)

    if settings.user_name and settings.password:
        if verbosity:
            print(
                f'login with user: {anonymize(settings.user_name)} password:{anonymize(settings.password)}',
                end='...',
            )
        mqttc.username_pw_set(settings.user_name, settings.password)

    mqttc.connect(settings.host, port=settings.port)

    if verbosity:
        print('[green]OK')
    return mqttc


class HaMqttPublisher:
    def __init__(self, settings: MqttSettings, verbosity: int = 0, config_count: int = 10):
        self.verbosity = verbosity
        self.mqttc = get_connected_client(settings=settings, verbosity=verbosity)
        self.mqttc.loop_start()

        self.config_count = config_count
        self.send_count = 0

    def publish(self, *, topic: str, payload: dict) -> None:
        if self.verbosity:
            print('_' * 100)
            print(f'[yellow]Publish MQTT topic: [blue]{topic} [grey](Send count: {self.send_count})')
            pprint(payload)

        info: mqtt.MQTTMessageInfo = self.mqttc.publish(topic=topic, payload=json.dumps(payload))
        if self.verbosity:
            print('publish result:', info)

    def publish2homeassistant(self, *, ha_mqtt_payload: HaMqttPayload) -> None:
        log_prefix = f'{self.send_count=} ({self.config_count=})'

        if self.send_count == 0 or self.send_count % self.config_count == 0:
            logger.debug(f'{log_prefix} send {len(ha_mqtt_payload.configs)} configs')
            for config in ha_mqtt_payload.configs:
                self.publish(
                    topic=config['topic'],
                    payload=config['data'],
                )

        logger.debug(f'{log_prefix} send {len(ha_mqtt_payload.state["data"])} values')
        self.publish(
            topic=ha_mqtt_payload.state['topic'],
            payload=ha_mqtt_payload.state['data'],
        )
        self.send_count += 1
