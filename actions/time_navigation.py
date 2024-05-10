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
    cosmo.showObject(sensor_name)
    print("Viewing " + sensor_name)
    api.gotoObject(sc)
    api.setCentralObject(sc)
    api.setCameraToBodyFixedFrame()
    api.setCameraPosition([0, 0, 5e-3])
    quat = [0, -1, 0, 0]
    api.setCameraOrientation(quat)
    api.adjustFov(fov, 0)
