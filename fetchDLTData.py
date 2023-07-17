import json
import re
import requests
from requests.adapters import HTTPAdapter
import os

headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
 'Cookie': ''}

def fetchDLTData(pageSize=30, pageNo=1):
    print("fetching data...")
    request_link = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=" + str(pageSize) + "&isVerify=1&pageNo=" + str(pageNo)
    r = requests.get(request_link, headers=headers, verify=False)
    return r.json()

def main():
    X = fetchDLTData(3000, 1)
    # Specify the file path where you want to save the JSON data
    file_path = "dltData.json"

    # Open the file in write mode
    with open(file_path, "w") as f:
        # Write the JSON data to the file
        json.dump(X, f)
        print("Saved")

if __name__ == '__main__':
    main()
