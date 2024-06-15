import cosmoscripting
from ui.common import get_api, get_runtime


def goto_date(utc_str):
    cosmo = cosmoscripting.Cosmo()
    cosmo.setTime(utc_str + " UTC")
    spacecraft_view()


def spacecraft_view():
    run_time = get_runtime()
    sc = run_time.get("spacecraft", "")
    sc_frame = run_time.get("spacecraft_frame", "")
    cosmo = cosmoscripting.Cosmo()
    cosmo.moveToPovSpiceFrame(
        sc, sc_frame, [0, 2e-3, -22e-3], [0, 0, 1], [0, 1, 0], 0.0
    )
    cosmo.setFov(70, 0)


def sensor_view(sensor_name, fov):
    api = get_api()
    cosmo = cosmoscripting.Cosmo()
    cosmo.gotoObject(sensor_name + '_SENSOR',  0)
    cosmo.setCentralObject(sensor_name + '_SENSOR')
    cosmo.setCameraToBodyFixedFrame()
    cosmo.setCameraPosition([0, 0, 0.05])
    api.adjustFov(fov, 0)
    cosmo.setCameraOrientation([0, 0, -1, 0])


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