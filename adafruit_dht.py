# The MIT License (MIT)
#
# Copyright (c) 2017 Mike McWethy for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
:mod:`adafruit_dhtlib`
======================

CircuitPython support for the DHT11 and DHT22 temperature and humidity devices.

* Author(s): Mike McWethy
"""

import array
import time
try:
    import pulseio
except ImportError as excpt:
    print("adafruit_dht requires the pulseio library, but it failed to load."+
        "  Note that CircuitPython does not support pulseio on all boards.")
    raise excpt

class DHTBase:
    """ base support for DHT11 and DHT22 devices
    """

    __hiLevel = 51

    def __init__(self, dht11, pin, trig_wait):
        """
        :param boolean dht11: True if device is DHT11, otherwise DHT22.
        :param ~board.Pin pin: digital pin used for communication
        :param int trig_wait: length of time to hold trigger in LOW state (microseconds)
        """
        self._dht11 = dht11
        self._pin = pin
        self._trig_wait = trig_wait
        self._last_called = 0
        self._humidity = None
        self._temperature = None


    def _pulses_to_binary(self, pulses, start, stop):
        """Takes pulses, a list of transition times, and converts
        them to a 1's or 0's.  The pulses array contains the transition times.
        pulses starts with a low transition time followed by a high transistion time.
        then a low followed by a high and so on.  The low transition times are
        ignored.  Only the high transition times are used.  If the high
        transition time is greater than __hiLevel, that counts as a bit=1, if the
        high transition time is less that __hiLevel, that counts as a bit=0.

        start is the starting index in pulses to start converting

        stop is the index to convert upto but not including

        Returns an integer containing the converted 1 and 0 bits
        """

        binary = 0
        hi_sig = False
        for bit_inx in range(start, stop):
            if hi_sig:
                bit = 0
                if pulses[bit_inx] > self.__hiLevel:
                    bit = 1
                binary = binary<<1 | bit

            hi_sig = not hi_sig

        return binary

    def _get_pulses(self):
        """ _get_pulses implements the communication protcol for
        DHT11 and DHT22 type devices.  It sends a start signal
        of a specific length and listens and measures the
        return signal lengths.

        return pulses (array.array uint16) contains alternating high and low
        transition times starting with a low transition time.  Normally
        pulses will have 81 elements for the DHT11/22 type devices.
        """
        pulses = array.array('H')
        tmono = time.monotonic()

        # create the PulseIn object using context manager
        with pulseio.PulseIn(self._pin, 81, True) as pulse_in:

            # The DHT type device use a specialize 1-wire protocol
            # The microprocessor first sends a LOW signal for a
            # specific length of time.  Then the device sends back a
            # series HIGH and LOW signals.  The length the HIGH signals
            # represents the device values.
            pulse_in.pause()
            pulse_in.clear()
            pulse_in.resume(self._trig_wait)

            # loop until we get the return pulse we need or
            # time out after 1/2 seconds
            while True:
                if len(pulse_in) >= 80:
                    break
                if time.monotonic()-tmono > 0.5: # time out after 1/2 seconds
                    break

            pulse_in.pause()
            while len(pulse_in):
                pulses.append(pulse_in.popleft())
            pulse_in.resume()

        return pulses

    def measure(self):
        """ measure runs the communications to the DHT11/22 type device.
            if successful, the class properties temperature and humidity will
            return the reading returned from the device.

            Raises RuntimeError exception for checksum failure and for insuffcient
            data returned from the device (try again)
        """
        if time.monotonic()-self._last_called > 0.5:
            self._last_called = time.monotonic()

            pulses = self._get_pulses()
            ##print(pulses)

            if len(pulses) >= 80:
                buf = array.array('B')
                for byte_start in range(0, 80, 16):
                    buf.append(self._pulses_to_binary(pulses, byte_start, byte_start+16))
                #print(buf)

                # humidity is 2 bytes
                if self._dht11:
                    self._humidity = buf[0]
                else:
                    self._humidity = ((buf[0]<<8) | buf[1]) / 10

                # tempature is 2 bytes
                if self._dht11:
                    self._temperature = buf[2]
                else:
                    self._temperature = ((buf[2]<<8) | buf[3]) / 10

                # calc checksum
                chk_sum = 0
                for b in buf[0:4]:
                    chk_sum += b

                # checksum is the last byte
                if chk_sum & 0xff != buf[4]:
                    # check sum failed to validate
                    raise RuntimeError("Checksum did not validate. Try again.")
                    #print("checksum did not match. Temp: {} Humidity: {} Checksum:{}".format(self._temperature,self._humidity,bites[4]))

                # checksum matches
                #print("Temp: {} C Humidity: {}% ".format(self._temperature, self._humidity))

            else:
                raise RuntimeError("A full buffer was not returned.  Try again.")
                #print("did not get a full return.  number returned was: {}".format(len(r)))

    @property
    def temperature(self):
        """ temperature current reading.  It makes sure a reading is available

            Raises RuntimeError exception for checksum failure and for insuffcient
            data returned from the device (try again)
        """
        self.measure()
        return self._temperature

    @property
    def humidity(self):
        """ humidity current reading. It makes sure a reading is available

            Raises RuntimeError exception for checksum failure and for insuffcient
            data returned from the device (try again)
        """
        self.measure()
        return self._humidity

class DHT11(DHTBase):
    """ Support for DHT11 device.

        :param ~board.Pin pin: digital pin used for communication
    """
    def __init__(self, pin):
        super().__init__(True, pin, 18000)


class DHT22(DHTBase):
    """ Support for DHT22 device.

        :param ~board.Pin pin: digital pin used for communication
    """
    def __init__(self, pin):
        super().__init__(False, pin, 1000)
