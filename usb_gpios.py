import dataclasses
from enum import Enum, auto
import serial

class M5:
    HIGH = 1
    LOW = 0
    class Boards(Enum):
        M5_ATOMS3 = auto()
        M5_ATOM_S3_LITE = auto()
        M5_STACK_CORE2 = auto()
        M5_ATOM_LITE = auto()

    class PinMode(Enum):
        OUTPUT = auto()
        INPUT_PULLUP = auto()
        INPUT_PULLDOWN = auto()

    class Peripheral(Enum):
        DIGITAL_INPUT_PULLUP = auto()  
        DIGITAL_INPUT_PULLDOWN = auto()
        DIGITAL_OUTPUT = auto()       
        ANALOG_INPUT = auto()         
        ANALOG_OUTPUT = auto()        
        I2C_SCL = auto()              
        I2C_SDA = auto()              
        SPI = auto()                  
        UART = auto()                 
        ADC = auto()                  
        DAC = auto()                  
        TOUCH = auto()                
        NONE = auto()

    @dataclasses.dataclass
    class PinFeature:
        pinNumber: int
        peripherals_can_use: list['M5.Peripheral']
        state_used_for: 'M5.Peripheral'
        state_bool_used: bool

    allPinBanks = {
        Boards.M5_ATOMS3: {
            0: 'hogehoge',
            1: PinFeature(1, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            2: PinFeature(2, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            4: PinFeature(4, [Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            5: PinFeature(5, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            6: PinFeature(6, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            7: PinFeature(7, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            8: PinFeature(8, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            38: PinFeature(7, [Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.I2C_SCL], Peripheral.NONE, False),
            39: PinFeature(8, [Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.I2C_SDA], Peripheral.NONE, False),
        },
        Boards.M5_ATOM_S3_LITE: {
            0: 'fugafuga',
            1: PinFeature(1, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            2: PinFeature(2, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            4: PinFeature(4, [Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            5: PinFeature(5, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            6: PinFeature(6, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            7: PinFeature(7, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            8: PinFeature(8, [Peripheral.ADC, Peripheral.TOUCH, Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.UART], Peripheral.NONE, False),
            38: PinFeature(7, [Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.I2C_SCL], Peripheral.NONE, False),
            39: PinFeature(8, [Peripheral.DIGITAL_OUTPUT, Peripheral.DIGITAL_INPUT_PULLUP, Peripheral.DIGITAL_INPUT_PULLDOWN, Peripheral.ANALOG_INPUT, Peripheral.ANALOG_OUTPUT, Peripheral.I2C_SDA], Peripheral.NONE, False),
        }
    }

    def __init__(self, board: Boards, serial: serial):
        self.board = board
        self.serial = serial
        self.pinBank = self.allPinBanks[board]

    def send_command(self, command: int):
        self.serial.write(command)

    def pinMode(self, pin: int, mode: PinMode):
        if pin in self.pinBank and self.pinBank[pin].state_used_for == self.Peripheral.NONE and mode in self.pinBank[pin].peripherals_can_use:
            self.pinBank[pin].state_used_for = mode
            self.send_command(str(0x1200 + pin).encode() + b'\n')
            print(hex(0x1200 + pin).encode() + b'\n', flush=True)
            return True
        elif pin not in self.pinBank:
            raise ValueError(f"Invalid pin number: {pin}")
        elif self.pinBank[pin].state_used_for != self.Peripheral.NONE:
            raise ValueError(f"Pin {pin} is already used for {self.pinBank[pin].state_used_for}")
        elif self.mode not in self.pinBank[pin].peripherals_can_use:
            raise ValueError(f"Invalid peripheral: {mode}")
        return False

    def digitalWrite(self, pin: int, value: int):
        if pin in self.pinBank and self.pinBank[pin].state_used_for == self.Peripheral.DIGITAL_OUTPUT:
            self.send_command(str(0x1100 + value*16 + pin).encode() + b'\n')
            print(hex(0x1100 + value*16 + pin).encode() + b'\n', flush=True)
            return True
        elif pin not in self.pinBank:
            raise ValueError(f"Invalid pin number: {pin}")
        elif self.pinBank[pin].state_used_for != self.Peripheral.DIGITAL_OUTPUT:
            raise ValueError(f"Pin {pin} is not used for DIGITAL_OUTPUT")
        return False

    def digitalRead(self, pin: int):
        if pin in self.pinBank and (self.pinBank[pin].state_used_for == self.Peripheral.DIGITAL_INPUT_PULLUP or self.pinBank[pin].state_used_for == self.Peripheral.DIGITAL_INPUT_PULLDOWN):
            self.send_command(f"digitalRead({pin})")
            return True
        elif pin not in self.pinBank:
            raise ValueError(f"Invalid pin number: {pin}")
        elif self.pinBank[pin].state_used_for != self.Peripheral.DIGITAL_INPUT_PULLUP and self.pinBank[pin].state_used_for != self.Peripheral.DIGITAL_INPUT_PULLDOWN:
            raise ValueError(f"Pin {pin} is not used for DIGITAL_INPUT_PULLUP or DIGITAL_INPUT_PULLDOWN")
        return False

    # def Serial_begin(self, num: int, baudrate: int):
    # def s_serial_begin