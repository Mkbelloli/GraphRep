import xlrd
from Loaders.DataSourceLoader import DataSourceLoader

ANCHOR_COLUMN = 3
MAX_COLUMN_RANGE = 100
MAX_ROW_RANGE = 100


class RowXLSLoader(DataSourceLoader):

    def __init__(self, filename):
        self.xls_filename = filename
        self.xl_workbook = None
        self.sheet = None
        self.param_names = []
        self.row_counter = 1

    def initialize(self):
        self.xl_workbook = xlrd.open_workbook(self.xls_filename)
        self.sheet = self.xl_workbook.sheet_by_index(0)
        self.param_names = []
        for i in range(self.sheet.ncols):
            t = self.sheet.cell_value(0, i)
            self.param_names.append((t, i))

        self.row_counter = 1

    def __next__(self):
        if self.xl_workbook == None:
            raise StopIteration

        if self.row_counter >= self.sheet.nrows:
            raise StopIteration

        while self.row_counter < self.sheet.nrows:
            row = {}
            for param_counter  in range(0, len(self.param_names)):
                t, tind = self.param_names[param_counter]
                v = str(self.sheet.cell_value(self.row_counter, tind))
                if len(v.strip()) > 0:
                    row[t] = v

            self.row_counter += 1
            return row

        raise StopIteration
