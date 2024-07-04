import requests
import json
import os
# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # server酱
    sckey = os.environ.get('SCKEY')

    # 推送内容
    title = "Glados"
    success, fail = 0, 0        # 成功账号数量 失败账号数量
    sendContent = ""

    # glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("COOKIES", []).split("&")
    if cookies[0] == "":
        print('未获取到COOKIE变量')
        cookies = []
        exit(0)

    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"

    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload = {
        'token': 'glados.one'
    }

    for cookie in cookies:
        checkin = requests.post(url, headers={'cookie': cookie, 'referer': referer, 'origin': origin,
                                'user-agent': useragent, 'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
        state = requests.get(url2, headers={
                             'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})
    # --------------------------------------------------------------------------------------------------------#
        if checkin.status_code == 200:
            # 解析返回的json数据
            result = checkin.json()
            # 获取签到结果
            status = result.get('message')
            points = result.get('points')
            list1 = result.get('list')
            # 查找第一个名为balance的值并保留小数点前的部分
            balance = next((item['balance'].split('.')[0] for item in list1 if 'balance' in item), None)
            # 获取账号当前状态
            result = state.json()
            # 获取剩余时间
            leftdays = int(float(result['data']['leftDays']))
            # 获取账号email
            email = result['data']['email']

            if "Checkin!" in status:
                success += 1
                message_status = f"签到成功,获得 {points} 点数，剩余{balance}点数 "
            elif status == "Checkin Repeats! Please Try Tomorrow":
                message_status = f"今日已签到，剩余{balance}点数"
            else:
                fail += 1
                message_status = "签到失败，请检查..."

            if leftdays is not None:
                message_days = f"{leftdays} 天"
            else:
                message_days = "无法获取剩余天数信息"
        else:
            email = ""
            message_status = "签到请求url失败, 请检查..."
            message_days = "获取信息失败"

        # 推送内容
        sendContent += f"{'-'*30}\n\
            账号: {email}\n\
            签到情况: {message_status}\n\
            剩余天数: {message_days}\n"
        
        if cookie == cookies[-1]:
            sendContent += '-' * 30
        
     # --------------------------------------------------------------------------------------------------------#
    print("sendContent:" + "\n", sendContent)
    if sckey != "":
        title += f': 成功{success},失败{fail}'
        url = "https://sctapi.ftqq.com/{}.send?title={}&desp={}".format(sckey, title, sendContent)
        r = requests.post(url)
        print('推送完成',r.status_code)
        

