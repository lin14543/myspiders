# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb, logging, traceback, time
from myspiders import settings
from datetime import datetime


class DBHost(object):

    def __init__(self):
        self.db = self._get_con()
        self.cursor = self.db.cursor()

    def update_item(self, table_name, row):
        sql = "SELECT id FROM %s WHERE host_name='%s'" % (table_name, row['host_name'])
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            row_id = result[0]
            sql_update = "UPDATE %s SET %s " % (table_name, ', '.join('{}=%s'.format(k) for k in row))
            sql_update += "WHERE id = %s" % row_id
            values = tuple(row[key] for key in row)
            try:
                self.cursor.execute(sql_update, values)
                print('updated')
            except:
                logging.error('update item error')
            return True
        return False

    def add_row(self, tablename, rowdict):
        keys = rowdict.keys()
        columns = ", ".join(keys)
        values_template = ", ".join(["%s"] * len(keys))

        sql = "insert into %s (%s) values (%s)" % (tablename, columns, values_template)
        values = tuple(rowdict[key] for key in keys)
        try:
            self.cursor.execute(sql, values)
            print('added')
        except:
            traceback.print_exc()
            logging.error('add error')

    def process_host(self, item):
        try:
            item['update_time'] = datetime.now()
            self.db.ping()
        except:
            self.db = self._get_con()
            self.cursor = self.db.cursor()
        if not self.update_item('ticket_host', item):
            self.add_row('ticket_host', item)

    @staticmethod
    def _get_con():
        db = MySQLdb.connect(host=settings.DB_HOST, user=settings.DB_USER, passwd=settings.DB_PWD,
                             port=settings.DB_PORT, db=settings.DB_NAME)
        db.autocommit(True)
        return db
