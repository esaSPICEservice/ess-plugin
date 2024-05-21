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
    run_time = get_runtime()
    sc = run_time.get("spacecraft", "")
    api = get_api()
    cosmo = cosmoscripting.Cosmo()
    frame = sensor_name
    cosmo.moveToPovSpiceFrame(sc, frame, [0,0,0.002], [0,0,1], [0,1,0], 0.0)
    print("Viewing " + sensor_name)
    api.adjustFov(fov, 0)
    cosmo.pause()

def evaluate(expressions):
    cosmo = cosmoscripting.Cosmo()
    api = get_api()
    try:
        for expression in expressions.split('\n'):
            if len(expression.strip()) > 0:
                eval(expression, {'cosmo': cosmo, 'api': api})
    except Exception as error:
        raise EvaluateException("An error occurred: " + type(error).__name__ + " " + error)

class EvaluateException(Exception):
    pass