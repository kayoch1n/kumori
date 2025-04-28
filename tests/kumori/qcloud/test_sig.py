import unittest

from kumori.qcloud import sig_v1

class TestSigV1(unittest.TestCase):
    def test_expand_dict(self):
        data = {'a': 1}
        actual = list(sig_v1.expand(data, key=''))
        self.assertEqual([('a', 1)], actual)
        
    def test_expand_list(self):
        data = {'a': [1,2,3]}
        actual = list(sig_v1.expand(data, key=''))
        self.assertEqual([('a.0', 1), ('a.1', 2), ('a.2', 3)], actual)
    
    def test_compose(self):
        kwargs = dict(
            InstanceIds=['ins-09dx96dg'],
            Offset=0,
            Limit=20,
        )
        actual = sig_v1.compose(
            kwargs, 
            action='DescribeInstances',
            timestamp=1465185768,
            nonce=11886,
            region='ap-guangzhou',
            version='2017-03-12',
            sid='AKIDz8krbsJ5yK**********mLPx3EXAMPLE'
            )
        actual = {k:v for k, v in actual}
        expect = {
            'Action' : 'DescribeInstances',
            'InstanceIds.0' : 'ins-09dx96dg',
            'Limit' : 20,
            'Nonce' : 11886,  
            'Offset' : 0,
            'Region' : 'ap-guangzhou',
            'SecretId' : 'AKIDz8krbsJ5yK**********mLPx3EXAMPLE',
            'Timestamp' : 1465185768,
            'Version': '2017-03-12',
        }
        self.assertEqual(expect, actual)
        
    def test_sign(self):
        args = {
            'Action' : 'DescribeInstances',
            'InstanceIds.0' : 'ins-09dx96dg',
            'Limit' : 20,
            'Nonce' : 11886,  
            'Offset' : 0,
            'Region' : 'ap-guangzhou',
            'SecretId' : 'AKIDz8krbsJ5yK**********mLPx3EXAMPLE',
            'Timestamp' : 1465185768,
            'Version': '2017-03-12',
        }
        sign = sig_v1.sign(
            b'Gu5t9xGARN**********QYCN3EXAMPLE',
            'GET',
            'cvm.tencentcloudapi.com',
            "/",
            args=list((k, v) for k, v in args.items())
        )
        self.assertEqual(b'3T55hnKF3YgbPRlpbTd3B+6bYwQ=', sign)
        

if __name__ == '__main__':
    unittest.main()
