# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb, logging, traceback, time
from myspiders import settings

class MyspidersPipeline(object):

    def __init__(self):
        self.db = self._get_con()
        self.cursor = self.db.cursor()

    def update_item(self,table_name, row):
        sql = "SELECT id FROM %s WHERE flightNumber='%s' AND depTime=%s" % (table_name, row['flightNumber'], row['depTime'])
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            row_id = result[0]
            sql_update = "UPDATE %s SET %s " % (table_name, ', '.join('{}=%s'.format(k) for k in row))
            sql_update += "WHERE id = %s" % row_id
            values = tuple(row[key] for key in row)
            try:
                self.cursor.execute(sql_update, values)
            except:
                logging.error('update item error')
            return True
        return False

    def addRow(self, tablename, rowdict):
        rowdict['addTime'] = rowdict.get('getTime')
        keys = rowdict.keys()
        columns = ", ".join(keys)
        values_template = ", ".join(["%s"] * len(keys))

        sql = "insert into %s (%s) values (%s)" % (tablename, columns, values_template)
        values = tuple(rowdict[key] for key in keys)
        try:
            self.cursor.execute(sql, values)
            logging.info('%s:%s->%s at %s' % (rowdict.get('flightNumber'), rowdict.get('depAirport'), rowdict.get('arrAirport'), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rowdict.get('depTime')))))
        except:
            traceback.print_exc()
            logging.error('add error')

    def process_item(self, item, spider):
        try:
            self.db.ping()
        except:
            self.db = self._get_con()
            self.cursor = self.db.cursor()
        if not self.update_item('ticket_tickets', item):
            self.addRow('ticket_tickets', item)

    @staticmethod
    def _get_con():
        db = MySQLdb.connect(host=settings.DB_HOST, user=settings.DB_USER, passwd=settings.DB_PWD,
                             port=settings.DB_PORT, db=settings.DB_NAME)
        db.autocommit(True)
        return db
