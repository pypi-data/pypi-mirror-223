# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`adt7410`
================================================================================

MicroPython Driver for the Analog Devices ADT7410 Temperature Sensor


* Author(s): Jose D. Montoya


"""

import time
from collections import namedtuple
from micropython import const
from micropython_adt7410.i2c_helpers import CBits, RegisterStruct


__version__ = "0.2.0"
__repo__ = "https://github.com/jposada202020/MicroPython_ADT7410.git"


_REG_WHOAMI = const(0xB)
_TEMP = const(0x00)
_STATUS = const(0x02)
_CONFIGURATION = const(0x03)
_TEMP_HIGH = const(0x04)
_TEMP_LOW = const(0x06)
_TEMP_CRITICAL = const(0x08)
_TEMP_HYSTERESIS = const(0x0A)
_RESET = const(0x2F)

CONTINUOUS = const(0b00)
ONE_SHOT = const(0b01)
SPS = const(0b10)
SHUTDOWN = const(0b11)
operation_mode_values = (CONTINUOUS, ONE_SHOT, SPS, SHUTDOWN)

LOW_RESOLUTION = const(0b0)
HIGH_RESOLUTION = const(0b1)
resolution_mode_values = (LOW_RESOLUTION, HIGH_RESOLUTION)

COMP_DISABLED = const(0b0)
COMP_ENABLED = const(0b1)
comparator_mode_values = (COMP_DISABLED, COMP_ENABLED)

AlertStatus = namedtuple("AlertStatus", ["high_alert", "low_alert", "critical_alert"])


class ADT7410:
    """Driver for the ADT7410 Sensor connected over I2C.

    The ADT7410 is a high accuracy digital temperature sensor. it has
    a 13-bit ADC to monitor and digitize the temperature to a
    0.0625°C resolution.

    The ADC resolution, by default, is set to 13 bits (0.0625°C).
    This can be changed to 16 bits (0.0078°C) by :attr:`resolution_mode`

    The ADT7410 is rated for operation over the -55°C to +150°C temperature
    range

    In normal mode, the ADT7410 runs an automatic conversion
    sequence. During this automatic conversion sequence, a conversion
    takes 240 ms to complete and the ADT7410 is continuously
    converting.


    :param ~machine.I2C i2c: The I2C bus the ADT7410 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x48`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`ADT7410` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_adt7410 import adt7410

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        adt = adt7410.ADT7410(i2c)

    Now you have access to the attributes

    .. code-block:: python

        temp = adt.temperature

    """

    _device_id = RegisterStruct(_REG_WHOAMI, "B")
    _temperature = RegisterStruct(_TEMP, ">h")
    _temperature_high = RegisterStruct(_TEMP_HIGH, ">h")
    _temperature_low = RegisterStruct(_TEMP_LOW, ">h")
    _temperature_critical = RegisterStruct(_TEMP_CRITICAL, ">h")
    _temperature_hysteresis = RegisterStruct(_TEMP_HYSTERESIS, "B")
    _status = RegisterStruct(_STATUS, "B")

    # Configuration register
    _resolution_mode = CBits(1, _CONFIGURATION, 7)
    _operation_mode = CBits(2, _CONFIGURATION, 5)
    _comparator_mode = CBits(1, _CONFIGURATION, 4)

    # Status Register
    _critical_alert = CBits(1, _STATUS, 6)
    _high_alert = CBits(1, _STATUS, 5)
    _low_alert = CBits(1, _STATUS, 4)

    def __init__(self, i2c, address: int = 0x48) -> None:
        self._i2c = i2c
        self._address = address

        if self._device_id != 0xCB:
            raise RuntimeError("Failed to find the ADT7410 sensor")

    @property
    def operation_mode(self) -> str:
        """
        Sensor operation_mode

        Continuous Mode
        ---------------

        In continuous conversion mode, the read operation provides the most recent
        converted result.

        One Shot Mode
        --------------

        When one-shot mode is enabled, the ADT7410 immediately
        completes a conversion and then goes into shutdown mode. The
        one-shot mode is useful when one of the circuit design priorities is
        to reduce power consumption.

        SPS Mode
        ----------

        In this mode, the part performs one measurement per second.
        A conversion takes only 60 ms, and it remains in the idle state
        for the remaining 940 ms period

        Shutdown Mode
        ---------------
        The ADT7410 can be placed in shutdown mode, the entire IC is
        shut down and no further conversions are initiated until the
        ADT7410 is taken out of shutdown mode. The conversion result from the
        last conversion prior to shut down can still be read from the
        ADT7410 even when it is in shutdown mode. When the part is
        taken out of shutdown mode, the internal clock is started and a
        conversion is initiated

        +--------------------------------+------------------+
        | Mode                           | Value            |
        +================================+==================+
        | :py:const:`adt7410.CONTINUOUS` | :py:const:`0b00` |
        +--------------------------------+------------------+
        | :py:const:`adt7410.ONE_SHOT`   | :py:const:`0b01` |
        +--------------------------------+------------------+
        | :py:const:`adt7410.SPS`        | :py:const:`0b10` |
        +--------------------------------+------------------+
        | :py:const:`adt7410.SHUTDOWN`   | :py:const:`0b11` |
        +--------------------------------+------------------+
        """
        values = (
            "CONTINUOUS",
            "ONE_SHOT",
            "SPS",
            "SHUTDOWN",
        )
        return values[self._operation_mode]

    @operation_mode.setter
    def operation_mode(self, value: int) -> None:
        if value not in operation_mode_values:
            raise ValueError("Value must be a valid operation_mode setting")
        self._operation_mode = value
        time.sleep(0.24)

    @property
    def temperature(self) -> float:
        """
        Temperature in Celsius
        In normal mode, the ADT7410 runs an automatic conversion
        sequence. During this automatic conversion sequence, a conversion
        takes 240 ms to complete and the ADT7410 is continuously
        converting. This means that as soon as one temperature conversion
        is completed, another temperature conversion begins.
        On power-up, the first conversion is a fast conversion, taking
        typically 6 ms. Fast conversion temperature accuracy is typically
        within ±5°C.
        The measured temperature value is compared with a critical
        temperature limit, a high temperature limit, and a low temperature
        limit. If the measured value
        exceeds these limits, the INT pin is activated; and if it exceeds the
        :attr:`critical_temp` limit, the CT pin is activated.
        """
        return self._temperature / 128

    @property
    def resolution_mode(self) -> str:
        """
        Sensor resolution_mode

        +-------------------------------------+-----------------+
        | Mode                                | Value           |
        +=====================================+=================+
        | :py:const:`adt7410.LOW_RESOLUTION`  | :py:const:`0b0` |
        +-------------------------------------+-----------------+
        | :py:const:`adt7410.HIGH_RESOLUTION` | :py:const:`0b1` |
        +-------------------------------------+-----------------+
        """
        values = (
            "LOW_RESOLUTION",
            "HIGH_RESOLUTION",
        )
        return values[self._resolution_mode]

    @resolution_mode.setter
    def resolution_mode(self, value: int) -> None:
        if value not in resolution_mode_values:
            raise ValueError("Value must be a valid resolution_mode setting")
        self._resolution_mode = value

    @property
    def alert_status(self):
        """The current triggered status of the high and low temperature alerts as a AlertStatus
        named tuple with attributes for the triggered status of each alert.

        .. code-block :: python

            import time
            from machine import Pin, I2C
            from micropython_adt7410 import adat7410

            i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
            adt = adt7410.ADT7410(i2c)

            tmp.low_temperature = 20
            tmp.high_temperature = 23
            tmp.critical_temperature = 30

            print(f"High limit: {tmp.high_temperature}")
            print(f"Low limit: {tmp.low_temperature}")
            print(f"Critical limit: {tmp.critical_temperature}")

            adt.comparator_mode = adt7410.COMP_ENABLED

            while True:
                print(f"Temperature: {adt.temperature:.2f}°C")
                alert_status = tmp.alert_status
                if alert_status.high_alert:
                    print("Temperature above high set limit!")
                if alert_status.low_alert:
                    print("Temperature below low set limit!")
                if alert_status.critical_alert:
                    print("Temperature above critical set limit!")
                time.sleep(1)

        """

        return AlertStatus(
            high_alert=self._high_alert,
            low_alert=self._low_alert,
            critical_alert=self._critical_alert,
        )

    @property
    def comparator_mode(self) -> str:
        """
        Sensor comparator_mode
        In comparator mode, the INT pin returns to its inactive status
        when the temperature drops below the
        :attr:`high_temperature` - :attr:`hysteresis_temperature` limit or
        rises above the :attr:`low_temperature` + :attr:`hysteresis_temperature`
        limit.
        Putting the ADT7410 into shutdown mode does not reset the
        INT state in comparator mode

        +-----------------------------------+-----------------+
        | Mode                              | Value           |
        +===================================+=================+
        | :py:const:`adt7410.COMP_DISABLED` | :py:const:`0b0` |
        +-----------------------------------+-----------------+
        | :py:const:`adt7410.COMP_ENABLED`  | :py:const:`0b1` |
        +-----------------------------------+-----------------+
        """
        values = (
            "COMP_DISABLED",
            "COMP_ENABLED",
        )
        return values[self._comparator_mode]

    @comparator_mode.setter
    def comparator_mode(self, value: int) -> None:
        if value not in comparator_mode_values:
            raise ValueError("Value must be a valid comparator_mode setting")
        self._comparator_mode = value

    @property
    def high_temperature(self) -> int:
        """
        High temperature limit value in Celsius
        When the temperature goes above the :attr:`high_temperature`,
        and if :attr:`comparator_mode` is selected. The :attr:`alert_status`
        high_alert clears to 0 when the status register is read and/or when
        the temperature measured goes back below the limit set in the set point
        :attr:`high_temperature` + :attr:`hysteresis_temperature`

        The INT pin is activated if an over temperature event occur
        The default setting is 64°C

        """
        return self._temperature_high // 128

    @high_temperature.setter
    def high_temperature(self, value: int) -> None:
        if value not in range(-55, 151, 1):
            raise ValueError("Temperature should be between -55°C and 150°C")
        self._temperature_high = value * 128

    @property
    def low_temperature(self) -> int:
        """
        Low temperature limit value in Celsius.
        When the temperature goes below the :attr:`low_temperature`,
        and if :attr:`comparator_mode` is selected. The :attr:`alert_status`
        low_alert clears to 0 when the status register is read and/or when
        the temperature measured goes back above the limit set in the set point
        :attr:`low_temperature` + :attr:`hysteresis_temperature`

        The INT pin is activated if an under temperature event occur
        The default setting is 10°C
        """
        return self._temperature_low // 128

    @low_temperature.setter
    def low_temperature(self, value: int) -> None:
        if value not in range(-55, 151, 1):
            raise ValueError("Temperature should be between -55°C and 150°C")
        self._temperature_low = value * 128

    @property
    def critical_temperature(self) -> int:
        """
        Critical temperature limit value in Celsius
        When the temperature goes above the :attr:`critical_temperature`,
        and if :attr:`comparator_mode` is selected. The :attr:`alert_status`
        critical_alert clears to 0 when the status register is read and/or when
        the temperature measured goes back below the limit set in
        :attr:`critical_temperature` + :attr:`hysteresis_temperature`

        The INT pin is activated if a critical over temperature event occur
        The default setting is 147°C
        """
        return self._temperature_critical // 128

    @critical_temperature.setter
    def critical_temperature(self, value: int) -> None:
        if value not in range(-55, 151, 1):
            raise ValueError("Temperature should be between -55°C and 150°C")
        self._temperature_critical = value * 128

    @property
    def hysteresis_temperature(self) -> float:
        """
        Hysteresis temperature limit value in Celsius for the
        :attr:`critical_temperature`, :attr:`high_temperature` and
        :attr:`low_temperature` limits
        """
        return self._temperature_hysteresis

    @hysteresis_temperature.setter
    def hysteresis_temperature(self, value: int) -> None:
        if value not in range(0, 16, 1):
            raise ValueError("Temperature should be between 0°C and 15°C")
        self._temperature_hysteresis = value

    def reset(self) -> None:
        """Reset the sensor to default values"""
        self._i2c.writeto(self._address, bytes([_RESET]))
        time.sleep(0.0002)
