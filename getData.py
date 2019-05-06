from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
from requests import request
import json
import config.read_config
import dbOperate.dbOperate
import dateutil.parser as dp


class Auth():
    def __init__(self, id, key):
        self.app_id = id
        self.app_key = key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


if __name__ == "__main__":
    url = "https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/Taichung?$top=30&$format=JSON"
    # 取得自己的config
    sys_config = config.read_config.SystemConfig("config.yaml")
    sys_config = sys_config.get_config()
    auth = Auth(sys_config["app_id"], sys_config["app_key"])
    response = request('get', url, headers=auth.get_auth_header())
    json_data = json.loads(response.text)

    db_conn = dbOperate.dbOperate.dbOperate(mongo_str=sys_config["mongodb"]["host"])
    # 把時間資料進行轉換成時間格式再存入db，不然無法進行搜尋
    for index, data in enumerate(json_data):
        json_data[index]["NextBusTime"] = dp.parse(data["NextBusTime"])
        json_data[index]["SrcUpdateTime"] = dp.parse(data["SrcUpdateTime"])
        json_data[index]["UpdateTime"] = dp.parse(data["UpdateTime"])

    db_conn.db_insert_many("Bus", "bus_route", json_data)

    print(json_data)
