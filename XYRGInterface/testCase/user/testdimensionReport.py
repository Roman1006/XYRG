#coding:gbk
import json
import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp

login_xls = common.get_xls("userCase.xlsx", "weidu")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}
cookie_v = []


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, token,JSESSIONID, type, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param JSESSIONID:
        :param type:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.JSESSIONID = str(JSESSIONID)
        self.type = str(type)
        self.result = str(result)
        self.code = int(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        with open('E:/XYRGInterface/testCase/user/cookie.txt','r') as f:
            # print(f.readline())
            # print(type(f.readline()))
            cookie_value = f.readline()
            # print(cookie_value)
            # print(type(cookie_value))
            cookie_v.append(cookie_value)
            # print(cookie_v)
        print(self.case_name+"测试开始前准备")
        self.logger.info(self.case_name + "测试开始前准备")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('weidu')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)
        self.logger.info("第一步：设置url  " + self.url)

        # get visitor token
        # if self.token == '0':
        #     token = localReadConfig.get_headers("token_v")
        # elif self.token == '1':
        #     token = None
        #
        # set headers
        # header = {"JSESSIONID": str(token)}
        # configHttp.set_header(header)
        print("第二步：设置cookie")
        self.logger.info("第二步：设置cookie")
        # print(configHttp.set_header(header))
        cookie = {"JSESSIONID": cookie_v[0]}
        configHttp.set_cookies(cookie)
        print(configHttp.set_cookies(cookie))
        self.logger.info(configHttp.set_cookies(cookie))
        # set params
        print("第三步：设置发送请求的参数")
        self.logger.info("第三步：设置发送请求的参数")
        data = {"type": self.type, "JSESSIONID": cookie_v[0]}
        print(configHttp.set_data(data))
        self.logger.info(configHttp.set_data(data))
        # test interface
        self.return_json = configHttp.postWriteJson()
        # self.return_json.encoding = "UTF-8"
        # print(self.return_json.url)

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)
        self.logger.info("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查结果")
        self.logger.info("第五步：检查结果")

    def tearDown(self):
        """

        :return:
        """
        self.log.build_end_line(self.case_name)
        print("测试结束，输出log完结\n\n")
        self.logger.info("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        print(self.info)
        common.show_return_msg(self.return_json)
        common.get_value_from_return_json_assertEqual(self.info, 'code', 'msg', self.case_name)
        if self.result == '0':
            # common.get_value_from_return_json_assertEqual(self.info, 'code', 'msg',self.case_name)
            self.assertEqual(self.info['code'], self.code,"code值验证不成功")
            self.assertEqual(self.info['msg'], self.msg,"msg值验证不成功")
        if self.result == '1':
            self.assertEqual(self.info['code'], self.code,"code值验证不成功")
            self.assertEqual(self.info['msg'], self.msg,"msg值验证不成功")
