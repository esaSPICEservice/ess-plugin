 The SWI Channel #1 field of view is defined based on the receiver main beam
   half power point directions (-3 dB), and corresponds to a half-cone of
   1-mrad (see [5]).

   The following FOV definition corresponds to the NAIF Body Name:
   JUICE_SWI_CH1.

   \begindata

      INS-28830_NAME                       = 'JUICE_SWI_CH1P'
      INS-28830_BORESIGHT                  = ( 0.000,  0.000,  1.000 )
      INS-28830_FOV_FRAME                  = 'JUICE_SWI_POINTER'
      INS-28830_FOV_SHAPE                  = 'CIRCLE'
      INS-28830_FOV_CLASS_SPEC             = 'ANGLES'
      INS-28830_FOV_REF_VECTOR             = ( 0.000,  1.000,  0.000 )
      INS-28830_FOV_REF_ANGLE              = ( 0.001 )
      INS-28830_FOV_ANGLE_UNITS            = 'RADIANS'

   \begintext


   The SWI Channel #2 field of view is defined based on the receiver main beam
   half power point directions (-1.5 dB), and corresponds to a half-cone of
   0.5-mrad (see [7]).

   The following FOV definition corresponds to the NAIF Body Name:
   JUICE_SWI_CH2.

   \begindata

      INS-28840_NAME                       = 'JUICE_SWI_CH2P'
      INS-28840_BORESIGHT                  = ( 0.000,  0.000,  1.000 )
      INS-28840_FOV_FRAME                  = 'JUICE_SWI_POINTER'
      INS-28840_FOV_SHAPE                  = 'CIRCLE'
      INS-28840_FOV_CLASS_SPEC             = 'ANGLES'
      INS-28840_FOV_REF_VECTOR             = ( 0.000,  1.000,  0.000 )
      INS-28840_FOV_REF_ANGLE              = ( 0.0005 )
      INS-28840_FOV_ANGLE_UNITS            = 'RADIANS'

   \begintext


   \begindata

        FRAME_JUICE_SWI_POINTER = 1234567
        FRAME_1234567_NAME       = 'JUICE_SWI_POINTER'
        FRAME_1234567_CLASS      = 4
        FRAME_1234567_CLASS_ID   = 1234567
        FRAME_1234567_CENTER     = -28800
    
        TKFRAME_1234567_SPEC     = 'ANGLES'
        TKFRAME_1234567_RELATIVE = 'JUICE_SWI_BASE'
        TKFRAME_1234567_ANGLES   = ( 0, 0, 0 )
        TKFRAME_1234567_AXES     = ( 1, 2, 3 )
        TKFRAME_1234567_UNITS    = 'DEGREES'


        NAIF_BODY_NAME += ( 'JUICE_SWI_CH1P'  )
        NAIF_BODY_CODE += ( -28830             )
        NAIF_BODY_NAME += ( 'JUICE_SWI_CH2P'  )
        NAIF_BODY_CODE += ( -28840             )

    \begintext