import argparse
from typing import List, Any


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--FileName", help="Data File Name", type=str, default='C:/Temp/pythonTest/equity_namr.txt')
    parser.add_argument("-c", "--Columns",  help="Report Columns", type=str, default='EQY_PRIM_EXCH_SHRT;CRNCY;EXCH_CODE;TICKER')
    parser.add_argument("-d", "--Delimiter", help="Report data delimiter character", type=str, default='^')

    return parser.parse_args()

FIELD_DELIM_CHR = "|"
COLS_DELIM_CHR  = ";"


def valid(s: str, sz: int) -> bool:
    # Ensure that the data line we are reading is valid for a given meta context
    return len(s) and len(s.split(FIELD_DELIM_CHR)) >= sz


class Parser:

    def __init__(self, fname: str, report_cols: str, delimiter: str):
        self.filename = fname
        self.delimiter = delimiter
        self.report_cols = report_cols.split(COLS_DELIM_CHR)
        self.data_cols = None

    def read_block(self, block_id: str):
        block_start = f"START-OF-{block_id}"
        block_end   = f"END-OF-{block_id}"
        inside_meta_block = False
        with open(self.filename, 'r') as _file:
            while line := _file.readline():
                if line.startswith(block_start):
                    inside_meta_block = True
                    continue
                if line.startswith(block_end):
                    inside_meta_block = False
                    break
                if inside_meta_block:
                    yield line.strip()
        return

    def read_meta(self) -> str:
        for line in self.read_block('FIELDS'):
            if len(line) == 0 or line.startswith("#"):
                continue
            yield line

    def read_data(self) -> str:
        result = []
        for line in self.read_block('DATA'):
            if valid(line, len(self.data_cols)):
                yield line.split(FIELD_DELIM_CHR)

    def extract_data(self) -> List[List[str]]:
        res = [self.report_cols]  # Header
        self.data_cols = list(self.read_meta())

        # get indices of extract columns in the meta data
        col_index = [self.data_cols.index(f) for f in self.report_cols]

        for line in self.read_data():
            res.append([line[i] for i in col_index])

        return res

    def print_report(self, data: List[List[str]]):
        for line in data:
            print(self.delimiter.join(line))


if __name__ == "__main__":
    args = parse_arguments()

    p = Parser(args.FileName, args.Columns, args.Delimiter)
    p.print_report(p.extract_data())
