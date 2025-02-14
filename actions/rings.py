import cosmoscripting

def get_rings():
    return {
        'Rings': [('JUICE_JUP_HALO_RING',    '01 Halo'),
                  ('JUICE_JUP_MAIN_RING',    '02 Main'),
                  ('JUICE_JUP_AMA_GOS_RING', '03 Amalthea Gossamer'),
                  ('JUICE_JUP_THE_GOS_RING', '04 Thebe Gossamer'),
                  ('JUICE_JUP_THE_RING_EXT', '05 Thebe extension')],
        'Torus': [
            ('JUICE_IO_PLASMA_TORUS', 'Io Plasma'),
            ('JUICE_EUROPA_PLASMA_TORUS', 'Europa Plasma')]
    }

def toggle_ring(value, name):
    cosmo = cosmoscripting.Cosmo()
    if value:
        cosmo.showObject(name)
    else:
        cosmo.hideObject(name)
