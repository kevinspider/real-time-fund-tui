import json
import time
import requests
from typing import TypedDict


class GSZZLRES(TypedDict):
    """
    {"fundcode":"002963","name":"易方达黄金ETF联接C","jzrq":"2026-02-03","dwjz":"3.5004","gsz":"3.6123","gszzl":"3.20","gztime":"2026-02-04 10:46"}
    """

    fundcode: str
    name: str
    # 单位净值
    dwjz: str
    # 截止日期
    jzrq: str
    # 估算值
    gsz: str
    # 估算增长率
    gszzl: str
    # 当前时间
    gztime: str


class IndustryINFO(TypedDict):
    """{"f12":"BK1031","f13":90,"f14":"光伏设备","f62":5823197440.0}"""

    # 板块名称
    f14: str
    # 增长资金
    f62: float


def get_gszzl(fund_code: str, retry: int = 10) -> GSZZLRES | None:
    while retry:
        try:
            url = f"https://fundgz.1234567.com.cn/js/{fund_code}.js"
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
            }
            res = requests.get(url=url, headers=headers)
            if res.status_code == 200:
                if res.text.startswith("jsonpgz("):
                    data = res.text.strip("jsonpgz(").strip(");")
                    data = json.loads(data)
                    return GSZZLRES(data)
                else:
                    # 返回不是 jsonpgz(开头, 重试
                    raise ValueError("response not start with `jsonpgz(`, retrying")
            else:
                # != 200 重试
                raise ValueError("response status != 200, retrying")
        except Exception as e:
            print(f"Error {e} from `get_gszzl`")
            retry -= 1


def get_industry(retry:int = 10) -> list[IndustryINFO] | None:
    while retry:
        try:
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
            }

            params = (
                ("pn", "1"),
                ("pz", "500"),
                ("po", "1"),
                ("np", "1"),
                ("fields", "f12,f13,f14,f62"),
                ("fid", "f62"),
                ("fs", "m:90 t:2"),
                ("_", str(int(time.time() * 1000))),
            )

            response = requests.get(
                "http://push2.eastmoney.com/api/qt/clist/get",
                headers=headers,
                params=params,
                verify=False,
            )
            return response.json()["data"]["diff"]

        except Exception as e:
            print(f"Error {e} from `get_industry`")
            retry -= 1


if __name__ == "__main__":

    res = get_gszzl("002963")
    print(res)

    res = get_industry()
    print(res)
