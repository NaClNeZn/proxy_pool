import random
import requests
import time
import fake_useragent

# 实例化fake_useragent对象
ua = fake_useragent.UserAgent()

# 视频bv号
bvid = ["BV1ZCHYeMEQt"]

# 代理池地址，项目可见https://github.com/jhao104/proxy_pool
getproxy = "http://192.168.0.234:5010/get/"
deleteproxy = "http://192.168.0.234:5010/delete/?proxy={}"
proxynum = "http://192.168.0.234:5010/count"
# 真正点击地址
url = "http://api.bilibili.com/x/click-interface/click/web/h5"


def run():
    num = 0
    while int(requests.get(proxynum).json().get("count")) != 0:
        resp = requests.get(getproxy).json().get("proxy")
        for bv in bvid:
            headers = {
                'User-Agent': ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Origin': 'https://www.bilibili.com',
                'Connection': 'keep-alive'
            }
            stime = str(int(time.time()))

            while True:
                try:
                    resp_view = requests.get("http://api.bilibili.com/x/web-interface/view?bvid={}".format(bv),
                                             headers=headers)
                    resp_view_json = resp_view.json()
                    if "data" in resp_view_json:
                        getdata = resp_view_json["data"]
                        break
                except requests.RequestException as e:
                    sleep_time = random.randint(10, 15)
                    print(f"获取的视频数据时出错: {bv},等待{sleep_time}秒后重试, {e}")
                    # 等待一段时间后重试
                    time.sleep(sleep_time)

            data = {
                'aid': getdata["aid"],
                'cid': getdata["cid"],
                "bvid": bv,
                'part': '1',
                'mid': getdata["owner"]["mid"],
                'lv': '6',
                "stime": stime,
                'jsonp': 'jsonp',
                'type': '3',
                'sub_type': '0',
                'title': getdata["title"]
            }

            try:
                stime = str(int(time.time()))
                data["stime"] = stime
                headers["referer"] = "http://www.bilibili.com/video/{}/".format(data.get("bvid"))

                proxy = {
                    "http": "http://{}".format(resp)
                }

                response = requests.post(url, headers=headers, data=data, proxies=proxy, timeout=5)
                response.raise_for_status()  # 检查响应状态码
                response.close()
                num += 1
                sleep_time = random.randint(10, 15)
                print(f"done   {num},等待 {sleep_time} 秒后执行下一次")
                time.sleep(sleep_time)
            except requests.RequestException as e:
                print(f"代理连接超时或请求错误: {e}")
            except Exception as e:
                print(f"意外错误: {e}")
        requests.get(deleteproxy.format(resp))
    print("无可用代理")


if __name__ == '__main__':
    run()

if __name__ == '__main__':
    run()
