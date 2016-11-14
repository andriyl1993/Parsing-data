import xlrd
from xlutils.margins import number_of_good_rows
from xlutils.copy import copy
import requests
from bs4 import BeautifulSoup
import urllib

class Excel:
    def __init__(self):
        self.file = None
        self.sheets_read = []
        self.sheets_write = []
        self.data = {}

    def open_file(self, name='fpm.xls'):
        self.file = xlrd.open_workbook(name,formatting_info=True)
        self.save_data = copy(self.file)

    def get_sheet(self, index):
        self.sheets_read.append(self.file.sheet_by_index(index))
        self.sheets_write.append(self.save_data.get_sheet(index))
        if index == 0:
            self.res_sheet = self.save_data.get_sheet(index)

    def get_sheet_data(self, index):
        curr_sheet = self.sheets_read[index]
        rows = number_of_good_rows(curr_sheet)
        cols = range(curr_sheet.ncols)
        self.data[index] = []

        for i in range(rows):
            d = []
            for col in cols:
                d.append(curr_sheet.cell_value(i, col))
            self.data[index].append(d)

    def run(self, name='fpm.xls'):
        self.open_file(name)
        self.get_sheet(0)
        self.get_sheet(1)
        self.get_sheet_data(0)
        self.get_sheet_data(1)
        rows1 = ['TotalShifr', 'komu', 'ktoRead', 'StudyCourse']
        rows2 = ['SPECIALITY_CODE', 'KOMY', 'KTO', 'COURSE_ID']
        self.row_compare(0, 1, rows1, rows2)

    def my_print(self):
        for el in self.data[0]:
            for e in el:
                print e

    def _get_column_index(self, row_cols, column):
        for col, val in enumerate(row_cols):
            if column == val:
                return col
        raise Exception('Not Found')

    def row_compare(self, index_sheet1, index_sheet2, rows1 = [], rows2 = [], field_write='Dek_DISCIPLINE_ID'):
        if len(rows1) == len(rows2):
            data_sheet1 = self.data[index_sheet1]
            data_sheet2 = self.data[index_sheet2]
            write_field_index = self._get_column_index(data_sheet1[0], field_write)

            for i, data_row1 in enumerate(data_sheet1):
                for j, data_row2 in enumerate(data_sheet2):
                    res = []
                    for k in range(len(rows1)):
                        if i != 0 and j != 0:
                            index_column1 = self._get_column_index(data_sheet1[0], rows1[k])
                            index_column2 = self._get_column_index(data_sheet2[0], rows2[k])
                            try:
                                split_text = str(data_row1[index_column1]).split('.')
                                if len(split_text) > 1 and split_text[1] == "0":
                                    val_row1 = int(data_row1[index_column1])
                                    val_row2 = int(data_row2[index_column2])
                                else:
                                    val_row1 = str(data_row1[index_column1])
                                    val_row2 = str(data_row2[index_column2])
                            except:
                                val_row1 = data_row1[index_column1]
                                val_row2 = data_row2[index_column2]
                            if val_row1 == val_row2:
                                res.append(True)
                            else:
                                res = []
                                break
                    if len(res) == 4:
                        break
                if len(res) == len(rows1):
                    res = filter(lambda el: el == False, res)
                    if not len(res):
                        id = data_sheet2[j][0]
                        self.res_sheet.write(i, write_field_index, int(id))

            self.save_data.save('fpm-output.xls')
        else:
            raise Exception("Length rows don't equal")

ex = Excel()
ex.run()