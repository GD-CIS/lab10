import asyncio
import shelve
from bleak import BleakScanner
from time import sleep, gmtime, strftime
import shelve
KNOWN_DEVICES = {"JBL Tune720BT" : "C0:A5:F8:27:E2:99"} #I could only get 1 device to show up with its name
async def scan():
    print("Scanning...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device Name: {device.name}, Address: {device.address}")
    return devices

async def check():
    devices = await BleakScanner.discover()
    nearby_known_devices = {}

    for device in devices:
        if device.address in KNOWN_DEVICES.values():
            device_name = [name for name, addr in KNOWN_DEVICES.items() if addr == device.address][0]
            print(f"{device_name} is nearby!")
            nearby_known_devices[device_name] = device.address

    return nearby_known_devices

def log_devices(devices):
    with shelve.open( "device_log" ) as db:
        for name, address in devices.items():
            key = name + '_' + address
            formatted_time = strftime( "%Y-%m-%d %H:%M:%S", gmtime())
            if key in db:
                time_list = db[key]
                time_list.append(formatted_time)
                db[key] = time_list
            else:
                db[key] = [formatted_time]
    print( "Logged devices in the shelf database." )
async def scan_log():
    nearby = await check()
    if nearby:
        log_devices(nearby)
    else:
        print("Nothing nearby")
async def main(): #Change back to standard def if error occurs
    while True:
        print("Scanning...")
        await (scan_log())
        print("sleeping till next loop...")
        sleep(15)
        print("Verifying log...")
        with shelve.open("device_log") as db:
            for name, address in db.items():
                print(f"{name}: {address}")

async def clean():
    await asyncio.sleep(3600)
    with shelve.open("device_log") as db:
        db.clear()
    print("Cleared the device log.")

async def plz_work():
    do_stuff = await asyncio.gather(main(), clean())
if __name__ == '__main__':
    asyncio.run(plz_work())
    #main #Uncomment main and comment task above if error occurs

    #My main PC doesn't have bluetooth support so I did this on a friends but wasn't able to test how to get the
    #clean() function integrated into the main function, I know it works I just can't get it to run without slowing down
    #whole program




