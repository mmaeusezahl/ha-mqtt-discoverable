#
#    Copyright 2022-2024 Joe Block <jpb@unixorn.net>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
import pytest

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo


@pytest.fixture(params=["°C", "kWh"])
def sensor(request) -> Sensor:
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SensorInfo(name="test", unit_of_measurement=request.param)
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return Sensor(settings)


def test_required_config():
    mqtt_settings = Settings.MQTT(host="localhost")
    sensor_info = SensorInfo(name="test")
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    sensor = Sensor(settings)
    assert sensor is not None


def test_generate_config(sensor: Sensor):
    config = sensor.generate_config()

    assert config is not None
    # If we have defined a custom unit of measurement, check that is part of the
    # output config
    if sensor._entity.unit_of_measurement:
        assert config["unit_of_measurement"] == sensor._entity.unit_of_measurement


def test_update_state(sensor: Sensor):
    sensor.set_state(1)
