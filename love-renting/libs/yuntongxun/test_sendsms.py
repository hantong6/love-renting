#-*-coding:utf-8-*_
from sendsms import SendSms
import unittest

class TestSendSms(unittest.TestCase):
    """自定义测试类"""
    def setUp(self):
        pass

    def testSingle(self):
        send1=SendSms()
        send2=SendSms()
        self.assertIs(send1,send2)

    def tearDown(self):
        pass

if __name__=='__main__':
    unittest.main()