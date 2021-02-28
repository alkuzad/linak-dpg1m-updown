import logging
import asyncio

from bleak import BleakClient, BleakError
from bleak.uuids import uuidstr_to_str

async def run(address, loop, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        # loop.set_debug(True)
        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        log.info("Connected: {0}".format(x))

        for service in client.services:
            # service is instance of 'Windows.Devices.Bluetooth.GenericAttributeProfile.GattDeviceService'
            log.info(
                "[Service] {0}: {1}".format(service.uuid, uuidstr_to_str(service.uuid))
            )
            # Ugly way to filter out characteristics for this service... I use this since Bleak has
            # already fetched all characteristics and stored them in `client.characteristics`,
            # albeit not grouped by service...
            # Could e.g. be fetched as `chars = await client._get_chars(service)`
            for char in service.characteristics:
                # char is instance of 'Windows.Devices.Bluetooth.GenericAttributeProfile.GattCharacteristic'
                if "read" in char.properties:
                    try:
                        char_value = await client.read_gatt_char(char.uuid)
                    except BleakError as e:
                        char_value = "ERROR: {0}".format(e)
                else:
                    char_value = None

                char_name = (
                    char.description if char.description else "None"
                )
                log.info(
                    "\t[Characteristic] {0}: ({1}) | Name: {2}, Value: {3} ".format(
                        char.uuid, ",".join(char.properties), char_name, char_value
                    )
                )
                # Descriptor handling for Windows will be added in Bleak 0.4.0...
                for descriptor in char.descriptors:
                    log.info(
                        "\t\t[Descriptor] {0}: (Handle: {1})".format(
                            descriptor.description, descriptor.handle
                        )
                    )

if __name__ == "__main__":
    address = open("mac").read().strip()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, True))