import cosmoscripting

def get_rings():
    return {
        'Rings': ['JUICE_JUP_HALO_RING',
                  'JUICE_JUP_MAIN_RING',
                  'JUICE_JUP_AMA_GOS_RING',
                  'JUICE_JUP_THE_GOS_RING',
                  'JUICE_JUP_THE_RING_EXT'],
        'Torus': ['JUICE_IO_PLASMA_TORUS', 'JUICE_EUROPA_PLASMA_TORUS']
    }

def toggle_ring(value, name):
    cosmo = cosmoscripting.Cosmo()
    if value:
        cosmo.showObject(name)
    else:
        cosmo.hideObject(name)
