import cosmoscripting

def goto_date(utc_str):    
    cosmo = cosmoscripting.Cosmo()
    cosmo.setTime(utc_str + ' UTC')