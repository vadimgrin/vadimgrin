import unittest
from calculator import Service, Cache, sToDate
from decimal import Decimal
import datetime

sampleData = {
    "1/16/2023": {"MSFT": 125, "YHO": 300, "F": 250, },
    "1/17/2023": {"MSFT": 125, "YHO": 300, "F": 250, },
    "1/18/2023": {"MSFT": 125, "YHO": 300, "ABC": 250},
    "1/19/2023": {"MSFT": 125, "YHO": 300, "F": 250, "ZZZ": 0.01},
    "1/20/2023": {"MSFT": 125, "YHO": 300, "F": 250},
}


def digestData(data):
    ret = {}
    for k, v in sampleData.items():
        ret[sToDate(k)] = {i: Decimal(p) for i, p in v.items()}
    return ret


class CalculatorTestCase(unittest.TestCase):
    def setUp(self):
        d = digestData(sampleData)
        self.Cache = Cache(initData=d)
        self.service = Service(cache=self.Cache)

    def test_sToDate(self):
        expected = datetime.date(2023, 11, 30)
        actual = sToDate("11/30/2023")
        self.assertEqual(actual, expected)

    def test_calcBeta(self):
        expected = [2.4, 2.4]
        actual = self.service.calcBeta("MSFT", "YHO", "1/19/2023",  "1/20/2023",  2)
        self.assertListEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
