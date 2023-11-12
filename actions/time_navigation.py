import cosmoscripting

def goto_date(utc_str):    
    cosmo = cosmoscripting.Cosmo()
    cosmo.setTime(utc_str + ' UTC')
    spacecraft_view()


def spacecraft_view():
    cosmo = cosmoscripting.Cosmo()
    cosmo.moveToPovSpiceFrame(
        'JUICE', 'JUICE_SPACECRAFT', [0,2E-3,-22E-3], [0,0,1], [0,1,0], 0.0) 