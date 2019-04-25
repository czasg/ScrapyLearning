from czaSpider.czaTools import *


class CzaSpiderPipeline(object):
    def process_item(self, item, spider):
        pass  # todo this sql exist bug, i can not to read data from this table
        # sql = """select * from source"""
        # conn = get_sqlite3_connection(timeStr=True)
        # conn.cursor().execute(sql)
        # print(conn.cursor().fetchall())
        # if spider.SQLITE3:
        #     data = ['"'+value+'"' if value else '"0"' for key,value in item.items()]
        #     try:
        #         conn = get_sqlite3_connection(timeStr=True)
        #         execute_sql(conn, constant.SQL_INSERT_TABLE.format(*data))
        #         # execute_sql(spider.sqlite3Conn, constant.SQL_INSERT_TABLE.format(*data))
        #     except:
        #         raise ValueError("insert error")
        #     else:
        #         print("insert SQL done")
        #     finally:
        #         return item


        # res = dict(item.copy())
        # print('source')
        # # return None
        # return item
        # try:
        #     spider.collection.insert_one(res)
        # except:
        #     raise ValueError("insert error")
        # else:
        #     print("insert done")
        # finally:
        #     return item