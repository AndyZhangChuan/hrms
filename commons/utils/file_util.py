# -*- encoding: utf8 -*-
import codecs
import csv
import os

import cStringIO


def create_csv(file_name, field, data):
    csv_file = codecs.open(file_name, 'wb', 'utf_8')
    writer = DictUnicodeWriter(csv_file, fieldnames=field)
    writer.writeheader()
    writer.writerows(data)
    csv_file.close()


def create_excel(file_name, sheet_name, data):
    """
    创建excel
    :param file_name 文件名称
    :param sheet_name 表格名称
    :param data 表格数据，用二维数组表示
    :return:
    """
    import xlwt
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet_name)
    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            ws.write(row_idx, col_idx, val)
    wb.save(file_name)


def delete_file(file_name):
    os.remove(file_name)


class DictUnicodeWriter(object):
    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, lineterminator=os.linesep, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        encoded_item = {}
        for k, v in D.items():
            if type(v) == type(''):
                encoded_item[k] = v.encode("utf-8")
            else:
                encoded_item[k] = v
        self.writer.writerow(encoded_item)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()
