import logging
import time

from ha_services.cli_tools.rich_utils import human_error
from ha_services.mqtt4homeassistant.converter import values2mqtt_payload
from ha_services.mqtt4homeassistant.data_classes import HaValue, HaValues
from ha_services.mqtt4homeassistant.mqtt import HaMqttPublisher
from packaging.version import Version
from rich import print  # noqa

from inverter.api import Inverter
from inverter.constants import ERROR_STR_NO_DATA
from inverter.daily_reset import DailyProductionReset, DailyProductionResetState
from inverter.data_types import Config, InverterInfo, InverterValue
from inverter.exceptions import ReadInverterError, ReadTimeout, ValidationError


logger = logging.getLogger(__name__)


def publish_forever(*, config: Config, verbosity):
    start_time = time.monotonic()

    mqtt_settings = config.mqtt_settings
    try:
        publisher = HaMqttPublisher(settings=mqtt_settings, verbosity=verbosity, config_count=1)
    except Exception as err:
        human_error(message='given {mqtt_settings!r} is wrong?!?', exception=err)

    reset_state = DailyProductionResetState(config_path=config.config_path)

    while True:
        try:
            with Inverter(config=config) as inverter:
                inverter.connect()
                inverter_info: InverterInfo = inverter.inv_sock.inverter_info

                with DailyProductionReset(reset_state, inverter, config) as daily_production_reset:

                    try:
                        values = []
                        for value in inverter:
                            assert isinstance(value, InverterValue), f'{value!r}'

                            ha_value = value.value
                            if ha_value == ERROR_STR_NO_DATA:
                                # Don't send a MQTT message if one of the values are missing:
                                raise ReadInverterError(f'Missing data for {value.name}')
                            elif isinstance(value.value, Version):
                                ha_value = str(value.value)

                            daily_production_reset(value)

                            values.append(
                                HaValue(
                                    name=value.name,
                                    value=ha_value,
                                    device_class=value.device_class,
                                    state_class=value.state_class,
                                    unit=value.unit,
                                )
                            )
                    except ValidationError as err:
                        print(f'[red]Skip send values: {err}')
                    except ReadInverterError as err:
                        print(f'[red]{err}')
                    else:
                        values.append(
                            HaValue(
                                name='Loop Running Time',
                                value=int(time.monotonic() - start_time),
                                device_class='',
                                state_class='measurement',
                                unit='sec.',
                            )
                        )

                        values = HaValues(
                            device_name=str(inverter_info.serial),
                            values=values,
                            prefix='homeassistant',
                            component='sensor',
                        )
                        ha_mqtt_payload = values2mqtt_payload(values=values, name_prefix='inverter')
                        publisher.publish2homeassistant(ha_mqtt_payload=ha_mqtt_payload)
        except ReadTimeout as err:
            print(f'[red]{err}')
        except BaseException as err:
            print(f'[red]{err}')
            logger.exception('Unexpected error: %s', err)

        print('Wait', end='...')
        for i in range(10, 1, -1):
            time.sleep(1)
            print(i, end='...')
