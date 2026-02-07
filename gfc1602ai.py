import board
import digitalio


class GFC1602AI:
    """Driver for GFC1602AI LCD display."""

    __rs = None
    __rw = None
    __e = None
    __db0 = None
    __db1 = None
    __db2 = None
    __db3 = None
    __db4 = None
    __db5 = None
    __db6 = None
    __db7 = None

    def __init__(self, rs, rw, e, db0, db1, db2, db3, db4, db5, db6, db7):
        """Initializes the GFC1602AI display with given pin configuration."""
        self.__rs = digitalio.DigitalInOut(rs)
        self.__rw = digitalio.DigitalInOut(rw)
        self.__e = digitalio.DigitalInOut(e)
        self.__db0 = digitalio.DigitalInOut(db0)
        self.__db1 = digitalio.DigitalInOut(db1)
        self.__db2 = digitalio.DigitalInOut(db2)
        self.__db3 = digitalio.DigitalInOut(db3)
        self.__db4 = digitalio.DigitalInOut(db4)
        self.__db5 = digitalio.DigitalInOut(db5)
        self.__db6 = digitalio.DigitalInOut(db6)
        self.__db7 = digitalio.DigitalInOut(db7)
        self.__rs.direction = digitalio.Direction.OUTPUT
        self.__rw.direction = digitalio.Direction.OUTPUT
        self.__e.direction = digitalio.Direction.OUTPUT
        self.__db0.direction = digitalio.Direction.OUTPUT
        self.__db1.direction = digitalio.Direction.OUTPUT
        self.__db2.direction = digitalio.Direction.OUTPUT
        self.__db3.direction = digitalio.Direction.OUTPUT
        self.__db4.direction = digitalio.Direction.OUTPUT
        self.__db5.direction = digitalio.Direction.OUTPUT
        self.__db6.direction = digitalio.Direction.OUTPUT
        self.__db7.direction = digitalio.Direction.OUTPUT

    def clear_display(self):
        """Clears the display."""

        self.__rs.value = False
        self.__rw.value = False
        self.__e.value = True

        # Set command for clear display: 0b00000001
        self.__db7.value = False
        self.__db6.value = False
        self.__db5.value = False
        self.__db4.value = False
        self.__db3.value = False
        self.__db2.value = False
        self.__db1.value = False
        self.__db0.value = True

    def return_home(self):
        """Returns the cursor to the home position."""
        self.__rs.value = False
        self.__rw.value = False
        self.__e.value = True

        # Set command for return home: 0b00000010
        self.__db7.value = False
        self.__db6.value = False
        self.__db5.value = False
        self.__db4.value = False
        self.__db3.value = False
        self.__db2.value = False
        self.__db1.value = True
        self.__db0.value = False

    def entry_mode_set(self, decrement=False, display_shift=False):
        """Sets the entry mode of the display."""
        self.__rs.value = False
        self.__rw.value = False
        self.__e.value = True

        # Set command for entry mode set: 0b000001XX
        self.__db7.value = False
        self.__db6.value = False
        self.__db5.value = False
        self.__db4.value = False
        self.__db3.value = False
        self.__db2.value = True
        self.__db1.value = not decrement
        self.__db0.value = display_shift

    def display_control(self, display_on=True, cursor_on=False, blink_on=False):
        """Controls the display settings."""
        self.__rs.value = False
        self.__rw.value = False
        self.__e.value = True

        # Set command for display control: 0b00001XXX
        self.__db7.value = False
        self.__db6.value = False
        self.__db5.value = False
        self.__db4.value = False
        self.__db3.value = True
        self.__db2.value = display_on
        self.__db1.value = cursor_on
        self.__db0.value = blink_on

    def function_set(self, data_length_8bits=True, two_line_display=False, font_5x10=False):
        """Sets the function of the display."""
        self.__rs.value = False
        self.__rw.value = False
        self.__e.value = True

        # Set command for function set: 0b001XXX00
        self.__db7.value = False
        self.__db6.value = False
        self.__db5.value = True
        self.__db4.value = data_length_8bits
        self.__db3.value = two_line_display
        self.__db2.value = font_5x10
        self.__db1.value = False
        self.__db0.value = False

    def set_ddram_address(self, address):
        """Sets the DDRAM address."""

        if address < 0 or address > 0b1111111:
            raise ValueError("Address must be between 0 and 127 (0b1111111)")

        self.__rs.value = False
        self.__rw.value = False
        self.__e.value = True

        # Set ddram address: 0b1XXXXXXX
        self.__db7.value = True
        self.__db6.value = address & 0b1000000
        self.__db5.value = address & 0b0100000
        self.__db4.value = address & 0b0010000
        self.__db3.value = address & 0b0001000
        self.__db2.value = address & 0b0000100
        self.__db1.value = address & 0b0000010
        self.__db0.value = address & 0b0000001

    def write_data(self, data):
        """Writes data to the display."""

        if data < 0 or data > 0b11111111:
            raise ValueError("Data must be between 0 and 255 (0b11111111)")

        self.__rs.value = True
        self.__rw.value = False
        self.__e.value = True

        # Set data: 0bXXXXXXXX
        self.__db7.value = data & 0b10000000
        self.__db6.value = data & 0b01000000
        self.__db5.value = data & 0b00100000
        self.__db4.value = data & 0b00010000
        self.__db3.value = data & 0b00001000
        self.__db2.value = data & 0b00000100
        self.__db1.value = data & 0b00000010
        self.__db0.value = data & 0b00000001

    def _translate_char(self, char):
        """Translates a character to its corresponding ASCII value for the display."""
        if len(char) != 1:
            raise ValueError("Input must be a single character.")

        lookup_table = {
            '±': 0x10,
            '≡': 0x11,
            '': 0x12,  # TODO: Fix Implimentation
            '': 0x13,  # TODO: Fix Implimentation
            '': 0x14,  # TODO: Fix Implimentation
            '': 0x15,  # TODO: Fix Implimentation
            '': 0x16,  # TODO: Fix Implimentation
            '': 0x17,  # TODO: Fix Implimentation
            '': 0x18,  # TODO: Fix Implimentation
            '': 0x19,  # TODO: Fix Implimentation
            '': 0x1A,  # TODO: Fix Implimentation
            '∫': 0x1B,
            '=': 0x1C,
            '~': 0x1D,
            '²': 0x1E,
            '³': 0x1F,
            ' ': 0x20,
            '!': 0x21,
            '"': 0x22,
            '#': 0x23,
            '$': 0x24,
            '%': 0x25,
            '&': 0x26,
            "'": 0x27,
            '(': 0x28,
            ')': 0x29,
            '*': 0x2A,
            '+': 0x2B,
            ',': 0x2C,
            '-': 0x2D,
            '.': 0x2E,
            '/': 0x2F,
            '0': 0x30,
            '1': 0x31,
            '2': 0x32,
            '3': 0x33,
            '4': 0x34,
            '5': 0x35,
            '6': 0x36,
            '7': 0x37,
            '8': 0x38,
            '9': 0x39,
            ':': 0x3A,
            ';': 0x3B,
            '<': 0x3C,
            '=': 0x3D,
            '>': 0x3E,
            '?': 0x3F,
            '@': 0x40,
            'A': 0x41,
            'B': 0x42,
            'C': 0x43,
            'D': 0x44,
            'E': 0x45,
            'F': 0x46,
            'G': 0x47,
            'H': 0x48,
            'I': 0x49,
            'J': 0x4A,
            'K': 0x4B,
            'L': 0x4C,
            'M': 0x4D,
            'N': 0x4E,
            'O': 0x4F,
            'P': 0x50,
            'Q': 0x51,
            'R': 0x52,
            'S': 0x53,
            'T': 0x54,
            'U': 0x55,
            'V': 0x56,
            'W': 0x57,
            'X': 0x58,
            'Y': 0x59,
            'Z': 0x5A,
            '[': 0x5B,
            '\\': 0x5C,
            ']': 0x5D,
            '^': 0x5E,
            '_': 0x5F,
            '`': 0x60,
            'a': 0x61,
            'b': 0x62,
            'c': 0x63,
            'd': 0x64,
            'e': 0x65,
            'f': 0x66,
            'g': 0x67,
            'h': 0x68,
            'i': 0x69,
            'j': 0x6A,
            'k': 0x6B,
            'l': 0x6C,
            'm': 0x6D,
            'n': 0x6E,
            'o': 0x6F,
            'p': 0x70,
            'q': 0x71,
            'r': 0x72,
            's': 0x73,
            't': 0x74,
            'u': 0x75,
            'v': 0x76,
            'w': 0x77,
            'x': 0x78,
            'y': 0x79,
            'z': 0x7A,
            '{': 0x7B,
            '|': 0x7C,
            '}': 0x7D,
            '~': 0x7E,
            'Δ': 0x7F,
            'Ç': 0x80,
            'ü': 0x81,
            'é': 0x82,
            'â': 0x83,
            'ä': 0x84,
            'à': 0x85,
            'å': 0x86,
            'ç': 0x87,
            'ê': 0x88,
            'ë': 0x89,
            'è': 0x8A,
            'ï': 0x8B,
            'î': 0x8C,
            'ì': 0x8D,
            'Ä': 0x8E,
            'Å': 0x8F,
            'É': 0x90,
            'æ': 0x91,
            'Æ': 0x92,
            'ô': 0x93,
            'ö': 0x94,
            'ò': 0x95,
            'û': 0x96,
            'ù': 0x97,
            'ÿ': 0x98,
            'Ö': 0x99,
            'Ü': 0x9A,
            'ñ': 0x9B,
            'Ñ': 0x9C,
            'ª': 0x9D,
            'º': 0x9E,
            '¿': 0x9F,
            'á': 0xA0,
            'í': 0xA1,
            'ó': 0xA2,
            'ú': 0xA3,
            '¢': 0xA4,
            '£': 0xA5,
            '¥': 0xA6,
            '₧': 0xA7,
            'ƒ': 0xA8,
            '𝑖': 0xA9,
            'Ã': 0xAA,
            'ã': 0xAB,
            'Õ': 0xAC,
            'õ': 0xAD,
            'Ø': 0xAE,
            'ø': 0xAF,
            '': 0xB0,  # TODO: Fix Implimentation
            '¨': 0xB1,
            '°': 0xB2,
            '`': 0xB3,
            '´': 0xB4,
            '': 0xB5,  # TODO: Fix Implimentation
            '': 0xB6,  # TODO: Fix Implimentation
            '×': 0xB7,
            '÷': 0xB8,
            '≤': 0xB9,
            '≥': 0xBA,
            '≪': 0xBB,
            '≫': 0xBC,
            '≠': 0xBD,
            '√': 0xBE,
            '⁻': 0xBF,
            '': 0xC0,  # TODO: Fix Implimentation
            '': 0xC1,  # TODO: Fix Implimentation
            '∞': 0xC2,
            '◸': 0xC3,
            '↲': 0xC4,
            '↑': 0xC5,
            '↓': 0xC6,
            '→': 0xC7,
            '←': 0xC8,
            '⌜': 0xC9,  # ?
            '⌝': 0xCA,  # ?
            '⌞': 0xCB,  # ?
            '⌟': 0xCC,  # ?
            '•': 0xCD,
            '®': 0xCE,
            '©': 0xCF,
            '™': 0xD0,  # ?
            '': 0xD1,  # TODO: Fix Implimentation
            '': 0xD2,  # TODO: Fix Implimentation
            '': 0xD3,  # TODO: Fix Implimentation
            '': 0xD4,  # TODO: Fix Implimentation
            '': 0xD5,  # TODO: Fix Implimentation
            '': 0xD6,  # TODO: Fix Implimentation
            '': 0xD7,  # TODO: Fix Implimentation
            '': 0xD8,  # TODO: Fix Implimentation
            '': 0xD9,  # TODO: Fix Implimentation
            '': 0xDA,  # TODO: Fix Implimentation
            '': 0xDB,  # TODO: Fix Implimentation
            '': 0xDC,  # TODO: Fix Implimentation
            '': 0xDD,  # TODO: Fix Implimentation
            '': 0xDE,  # TODO: Fix Implimentation
            '': 0xDF,  # TODO: Fix Implimentation
            '': 0xE0,  # TODO: Fix Implimentation
            '': 0xE1,  # TODO: Fix Implimentation
            '': 0xE2,  # TODO: Fix Implimentation
            '': 0xE3,  # TODO: Fix Implimentation
            '': 0xE4,  # TODO: Fix Implimentation
            '': 0xE5,  # TODO: Fix Implimentation
            '': 0xE6,  # TODO: Fix Implimentation
            '': 0xE7,  # TODO: Fix Implimentation
            '': 0xE8,  # TODO: Fix Implimentation
            '': 0xE9,  # TODO: Fix Implimentation
            '': 0xEA,  # TODO: Fix Implimentation
            '': 0xEB,  # TODO: Fix Implimentation
            '': 0xEC,  # TODO: Fix Implimentation
            '': 0xED,  # TODO: Fix Implimentation
            '': 0xEE,  # TODO: Fix Implimentation
            '': 0xEF,  # TODO: Fix Implimentation
            '': 0xF0,  # TODO: Fix Implimentation
            '': 0xF1,  # TODO: Fix Implimentation
            '': 0xF2,  # TODO: Fix Implimentation
            '': 0xF3,  # TODO: Fix Implimentation
            '': 0xF4,  # TODO: Fix Implimentation
            '': 0xF5,  # TODO: Fix Implimentation
            '': 0xF6,  # TODO: Fix Implimentation
            '': 0xF7,  # TODO: Fix Implimentation
            '': 0xF8,  # TODO: Fix Implimentation
            '': 0xF9,  # TODO: Fix Implimentation
            '': 0xFA,  # TODO: Fix Implimentation
            '': 0xFB,  # TODO: Fix Implimentation
            '': 0xFC,  # TODO: Fix Implimentation
            '': 0xFD,  # TODO: Fix Implimentation
            '': 0xFE,  # TODO: Fix Implimentation
            '': 0xFF,  # TODO: Fix Implimentation
        }

        return lookup_table[char]

    def _translate_string(self, string):
        """Translate a string to a list of character RAM addresses."""

        return [self._translate_char(char) for char in string]

    def write_string(self, string, two_line_display=False):
        """Write a string to the LCD."""
        self.clear_display()
        self.set_ddram_address(0x00)  # Return Home
        self.function_set(two_line_display=two_line_display)
        self.display_control(display_on=True)
        self.entry_mode_set()

        if two_line_display:
            raise NotImplementedError()
        else:
            character_addresses = self._translate_string(string)

            for address in character_addresses:
                self.write_data(address)
