import datetime

def epoch_seconds(isoc):
    homologated = isoc[:19]+'+0000'
    # epoch = datetime.datetime.fromisoformat(homologated)
    epoch = datetime.datetime.strptime(homologated, '%Y-%m-%dT%H:%M:%S%z')
    return epoch.timestamp()


def duration(st, et):
    return epoch_seconds(et) - epoch_seconds(st) 

def tdb_to_utc(tdb_seconds):
    tdb_origin = datetime.datetime(2000,1,1,12,0,0,0)
    leap_seconds = 37
    seconds = tdb_seconds - 32.184 - leap_seconds
    return tdb_origin + datetime.timedelta(seconds=seconds)

def tdb_to_utc_str(tdb_seconds):
    return tdb_to_utc(tdb_seconds).isoformat(timespec='seconds')

