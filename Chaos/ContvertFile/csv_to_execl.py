#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/6/6'
"""

import csv
import xlsxwriter


def read_csv(file_path, start_line= None, end_line=None):
    """
    读取 csv 文件的内容
    :param file_path: csv文件路径
    :param start_line: 起始行
    :param end_line: 结束行
    :return: 读取的文件内容（前闭后闭） type: list
    """
    if not isinstance(start_line, int) and not isinstance(end_line, int):
        raise TypeError
    if start_line <= 0 or end_line <=0:
        raise Exception("start_line and end_line should be > 0")
    if start_line >= end_line:
        raise Exception("start_line should < end_line")

    with open(file_path, "r") as f:
        fp = csv.reader(f, delimiter=',')
        line = 1
        print(fp)
        data = []
        for row in fp:
            if line < start_line:
                line += 1
                continue
            if line > end_line:
                break
            line += 1
            data.append(row)
        return data


def write_execl(data):
    """
    写入到 execl 文件中
    :param data: 文件内容 type: 列表
    :return: None
    """
    if not data:
        raise Exception("未读取到文件内容")

    workbook = xlsxwriter.Workbook('test_hello1.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0

    for line_data in data:
        for col_data in line_data:
            col = 0
            worksheet.write(row, col, col_data)
            col += 1
        row += 1

    workbook.close()


def delete_readed():
    """删除已读取的文件内容，未读取的文件内容保存到新的文件"""
    pass


def write_csv():
    """内容写入到 csv 文件，使用`,`作为分割符"""
    pass


def read_execl():
    """读取 execl 文件的内容"""
    pass


if __name__ == '__main__':
    file_name = "/Users/johntoms/aliyunhub/mytoolkit/tmp/200万张券-券核销.csv"
    data = read_csv(file_path=file_name, start_line=150000, end_line=400000)
    write_execl(data)
