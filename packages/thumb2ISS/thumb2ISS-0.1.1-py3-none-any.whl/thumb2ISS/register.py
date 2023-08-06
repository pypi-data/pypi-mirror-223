#
# Copyright (c) 2023 Thibaut Zeissloff.
#
# This file is part of Thumb2ISS
# (see https://github.com/TZe-0xff/thumb2ISS).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#
import struct

class Register:
    def __init__(self, initial_value):
        if type(initial_value) == Register:
            self.ival = initial_value.ival
            self.bval = initial_value.bval
        elif type(initial_value) == bytes:
            self.bval = initial_value
            self.ival = struct.unpack('<l', initial_value)[0]
        elif type(initial_value) == str:
            self.ival = int(initial_value, 0)
            self.bval = struct.pack('<l', self.ival)
        else:
            uval = int(initial_value) & 0xffffffff
            self.bval = struct.pack('<L', uval)
            self.ival = struct.unpack('<l', self.bval)[0]
        self._msb = 31

    @staticmethod
    def __get_ival(other):
        if type(other) == Register:
            other_ival = other.ival
        elif type(other) == bytes:
            other_ival = struct.unpack('<l', other)[0]
        elif type(other) == str:
            other_ival = int(other, 0)
        else:
            other_ival = int(other)
        return other_ival


    def __add__(self, other): # +
        return Register(self.ival + self.__get_ival(other))

    def __sub__(self, other): # –
        return Register(self.ival - self.__get_ival(other))

    def __and__(self, other): # &
        return Register(self.ival & self.__get_ival(other))

    def __or__(self, other): # |
        return Register(self.ival | self.__get_ival(other))

    def __xor__(self, other): # ^
        return Register(self.ival ^ self.__get_ival(other))


    def __eq__(self, other): # ==
        return self.ival == self.__get_ival(other)

    def __ne__(self, other): # !=
        return self.ival != self.__get_ival(other)
