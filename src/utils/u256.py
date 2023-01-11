"""
File containing the U256 class and its associated logic
"""

from utils.exceptions import *

class U256:

    def __init__(self, value: int):

        if type(value) != int:
            raise U256InvalidType(value)

        if value < 0 or value > 2**256 - 1:
            raise U256OutOfBounds(value)
        
        self._value = value

    def to_binary_string(self) -> str:
        # Convert to Binary String
        temp_bin_value = bin(self._value)
        # Delete prefix
        temp_bin_value = temp_bin_value[2:]
        # Sign extend
        chars_needed = 256 - len(temp_bin_value)
        for i in range(chars_needed):
            temp_bin_value = "0" + temp_bin_value

        return temp_bin_value

    def to_hex_string(self) -> str:
        # Convert to Hex Value
        temp_hex_value = hex(self._value)
        # Delete prefix
        temp_hex_value = temp_hex_value[2:]
        # Sign Extend
        chars_needed = 64 - len(temp_hex_value)
        for i in range(chars_needed):
            temp_hex_value = "0" + temp_hex_value

        return temp_hex_value

    def __str__(self):
        return self.to_hex_string()

    def to_int(self) -> int:

        return self._value

    def get_bit_length(self) -> int:

        # Convert number to binary
        binary_value = bin(self._value)
        binary_value = binary_value[2:]

        return len(binary_value)

    def to_signed_int(self) -> int:
        """
        Returns two's complement interpretation of underlying U256 binary representation
        """

        if self.to_binary_string()[0] == '0': # If already nonnegative
            return self._value
        else: # MSB indicates negative value
            value = 0
            msb_exp = 255
            for bit in self.to_binary_string():
                if msb_exp == 255 and bit == '1': 
                    value -= 2 ** msb_exp
                elif bit == '1':
                    value += 2 ** msb_exp
                msb_exp -= 1
            return value

    @staticmethod
    def from_signed_integer(value: int):
        """
        Given a signed integer, if value is nonnegative, then this function
        defaults to the U256 initializer. If value is negative, then function
        first treats value as a nonnegative value, gets the binary version of
        it, and then converts it to a negative binary represenation via two's
        complement conversion.
        """
        if value >= 0:
            return U256(value)
        elif value < -(2 ** 128): # If value is out of bounds for conversion
            raise U256OutOfBounds(value)
        else: # Conversion is possible
            abs_val = abs(value)
            abs_val_bin = U256(abs_val).to_binary_string()
            abs_val_bin_lst = list(abs_val_bin)
            # Flip bits
            for i in range(len(abs_val_bin_lst)):
                if abs_val_bin_lst[i] == '0':
                    abs_val_bin_lst[i] = '1' # FIX
                else: # Char is '1'
                    abs_val_bin_lst[i] = '0' # FIX
            # Now 'add 1'
            temp = 1
            for i in range(len(abs_val_bin_lst) - 1, -1, -1): # LOOP BACKWARDS   

                if int(abs_val_bin_lst[i]) + temp == 2:
                    abs_val_bin[i] = '0' # FIX
                elif int(abs_val_bin_lst[i]) + temp == 1:
                    temp = 0
                    abs_val_bin_lst[i] = '1' # FIX

            converted_value = int("".join(abs_val_bin_lst), 2)
            return U256(converted_value)

    @staticmethod
    def add(a, b):
        """
        Return U256 object representing the sum of the arguments passed through
        """

        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()

        return U256((a._value + b._value) % (2**256)) 

    @staticmethod
    def mul(a, b):
        """
        Returns U256 object representing the product of the arguments passed through
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()

        return U256((a._value * b._value) % (2**256))

    @staticmethod
    def sub(a, b):
        """
        Returns U256 object representing the difference of the arguments passed through
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()

        return U256((a._value - b._value) % (2**256))

    @staticmethod
    def div(a, b):
        """
        Returns U256 object representing the difference of the arguments passed through
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()

        if (b._value == 0):
            return U256(0)

        return U256(a // b)

    @staticmethod
    def mod(a, b):
        """
        Returns U256 object representing the result a mod b
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()

        return U256(a % b)

    @staticmethod
    def addmod(a, b, N):
        """
        Returns U256 object representing the result of (a + b) mod N
        """
        if not isinstance(a, U256) or not isinstance(b, U256) or not isinstance(N, U256):
            raise U256InvalidType()
        
        return U256((a + b) % N)

    @staticmethod
    def sdiv(a, b):
        """
        Returns U256 object representing the division of the arguments passed
        through
        
        Temporarily utilizes arguments as signed integers
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()

        signed_a = a.to_signed_int()
        signed_b = b.to_signed_int()

        return U256.from_signed_integer(signed_a // signed_b)

    @staticmethod
    def sign_extend(b, x):
        """
        Returns U256 object representing the result of sign extending

        'Sign extends x from (b + 1) * 8 bits to 256 bits.'

        Temporarily utilizes arguments as signed integers
        """
        if not isinstance(b, U256) or not isinstance(x, U256):
            raise U256InvalidType()

        # First grab the rightmost bits based on b
        binary_x = x.to_binary_string()
        bits_to_grab = (b.to_int() + 1) * 8
        sliced_binary = binary_x[256 - bits_to_grab:]
        msb = sliced_binary[0]
        if msb == '0': # Sign extend with 0s
            padded_bits = '0' * (256 - bits_to_grab)
        else: # Sign extend with 1s
            padded_bits = '1' * (256 - bits_to_grab)
        new_val = int(padded_bits + sliced_binary, 2)
        return U256(new_val)

    @staticmethod
    def smod(a, b):
        """
        Returns U256 object representing the result a % b with sign preserved

        Temporarily utilizes arguments as signed integers
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        signed_a = a.to_signed_int()
        signed_b = b.to_signed_int()

        return U256.from_signed_integer(signed_a % signed_b)

    @staticmethod
    def mulmod(a, b, N):
        """
        Returns U256 object representing the result (a * b) % N
        """
        if not isinstance(a, U256) or not isinstance(b, U256) or not isinstance(N, U256):
            raise U256InvalidType()

        return U256((a.to_int() * b.to_int()) % N.to_int())

    @staticmethod
    def exp(a, b):
        """
        Returns U256 object representing the result of a^b
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        return U256((a ** b) % (2 ** 256))

    @staticmethod
    def lt(a, b):
        """
        Returns U256 object representing the result of a < b (UINT)
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        if not a.to_int() < b.to_int():
            return U256(0)
        else:
            return U256(1)

    @staticmethod
    def gt(a, b):
        """
        Returns U256 object representing the result of a > b (UINT)
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        if not a.to_int() > b.to_int():
            return U256(0)
        else:
            return U256(1)

    @staticmethod
    def slt(a, b):
        """
        Returns U256 object representing the result of a < b (SINT) 
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        signed_a = U256.to_signed_int()
        signed_b = U256.to_signed_int()

        if not signed_a < signed_b:
            return U256(0)
        else:
            return U256(1)

    @staticmethod
    def sgt(a, b):
        """
        Returns U256 object representing the result of a > b (SINT)
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        signed_a = U256.to_signed_int()
        signed_b = U256.to_signed_int()

        if not signed_a > signed_b:
            return U256(0)
        else:
            return U256(1)

    @staticmethod
    def eq(a, b):
        """
        Returns U256 object representing the result of a == b
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        if a.to_int() == b.to_int():
            return U256(1)
        else:
            return U256(0)

    @staticmethod
    def is_zero(a):
        """
        Returns U256 object representing the result of a == 0
        """
        if not isinstance(a, U256):
            raise U256InvalidType()
        
        if a.to_int() == 0:
            return U256(1)
        else:
            return U256(0)

    @staticmethod
    def bitwise_and(a, b):
        """
        Returns U256 object representing the result of a & b
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        return U256(a.to_int() & b.to_int())

    @staticmethod
    def bitwise_or(a, b):
        """
        Returns U256 object representing the result of a | b
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        return U256(a.to_int() | b.to_int())

    @staticmethod
    def bitwise_xor(a, b):
        """
        Returns U256 object representing the result of a ^ b
        """
        if not isinstance(a, U256) or not isinstance(b, U256):
            raise U256InvalidType()
        return U256(a.to_int() ^ b.to_int())

    @staticmethod
    def bitwise_not(a):
        """
        Returns U256 object representing the result of ~a
        """
        if not isinstance(a, U256):
            raise U256InvalidType()
        a_binary_lst = list(a.to_binary_string())
        for i in range(len(a_binary_lst)):
            if a_binary_lst[i] == '0':
                a_binary_lst[i] = '1'
            else:
                a_binary_lst[i] = '0'
        return U256(int("".join(a_binary_lst), 2))

    @staticmethod
    def byte(i, x):

        pass

    @staticmethod 
    def shl(shift, value):
        """
        Returns U256 object representing the result of value << shift
        """
        pass

    @staticmethod
    def shr(shift, value):
        """
        Returns U256 object representing the result of value >> shift
        """
        pass

    @staticmethod
    def sar(shift, value):
        """
        Returns U256 object representing the result of value >> shift (arithmetic)
        """
        pass

    @staticmethod
    def to_address_hex(address) -> str:
        """
        Use only if value is within range of [0, 2**160 - 1]
        """
        if not isinstance(address, U256):

            raise Exception("arg is not of type U256!")

        hex_str = hex(address.to_int())
        # Remove prefix
        hex_str = hex_str[2:]
        # Check length
        hex_str_len = len(hex_str)
        # How many zeros to prepend if necessary
        preprend_len = 40 - hex_str_len
        for i in range(preprend_len):
            hex_str = "0" + hex_str

        return hex_str

    @staticmethod
    def from_hex(hex: str):

        hex_int = int(hex, 16)
        return U256(hex_int)