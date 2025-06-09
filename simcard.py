"""
Interface with secure SIM card for encrypted config storage.
Requires PySCard (pyscard) and SIM C-APDU support.
"""

from smartcard.System import readers
from smartcard.Exceptions import NoReadersException

PIN_REFERENCE = 0x00
EF_CONFIG_FILE = [0x2F, 0x00]

class SIMCardError(Exception):
    pass

def select_reader():
    try:
        r = readers()
    except NoReadersException:
        raise SIMCardError("No smartcard readers.")
    if not r:
        raise SIMCardError("No smartcard readers available.")
    return r[0]

def load_config_from_sim():
    """
    Read the encrypted config JSON from the SIM’s file system.
    """
    reader = select_reader()
    conn = reader.createConnection()
    conn.connect()
    # Select the EF_CONFIG_FILE
    select_apdu = [0x00, 0xA4, 0x00, 0x00, len(EF_CONFIG_FILE)] + EF_CONFIG_FILE
    resp, sw1, sw2 = conn.transmit(select_apdu)
    if sw1 != 0x90:
        raise SIMCardError(f"SIM select failed {sw1:02X}{sw2:02X}")
    # Read binary (up to 256 bytes)
    read_apdu = [0x00, 0xB0, 0x00, 0x00, 0x00]
    resp, sw1, sw2 = conn.transmit(read_apdu)
    if sw1 != 0x90:
        raise SIMCardError(f"SIM read failed {sw1:02X}{sw2:02X}")
    return bytes(resp).decode('utf-8')

def save_config_to_sim(json_str):
    """
    Write the encrypted config JSON back to the SIM’s file system.
    Note: for payloads >255 bytes, you'd need chunking (omitted for brevity).
    """
    reader = select_reader()
    conn = reader.createConnection()
    conn.connect()
    # Select file
    conn.transmit([0x00, 0xA4, 0x00, 0x00, len(EF_CONFIG_FILE)] + EF_CONFIG_FILE)
    # Update binary
    data = json_str.encode('utf-8')
    update_apdu = [0x00, 0xD6, 0x00, 0x00, len(data)] + list(data)
    _, sw1, sw2 = conn.transmit(update_apdu)
    if sw1 != 0x90:
        raise SIMCardError(f"SIM write failed {sw1:02X}{sw2:02X}")
