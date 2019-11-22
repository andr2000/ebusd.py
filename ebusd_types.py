from enum import Enum


class EbusdErr(Enum):
    RESULT_ERR_GENERIC_IO = 'ERR: generic I/O error'
    RESULT_ERR_DEVICE = 'ERR: generic device error'
    RESULT_ERR_SEND = 'ERR: send error'
    RESULT_ERR_ESC = 'ERR: invalid escape sequence'
    RESULT_ERR_TIMEOUT = 'ERR: read timeout'
    RESULT_ERR_NOTFOUND = 'ERR: element not found'
    RESULT_ERR_EOF = 'ERR: end of input reached'
    RESULT_ERR_INVALID_ARG = 'ERR: invalid argument'
    RESULT_ERR_INVALID_NUM = 'ERR: invalid numeric argument'
    RESULT_ERR_INVALID_ADDR = 'ERR: invalid address'
    RESULT_ERR_INVALID_POS = 'ERR: invalid position'
    RESULT_ERR_OUT_OF_RANGE = 'ERR: argument value out of valid range'
    RESULT_ERR_INVALID_PART = 'ERR: invalid part type'
    RESULT_ERR_MISSING_ARG = 'ERR: missing argument'
    RESULT_ERR_INVALID_LIST = 'ERR: invalid value list'
    RESULT_ERR_DUPLICATE = 'ERR: duplicate entry'
    RESULT_ERR_DUPLICATE_NAME = 'ERR: duplicate name'
    RESULT_ERR_BUS_LOST = 'ERR: arbitration lost'
    RESULT_ERR_CRC = 'ERR: CRC error'
    RESULT_ERR_ACK = 'ERR: ACK error'
    RESULT_ERR_NAK = 'ERR: NAK received'
    RESULT_ERR_NO_SIGNAL = 'ERR: no signal'
    RESULT_ERR_SYN = 'ERR: SYN received'
    RESULT_ERR_SYMBOL = 'ERR: wrong symbol received'
    RESULT_ERR_NOTAUTHORIZED = 'ERR: not authorized'

    @classmethod
    def has_value(cls, value):
        return any(value.startswith(item.value) for item in cls)


# This can probably be converted at run-time if all the devices
# have similar format, e.g. <circuit><XX>
EbusdDeviceIdToCircuit = {
    'BAI00': 'bai',
    'B7V00': 'b7v'
}


class EbusdType(Enum):
    unknown = 'unknown'
    read = 'r'
    write = 'w'
    update = 'u'
    update_on_write = 'uw'


class EbusdMessage:
    def __init__(self, cs_string):
        # cs_string is a comma separated type,name
        list = cs_string.split(',')
        if not list:
            raise ValueError('Wrong or empty parameter list')
        self.type = EbusdType(list[0])
        self.type_ebusd = list[0]
        self.name = list[1]


class EbusdScanResult:
    def __init__(self, scan_string):
        # 08;Vaillant;BAI00;0104;7803;21;18;23;0010021961;0001;005167;N4
        vals = scan_string.split(';')
        if not vals:
            raise ValueError('Cannot parse scan result: %s' % scan_string)
        self.address = vals[0]
        self.make = vals[1]
        self.id = vals[2]
        # Set proper circuit name
        self.circuit = EbusdDeviceIdToCircuit[self.id]
        self.sw = vals[3]
        self.hw = vals[4]
        self.prod = vals[8]
