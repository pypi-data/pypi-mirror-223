# SPDX-FileCopyrightText: 2019 Bryan Siepert for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`pct2075`
================================================================================

MciroPython Driver for the NXP Semiconductors Temperature Sensor


* Author(s): Bryan Siepert,Jose D. Montoya


"""

from micropython import const
from micropython_pct2075.i2c_helpers import CBits, RegisterStruct

REGISTER_TEMP = const(0)  # Temperature register (read-only)
REGISTER_CONFIG = const(1)  # Configuration register
REGISTER_THYST = const(2)  # Hysterisis register
REGISTER_TOS = const(3)  # OS register
REGISTER_TIDLE = const(4)  # Measurement idle time register

COMPARATOR = const(0b0)
INTERRUPT = const(0b1)
operation_mode_values = (COMPARATOR, INTERRUPT)


__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_PCT2075.git"


class PCT2075:
    """Driver for the PCT2075 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the PCT2075 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x69`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`PCT2075` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_pct2075 import pct2075

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        pct2075 = pct2075.PCT2075(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    _temperature = RegisterStruct(REGISTER_TEMP, ">h")
    _operation_mode = CBits(1, REGISTER_CONFIG, 1)

    shutdown = CBits(1, REGISTER_CONFIG, 0)

    _fault_queue_length = CBits(2, REGISTER_CONFIG, 3)
    _high_temperature_threshold = RegisterStruct(REGISTER_TOS, ">h")
    _temp_hysteresis = RegisterStruct(REGISTER_THYST, ">h")
    _idle_time = CBits(5, REGISTER_TIDLE, 0)
    high_temp_active_high = CBits(1, REGISTER_CONFIG, 2)
    """Sets the alert polarity. When False the INT pin will be tied to ground when an alert is
    triggered. If set to True it will be disconnected from ground when an alert is triggered."""

    def __init__(self, i2c, address: int = 0x37) -> None:
        self._i2c = i2c
        self._address = address

    @property
    def temperature(self) -> float:
        """Returns the current temperature in degrees Celsius.
        Resolution is 0.125 Celsius"""
        return (self._temperature >> 5) * 0.125

    @property
    def high_temperature_threshold(self) -> float:
        """The temperature in degrees celsius that will trigger an alert on the INT pin if it is
        exceeded. Resolution is 0.5 Celsius"""
        return (self._high_temperature_threshold >> 7) * 0.5

    @high_temperature_threshold.setter
    def high_temperature_threshold(self, value: float) -> None:
        self._high_temperature_threshold = int(value * 2) << 7

    @property
    def temperature_hysteresis(self) -> float:
        """The temperature hysteresis value defines the bottom
        of the temperature range in degrees Celsius in which
        the temperature is still considered high.
        :attr:`temperature_hysteresis` must be lower than
        :attr:`high_temperature_threshold`.
        Resolution is 0.5 degrees Celsius
        """
        return (self._temp_hysteresis >> 7) * 0.5

    @temperature_hysteresis.setter
    def temperature_hysteresis(self, value: float) -> None:
        if value >= self.high_temperature_threshold:
            raise ValueError(
                "temperature_hysteresis must be less than high_temperature_threshold"
            )
        self._temp_hysteresis = int(value * 2) << 7

    @property
    def delay_between_measurements(self) -> int:
        """The amount of time between measurements made by the sensor in milliseconds. The value
        must be between 100 and 3100 and a multiple of 100"""
        return self._idle_time * 100

    @delay_between_measurements.setter
    def delay_between_measurements(self, value: int) -> None:
        if value > 3100 or value < 100 or value % 100 > 0:
            raise ValueError(
                "delay_between_measurements must be >= 100 or <= 3100 and a multiple of 100"
            )
        self._idle_time = int(value / 100)

    @property
    def operation_mode(self) -> str:
        """
        Sensor operation_mode
        Sets the alert mode. In comparator mode, the sensor acts like a thermostat and will activate
        the INT pin according to `high_temp_active_high` when an alert is triggered.
        The INT pin will be deactivated when the temperature falls below
        :attr:`temperature_hysteresis`.
        In interrupt mode the INT pin is activated once when a temperature fault
        is detected, and once more when the temperature falls below
        :attr:`temperature_hysteresis`. In interrupt mode, the alert is cleared by
        reading a property

        +--------------------------------+-----------------+
        | Mode                           | Value           |
        +================================+=================+
        | :py:const:`pct2075.COMPARATOR` | :py:const:`0b0` |
        +--------------------------------+-----------------+
        | :py:const:`pct2075.INTERRUPT`  | :py:const:`0b1` |
        +--------------------------------+-----------------+
        """
        values = ("COMPARATOR", "INTERRUPT")
        return values[self._operation_mode]

    @operation_mode.setter
    def operation_mode(self, value: int) -> None:
        if value not in operation_mode_values:
            raise ValueError("Value must be a valid operation_mode setting")
        self._operation_mode = value
