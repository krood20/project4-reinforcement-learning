import http.client
import mimetypes
from codecs import encode
import json


def locate_me():
    #locate me
    #Example Output
    # {"code":"OK","world":"0","state":"0:1"}
    conn = http.client.HTTPSConnection("www.notexponential.com")
    payload = ''
    headers = {
        'x-api-key': '9398bf5f4533fbabb0af',
        'userId': '1042',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PHPSESSID=02be66b83f429101b2b740de970cfcc2; qa_key=pk7kcvbr5vlyiho3sgfq2vk5mk09pl2w'
    }
    conn.request("GET", "/aip2pgaming/api/rl/gw.php?type=location&teamId=1260", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data


#Enter World
def enter_world(world_num):
    # Example output
    # {"code":"OK","worldId":0,"runId":65,"state":"0:0"}
    conn = http.client.HTTPSConnection("www.notexponential.com")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=type;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("enter"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=worldId;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(world_num))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=teamId;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("1260"))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'x-api-key': '9398bf5f4533fbabb0af',
        'userId': '1042',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/aip2pgaming/api/rl/gw.php", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


#make move
def make_move(move, world_num):
    #Example output
    # {"code":"OK","worldId":0,"runId":"65","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.1000000000000000055511151231257827021181583404541015625,"newState":{"x":"0","y":1}}
    conn = http.client.HTTPSConnection("www.notexponential.com")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=type;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("move"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=teamId;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("1260"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=move;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(move))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=worldId;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(world_num))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
      'x-api-key': '9398bf5f4533fbabb0af',
      'userId': '1042',
      'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/aip2pgaming/api/rl/gw.php", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

#get score
def get_score():
    #Example output
    # {"score":0,"code":"OK"}
    conn = http.client.HTTPSConnection("www.notexponential.com")
    payload = ''
    headers = {
    'x-api-key': '9398bf5f4533fbabb0af',
    'userId': '1042',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'PHPSESSID=02be66b83f429101b2b740de970cfcc2; qa_key=pk7kcvbr5vlyiho3sgfq2vk5mk09pl2w'
    }
    conn.request("GET", "/aip2pgaming/api/rl/score.php?type=score&teamId=1260", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

#get last X moves
def get_last_x_moves(x):
    #Example output
    # {"runs":[{"runId":"65","teamId":"1260","gworldId":"0","createTs":"2021-04-20
    # 12:50:13","score":"-0.1","moves":"1"}],"code":"OK"}
    conn = http.client.HTTPSConnection("www.notexponential.com")
    payload = ''
    headers = {
        'x-api-key': '9398bf5f4533fbabb0af',
        'userId': '1042',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PHPSESSID=02be66b83f429101b2b740de970cfcc2; qa_key=pk7kcvbr5vlyiho3sgfq2vk5mk09pl2w'
    }
    conn.request("GET", "/aip2pgaming/api/rl/score.php?type=runs&teamId=1260&count=" + x, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


#example usage
# world_num = "0"
# move = "N"
# x = "10"

# enter_world(world_num)
# make_move(move, world_num)
# locate_me()
# get_score()
# get_last_x_moves(x)