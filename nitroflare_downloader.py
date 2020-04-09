import requests
import os
import sys
import wget


if len(sys.argv) != 5:
    print ("(+) usage: %s {USERNAME-premiumuser} {PASSWORD} {SAVE TO DIRECTORY} {FULL PATH OF FILE dl.txt}" % sys.argv[0])
    print ("(+) eg: %s user@domain.com password /PATH/TO/SAVE C:\PATH\TO\DOWNLOAD_LIST\list.txt" % sys.argv[0])
    sys.exit(-1)

URL = "https://nitroflare.com/api/v2/getKeyInfo"

PARAMS = {"user": sys.argv[1], "premiumKey": sys.argv[2]}

PATH = sys.argv[3];

r = requests.get(url=URL, params=PARAMS)
data = r.json()
print("Premium Account : " + data["type"])

with open(sys.argv[4]) as fp:
    lines = fp.readlines()
    cnt = 1
    for line in lines:
        if line.strip() == '':
            continue
        print("line is: " + line.strip())
        print("File {}: {}".format(cnt, line.strip()))
        _url = line.strip()
        _file_id = _url.split("/")[4]
        print(_file_id)
        url = "https://nitroflare.com/api/v2/getFileInfo"
        params = {"files": _file_id}
        r = requests.get(url=url, params=params)
        data = r.json()
        print("getFileInfo : " + str(data))
        print(
            "File ID : "
            + _file_id
            + " -> "
            + data["result"]["files"][_file_id]["status"]
        )
        url = "https://nitroflare.com/api/v2/getDownloadLink"
        params = PARAMS
        params["file"] = _file_id
        r = requests.get(url=url, params=params)
        data = r.json()
        print("getDownloadLink : " + str(data))
        _dl_url = data["result"]["url"]
        #print("dl url: " + _dl_url)
        #print("name" + data["result"]['name'])
        #print("PATH: " + PATH )
        # check if file exists and has the same size:
        if os.path.exists(PATH +data["result"]['name']):
            size = data["result"]['size']
            if str(os.path.getsize(PATH + data["result"]['name'])) ==size:
                print("File with name: " +PATH +data["result"]['name'] + " with size: " +   size + " exists! Skipping!")
                continue
            else:
                print("File with name: " + PATH + data["result"]['name'] + " exists but sizes mismatch! deleting!")
                os.remove(PATH + data["result"]['name'])
        wget.download(_dl_url, PATH +data["result"]['name'] )
        line = fp.readline()
        cnt += 1
print("DONE!...Downloaded "+ str(cnt) + " files")