# *_* uft-8 *_*
import json
import requests

from common.const import CONST
from common.loggers.logger import log
from common.sqllite_op import sql_lite_tool


def update_cookies(cookies):
    result = get_cookies()
    if result:
        sql = "update cache set value='{}' where name='cookies';".format(cookies)
        sql_lite_tool.execute(sql)
    else:
        sql = "insert into cache (name, value) values('{}','{}')".format('cookies', cookies)
        sql_lite_tool.execute(sql)


def get_cookies():
    sql = "select * from cache where name='cookies';"
    result = sql_lite_tool.execute(sql)
    return result


def check_response_status(response):
    status = response.status_code
    if status != 200:
        raise Exception("get captcha error :{}".format(status))


def get_captcha():
    try:
        url = 'http://{}:{}/ygdzh/api/v1/register/query_captcha'.format(CONST.DZH_SERVER_HOST,
                                                                        CONST.DZH_SERVER_PORT)
        res = requests.get(url)
        check_response_status(res)
        res.encoding = 'utf-8'
        img = res.content
        with open('captcha.png', 'wb') as file:
            file.write(img)
            file.close()
    except Exception as e:
        log.exception(e)


def saas_login(username, password, captcha):
    try:
        ret = True
        err_code = None
        info = None
        url = 'http://{}:{}/ygdzh/api/v1/register/login?web=tools'.format(CONST.DZH_SERVER_HOST,
                                                                          CONST.DZH_SERVER_PORT)
        data = {
            captcha: captcha,
            password: password,
            username: username
        }
        response = requests.post(url, json=data)
        check_response_status(response)
        response.encoding = 'utf-8'
        cookies = response.cookies
        result_json = json.loads(response.content)
        result = result_json.get('result')
        if result and result.lower() == "success":
            update_cookies(cookies)
        else:
            ret = False
            err_code = result_json.get('error_code')
            info = result_json.get('mag', '')
        return ret, err_code, info
    except Exception as e:
        log.exception(e)


def saas_logined(cookies):
    cookies = get_cookies()