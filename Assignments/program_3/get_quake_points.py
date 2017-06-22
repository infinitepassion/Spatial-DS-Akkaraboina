import requests
import json
import sys
import glob

"""
This class helps read the Earth Quake data.
Usage:
    fh = FileHelper()

    data = fh.get_data([1960-2017]) #pass year in as list, get data for that year
    data = fh.get_data([2015,2016,2017]) #pass years in as list, get data for those years
"""


def condense_file(data):
    condensed_data = []

    for quake in data['features']:
        keep = {}
        keep['geometry'] = quake['geometry']
        keep['mag'] = quake["properties"]["mag"]
        keep['magType'] = quake["properties"]["magType"]
        keep['time'] = quake["properties"]["time"]
        keep['place'] = quake["properties"]["place"]
        keep['types'] = quake["properties"]["types"]
        keep['rms'] = quake["properties"]["rms"]
        keep['sig'] = quake["properties"]["sig"]
        condensed_data.append(keep)

    return condensed_data
    

##########################################################################################

def get_earth_quake_data(year,month=[1,12],minmag=None,maxmag=None,query=True):
    start_month = month[0]
    end_month = month[1]

    if not maxmag is None:
        maxmag = '&maxmagnitude='+str(maxmag)
    else:
        maxmag = ''

    if not minmag is None:
        minmag = '&minmagnitude='+str(minmag)
    else:
        minmag = '&minmagnitude='+str(1.0)

    if query:
        type = 'query'

    else:
        type = 'count'

    url = 'https://earthquake.usgs.gov/fdsnws/event/1/'+type+'?format=geojson&starttime='+str(year)+'-'+str(start_month)+'-01&endtime='+str(year)+'-'+str(end_month)+'-01'+minmag+maxmag

    r = requests.get(url).json()

    if type == 'count':
        return r['count']
    else:
        return r

