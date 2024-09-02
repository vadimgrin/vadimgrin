import unittest
import os
import tempfile
from parse import Parser

DATA_BLOCK = '''
FIELD_A0|FIELD_B0|FIELD_C0|FIELD_D0
FIELD_A1|FIELD_B1|FIELD_C1|FIELD_D1
FIELD_A2|FIELD_B2|FIELD_C2|FIELD_D2
FIELD_A3|FIELD_B3|FIELD_C3|FIELD_D3
'''

FIELDS_BLOCK = '''
A
B
C
D
'''

TESTFILE = '''
START-OF-FILE
PROGRAMNAME=getdata
DATEFORMAT=yyyymmdd

START-OF-FIELDS
# Security Description
%s
## comment 
END-OF-FIELDS
START-OF-DATA
# Comment

%s
# Another comment
END-OF-DATA
DATARECORDS=1234
TIMEFINISHED=Tue Oct 25 17:40:14 EDT 2022
END-OF-FILE
''' % (FIELDS_BLOCK, DATA_BLOCK)

REPORT_FIELDS = 'B;C'

class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.fp = tempfile.NamedTemporaryFile(delete=False)
        self.fp.write(bytes(TESTFILE, 'utf-8'))
        self.fp.close()
        self.Parser = Parser(self.fp.name, REPORT_FIELDS, '$')

    def TearDown(self):
        self.fp.close()
        os.unlink(self.fp.name)
        print(f"Deleting temporary file: {self.fp.name}")

    def test_readMetaBlock(self):
        expected = FIELDS_BLOCK.split()
        actual = list(self.Parser.read_meta())
        self.assertEqual(actual, expected)

    def test_readDataBlock(self):
        self.Parser.data_cols = FIELDS_BLOCK.split()
        expected = [_l.split("|") for _l in DATA_BLOCK.split()]
        actual = list(self.Parser.read_data())
        self.assertEqual(actual, expected)

    def test_extractData(self):
        self.Parser.data_cols = FIELDS_BLOCK.split()

        expected = [REPORT_FIELDS.split(';'),
                    ['FIELD_B0', 'FIELD_C0'],
                    ['FIELD_B1', 'FIELD_C1'],
                    ['FIELD_B2', 'FIELD_C2'],
                    ['FIELD_B3', 'FIELD_C3']]
        actual = self.Parser.extract_data()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
