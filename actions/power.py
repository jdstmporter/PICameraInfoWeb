from battery import UPSDevice

def readBattery():
    try:
        ups=UPSDevice()
        ups.connect()
        info=ups()
        print(str(info))
    except Exception as e:
        print(f'Error = {e}')