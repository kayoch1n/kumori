import unittest

from kumori.qcloud import core, errors


class TestUser(unittest.TestCase):
    def test_User(self):
        with self.assertRaises(ValueError):
            core.User("11111111", "", "ap-guangzhou")
        with self.assertRaises(ValueError):
            core.User("", "22222222", "ap-guangzhou")


class TestConsole(unittest.TestCase):
    def test_suppress_errors(self):
        user = core.User("11111111", "22222222", "ap-guangzhou")
        with self.assertRaises(errors.ApiError):
            user.cvm.DescribeInstances(Unknown="Key")
        with core.console.suppress_errors():
            resp = user.cvm.DescribeInstances(Unknown="Key")
            self.assertIn("Error", resp)


class TestUserContext(unittest.TestCase):
    def test_prepare_params(self):
        user = core.User(
            "AKIDz8krbsJ5yK**********mLPx3EXAMPLE",
            "Gu5t9xGARN**********QYCN3EXAMPLE",
            "ap-guangzhou",
            core.console,
        )
        cvm = user.cvm
        api = cvm.service.get_api("DescribeInstances")
        api.method = "GET"
        kwargs = dict(
            InstanceIds=["ins-09dx96dg"],
            Offset=0,
            Limit=20,
        )
        actual = cvm.prepare_params(api, 1465185768, 11886, kwargs)
        assertions = {
            "Action": "DescribeInstances",
            "InstanceIds.0": "ins-09dx96dg",
            "Limit": 20,
            "Nonce": 11886,
            "Offset": 0,
            "Region": "ap-guangzhou",
            "SecretId": "AKIDz8krbsJ5yK**********mLPx3EXAMPLE",
            "Timestamp": 1465185768,
            "Version": "2017-03-12",
            "Signature": "3T55hnKF3YgbPRlpbTd3B+6bYwQ=",
        }
        for key, expect in assertions.items():
            self.assertEqual(expect, actual.get(key, None))


if __name__ == "__main__":
    unittest.main()
