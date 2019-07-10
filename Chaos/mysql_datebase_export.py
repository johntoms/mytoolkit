#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/4/24'
"""

import platform
import pymysql
python_info = platform.python_version()
if int(python_info.split('.')[0]) < 3:
    # 同时兼容 Python2
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')


class Explore(object):
    def __init__(self, host='127.0.0.1', user='root', password='', db=''):
        """
        初始化 数据库连接实例
        :param host: 主机名
        :param user: 用户名
        :param password: 密码
        :param db: 数据库名
        """
        self.user = user
        self.host = host
        self.password = password
        self.db = db
        self.title = None
        self.file_name = 'mysql_markdown.md'

    def get_sql_results(self, sql):
        """
        连接数据库并执行 sql 语句
        :param sql: SQL 语句
        :return:
        """
        connect = pymysql.connect(host=self.host, user=self.user, passwd=self.password, db=self.db, charset='utf8')
        cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        connect.close()
        return results

    def set_table_title(self, **kwargs):
        """
        设置表头显示的表头 和 要获取的列名
        :param kwargs: 列名(column) 及 列的说明(comment)
        :return:
        """
        print(kwargs)
        title = []
        comment = []
        for key, value in kwargs.items():
            title.append(key)
            comment.append(value)
        self.title = [title, comment]
        return self.title

    def set_file_name(self, file_name):
        """
        设置输出的文件名
        :param file_name: 文件名
        :return:
        """
        self.file_name = file_name
        if len(file_name.split('.')) == 1:
            self.file_name = file_name + '.md'
            return self.file_name
        elif file_name.split('.')[1] != 'md':
            raise Exception('请以 md 结尾')
        elif len(file_name.split('.')) != 2:
            raise Exception('名称有误，格式错误')
        else:
            return self.file_name

    def export_markdown_table(self, sql):
        table_title = self.title
        results = self.get_sql_results(sql)
        print(results)
        if results:
            if table_title is None:
                raise Exception("需要调用 set_table_title 方法，设置表头")
            elif not isinstance(table_title, list):
                raise Exception("你不该自己单独设置表头，请使用 set_table_title 方法")
            else:
                """组合 markdown 的表头格式"""
                markdown_table = ''
                markdown_format = ''
                for title in table_title[1]:
                    markdown_table += "|" + title + " "
                    markdown_format += "|" + " ------- "
                markdown_table += "|\n"
                markdown_format += "|\n"
                markdown_title = markdown_table + markdown_format

                # 打开文件
                pf = open('./' + self.file_name, 'w+')
                # 写入表头
                pf.write(markdown_title)
                # 写入内容
                for d in results:
                    contents = ''
                    for content in table_title[0]:
                        contents += "|" + str(d.get(content, '')).replace('\r\n', '') + " "
                    contents += "|\n"
                    pf.write(contents)

                # 关闭文件
                pf.close()
        else:
            print(u"数据库查询结果返回为空，请检查 SQL 语句")


if __name__ == '__main__':
    # 初始化实例，并传入连接数据库的信息
    explorer = Explore(host='localhost', password='123456', user='devops', db='cloudcare')

    # 设置输出文件的文件名，可以不设置，则使用默认的文件名：`mysql_markdown.md`.
    # 文件设置示例：`数据`或`数据.md` 不建议
    explorer.set_file_name('数据')

    # 设置获取字段和在 markdown 中展示的字段，对于如下情况：
    # root @ MySQL - 01
    # 17: 10:  [(none)] > select version();
    # +------------+
    # | version() |
    # +------------+
    # | 5.7.17 - log |
    # +------------+
    # 1 row in set(0.00 sec)

    # 不要慌，如下传参即可。
    # explorer.set_table_title(**{'version()':'版本信息'})
    # explorer.export_markdown_table('select version()')

    # 正常的数据格式如下传参即可。
    # explorer.set_table_title(Tables_in_sys="系统库的表")
    # explorer.export_markdown_table('show tables from sys;')


    # 对于导出的数据表有想要增加的列但暂不想添值，如下传参即可。
    # 注意： e: 随意定义，不要使用返回的结果里存在的 key,也就是列名。
    explorer.set_table_title(Tables_in_sys="系统库的表", e="说明")
    explorer.export_markdown_table('show tables from sys;')

