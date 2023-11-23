import cosmoscripting

def goto_date(utc_str):    
    cosmo = cosmoscripting.Cosmo()
    cosmo.setTime(utc_str + ' UTC')
    spacecraft_view()


def spacecraft_view():
    cosmo = cosmoscripting.Cosmo()
    cosmo.moveToPovSpiceFrame(
        'JUICE', 'JUICE_SPACECRAFT', [0,2E-3,-22E-3], [0,0,1], [0,1,0], 0.0)
    cosmo.setFov(70, 0)


def sensor_view(sensor_name, fov):
    cosmo = cosmoscripting.Cosmo()
    cosmo.moveToPovSpiceFrame(
        'JUICE', sensor_name, [0, 0, 10E-3], [0,0,1], [0,1,0], 0.0)
    cosmo.setFov(fov, 0)
