import cosmoscripting
from ui.common import get_api, get_runtime


def goto_date(utc_str):
    cosmo = cosmoscripting.Cosmo()
    cosmo.setTime(utc_str + " UTC")
    spacecraft_view()

def goto_spacecraft(sc_name, sc_frame, initial_offset):
    print(sc_name, sc_frame, initial_offset)
    cosmo = cosmoscripting.Cosmo()
    cosmo.moveToPovSpiceFrame(
        sc_name, sc_frame, initial_offset, [0, 0, 1], [0, 1, 0], 0.0
    )
    cosmo.setFov(70, 0)

def spacecraft_view():
    run_time = get_runtime()
    spacecrafts = run_time.get("spacecrafts", [])
    if len(spacecrafts) > 0:
        spacecraft = spacecrafts[0]
        name = spacecraft.get("spacecraft")
        frame = spacecraft.get("spacecraft_frame")
        initial_offset = spacecraft.get("initial_offset", [0, 2e-3, -22e-3])
        goto_spacecraft(name, frame, initial_offset)


def sensor_view(sensor_name, fov):
    api = get_api()
    cosmo = cosmoscripting.Cosmo()
    cosmo.gotoObject(sensor_name + '_SENSOR',  0)
    cosmo.setCentralObject(sensor_name + '_SENSOR')
    cosmo.setCameraToBodyFixedFrame()
    cosmo.setCameraPosition([0, 0, 0.05])
    api.adjustFov(fov, 0)
    cosmo.setCameraOrientation([0, 0, -1, 0])

def goto_sensor_date(utc_str, sensor_name, fov):
    cosmo = cosmoscripting.Cosmo()
    cosmo.setTime(utc_str + " UTC")
    sensor_view(sensor_name, fov)


def evaluate(expressions):
    cosmo = cosmoscripting.Cosmo()
    api = get_api()
    try:
        for expression in expressions.split('\n'):
            if len(expression.strip()) > 0:
                eval(expression, {'cosmo': cosmo, 'api': api})
    except Exception as error:
        raise EvaluateException("An error occurred: " + type(error).__name__ + " " + str(error))

class EvaluateException(Exception):
    pass