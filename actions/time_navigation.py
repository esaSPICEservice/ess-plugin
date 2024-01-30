import cosmoscripting
from ui.common import get_api

def goto_date(utc_str):    
    cosmo = cosmoscripting.Cosmo()
    cosmo.setTime(utc_str + ' UTC')
    spacecraft_view()


def spacecraft_view():
    cosmo = cosmoscripting.Cosmo()
    cosmo.moveToPovSpiceFrame(
        'JUICE', 'JUICE_SPACECRAFT', [0,2E-3,-22E-3], [0,0,1], [0,1,0], 0.0)
    cosmo.setFov(70, 0)


def sensor_view(sensor_name, fov, sc='JUICE'):
    api = get_api()
    cosmo = cosmoscripting.Cosmo()
    cosmo.showObject(sensor_name)
    print('Viewing ' + sensor_name)
    api.gotoObject(sc)
    api.setCentralObject(sc)
    api.setCameraToBodyFixedFrame()
    api.setCameraPosition([0,0,5E-3])
    quat = [0, -1, 0, 0]
    api.setCameraOrientation(quat)
    api.adjustFov(fov, 0)