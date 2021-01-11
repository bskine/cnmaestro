import requests
import urllib3
from pprint import pprint
import datetime
import time

urllib3.disable_warnings()


def access_token():
    url = "https://10.26.15.60/api/v1/access/token"

    payload = 'grant_type=client_credentials&client_id=FeH7JaeseMj2rJm5&client_secret=4SFsCFAnFmUpFsio8kNO6f78MGjp5L'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    token_json = response.json()
    token = token_json["access_token"]
    return token


def device_list():
    """returns list of location/software_version/status/model#/coordinates in ALP network.
       Not super useful information, but needed to compile list of all radios for processing
       by the details() function."""

    token = access_token()
    url = "https://10.26.15.60/api/v1/devices?network=Alpine&type=ptp"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': ('Bearer ' + token)}
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    x = response.json()
    return x


def details():
    """returns tuple of name, ip, and mac derived from the device_list() function
       for use in performance function"""

    foo = device_list()  # ["data"]
    foo = foo['data']
    site_list = []
    for i in foo:
        site = {"name": i["name"], "IP": i["ip"], "MAC": i["mac"]}
#       """adding dict 'site' to 'site_list'"""
        site_list.append(site)
    return site_list


def performance():
    stop = str(datetime.datetime.now().isoformat(timespec='minutes'))
    start = str((datetime.datetime.now() - datetime.timedelta(seconds=180)).isoformat(timespec='minutes'))
    token = access_token()
    dmx = details()
    #    print(dmx)
    https = "https://10.26.15.60/api/v1/devices/"
    for i in dmx:
        #       TODO:  add try/except for offline units
        mac = i['MAC']
        print(mac)
        name = i['name']
        #        print(name)
#        url = https+mac+"/performance?fields=ethernet&start_time="+start+"&stop_time="+stop
        url = https + mac + "/performance?start_time=" + start + "&stop_time=" + stop + 'total=2'
        payload = {}
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': ('Bearer ' + token)
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        zoo = response.json()
        #        zoo=zoo['data']
        print(name)
        pprint(zoo)
        print('\n')
        time.sleep(2)

        # if zoo['data']==[]:
        #     continue
        # else:
        #     bgp=zoo['data'][0]['ethernet']
        # rssi=(bgp.get('rx_power'))

        time.sleep(1)


if __name__ == "__main__":
    performance()
#    pprint(device_list())
#    pprint(details())
