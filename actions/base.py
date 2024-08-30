from picam import PiCam

def getInformation():
    cams = PiCam()
    return [cams.cameras, cams.modes]

def display(cams, mods):
    print('Cameras:')
    for n in range(len(cams)):
        print(f'{n} : {cams[n]}')

    print('Modes:')
    for mode in mods:
        print(str(mode))