import datetime
import re
from datetime import datetime
import json
import time
from decimal import Decimal
import math
import random

import pymysql
import pytz
import xlrd
from django.utils import timezone
from xlrd import xldate_as_tuple

from ..services.DataConsolidation import DataConsolidation


class DataExeclService:
    @staticmethod
    def excl_import(configure, table_name, file_path):
        # save_dir = "static/upload"
        # filename = "user_base_info.xlsx"
        # 文件地址
        # file_path = re.sub(r"[/\\]{1,3}", "/", f"{str(BASE_DIR)}/{save_dir}/{filename}")
        # 打开上传 excel 表格
        readboot = xlrd.open_workbook(file_path)
        sheet = readboot.sheet_by_index(0)
        # # 获取excel的行和列
        nrows = sheet.nrows  # 行
        ncols = sheet.ncols  # 列
        first_row_values = sheet.row_values(0)  # 第一行数据
        list = []
        num = 1
        for row_num in range(1, nrows):
            row_values = sheet.row_values(row_num)
            if row_values:
                str_obj = {}
            for i in range(len(first_row_values)):
                ctype = sheet.cell(num, i).ctype
                cell = sheet.cell_value(num, i)
                if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
                    cell = int(cell)  # 浮点转成整型
                    cell = str(cell)  # 转成整型后再转成字符串，如果想要整型就去掉该行
                elif ctype == 3:
                    date = datetime(*xldate_as_tuple(cell, 0))
                    cell = date.strftime('%Y/%m/%d %H:%M:%S')
                elif ctype == 4:
                    cell = True if cell == 1 else False
                str_obj[first_row_values[i]] = cell
            list.append(str_obj)
            num = num + 1
        configure = json.loads(configure)  # 连接数据库配置
        # 获得表字段
        field, err_txt = DataConsolidation.list_col(configure['localhost'], configure['port'], configure['username'],
                                                    configure['password'], configure['database'], table_name)
        if err_txt:
            return None, "连接数据库表失败"
        data = {
            "list": list,
            "rows": nrows - 1,
            "table": table_name,
            "field": field
        }
        return data, None

    @staticmethod
    def data_migrate(file_path, configure, export_field, old_table_id, new_table_id):
        configure = json.loads(configure)  # 连接数据库配置
        try:
            target_db = pymysql.connect(
                host=configure['localhost'],
                port=int(configure['port']),
                user=configure['username'],
                password=configure['password'],
                db=configure['database'],
                charset="utf8",
            )
        except Exception as err:
            return None, "目标数据库连接失败"
        conn = target_db.cursor()
        where = "id = " + new_table_id
        table_name_sql = "SELECT `table_name` FROM migrate_platform_table WHERE {};".format(where)
        conn.execute(table_name_sql)
        table_name = conn.fetchone()
        data = DataExeclService.excl_import(json.dumps(configure), table_name[0], file_path)
        print(data)
        import_data = data[0]["list"]
        # 连接目标数据库
        # try:
        num = 0
        for dict in import_data:
            # row = tuple(i)
            if "id" in dict.keys():
                old_id = dict.pop("id")  # 弹出id 返回旧表主键id
                field = export_field.lstrip("id,")  # 去除首部id
            row = tuple(dict.values())  # 字典转元组
            sql = "INSERT INTO `{}` ({}) VALUES {};".format(table_name[0], field, row)
            print(sql)
            sql = sql.replace("''", "NULL").replace("''", "NULL")  # 处理空数据
            sql = sql.replace("'{}'", "NULL").replace("'{}'", "NULL")  # 处理空json
            conn.execute(sql)
            new_id = conn.lastrowid  # 返回新表主键id
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
            # 迁移映射表数据
            migrate_old_to_new_data = {
                'old_table_id': old_table_id,
                'new_table_id': new_table_id,
                'old_data_id': old_id,
                'new_data_id': new_id,
                'created_time': now
            }
            migrate_old_to_new_data = tuple(migrate_old_to_new_data.values())  #
            # 迁移映射表数据插入
            migrate_old_to_new_field = "old_table_id,new_table_id,old_data_id,new_data_id,created_time"
            old_new_sql = "INSERT INTO `{}` ({}) VALUES {};".format("migrate_old_to_new", migrate_old_to_new_field,
                                                                    migrate_old_to_new_data)
            # print(old_new_sql)
            conn.execute(old_new_sql)

            num = num + 1
        # except Exception as e:
        #     return None, str(e)
        target_db.commit()
        conn.close()
        data = {
            "rows": num
        }
        return data, None

    @staticmethod
    def data_cover(file_path, configure, table_name, cover_where, cover_field):
        configure = json.loads(configure)  # 连接数据库配置
        try:
            target_db = pymysql.connect(
                host=configure['localhost'],
                port=int(configure['port']),
                user=configure['username'],
                password=configure['password'],
                db=configure['database'],
                charset="utf8",
            )
        except Exception as err:
            return None, "目标数据库连接失败"
        conn = target_db.cursor()
        readboot = xlrd.open_workbook(file_path)
        sheet = readboot.sheet_by_index(0)
        # # 获取excel的行和列
        nrows = sheet.nrows  # 行
        ncols = sheet.ncols  # 列
        first_row_values = sheet.row_values(0)  # 第一行数据
        list = []
        try:
            num = 1
            for row_num in range(1, nrows):
                row_values = sheet.row_values(row_num)
                if row_values:
                    str_obj = {}
                for i in range(len(first_row_values)):
                    ctype = sheet.cell(num, i).ctype
                    cell = sheet.cell_value(num, i)
                    if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
                        cell = int(cell)  # 浮点转成整型
                        cell = str(cell)  # 转成整型后再转成字符串，如果想要整型就去掉该行
                    elif ctype == 3:
                        date = datetime(*xldate_as_tuple(cell, 0))
                        cell = date.strftime('%Y/%m/%d %H:%M:%S')
                    elif ctype == 4:
                        cell = True if cell == 1 else False
                    str_obj[first_row_values[i]] = cell
                list.append(str_obj)
                num = num + 1

            # del list[0]
            success_num = 0
            for dict in list:
                where = cover_where + "=" + "'" + dict[cover_where] + "'"
                select_sql = "SELECT * FROM {} WHERE {};".format(table_name, where)
                select_sql = select_sql.replace("''", "NULL").replace("''", "NULL")  # 处理空数据
                select_sql = select_sql.replace("'{}'", "NULL").replace("'{}'", "NULL")  # 处理空json
                conn.execute(select_sql)
                select_data = conn.fetchone()
                # print(select_sql)
                if select_data:
                    li = []
                    for i in cover_field.split(","):
                        if len(dict[i]) > 0:
                            update = i + "=" + "'" + dict[i] + "'"
                        else:
                            update = i + "=" + "''"
                        li.append(update)
                    str1 = ','.join(li)
                    sql = "UPDATE `{}` SET {} WHERE {};".format(table_name, str1, where)
                    sql = sql.replace("''", "NULL").replace("''", "NULL")  # 处理空数据
                    sql = sql.replace("'{}'", "NULL").replace("'{}'", "NULL")  # 处理空json
                    conn.execute(sql)
                    success_num = success_num + 1

        except Exception as e:
            return None, e
        target_db.commit()
        conn.close()
        data = {
            "rows": success_num
        }
        return data, None

    """
    @staticmethod
    def data_cover2(file_path, configure, table_name, cover_where, cover_field):
        configure = json.loads(configure)  # 连接数据库配置
        try:
            target_db = pymysql.connect(
                host=configure['localhost'],
                port=int(configure['port']),
                user=configure['username'],
                password=configure['password'],
                db=configure['database'],
                charset="utf8",
            )
        except Exception as err:
            return None, "目标数据库连接失败"
        conn = target_db.cursor()
        readboot = xlrd.open_workbook(file_path)
        sheet = readboot.sheet_by_index(0)
        # # 获取excel的行和列
        nrows = sheet.nrows  # 行
        ncols = sheet.ncols  # 列
        first_row_values = sheet.row_values(0)  # 第一行数据
        list = []
        # try:
        num = 1
        for row_num in range(1, nrows):
            row_values = sheet.row_values(row_num)
            if row_values:
                str_obj = {}
            for i in range(len(first_row_values)):
                ctype = sheet.cell(num, i).ctype
                cell = sheet.cell_value(num, i)
                if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
                    cell = int(cell)  # 浮点转成整型
                    cell = str(cell)  # 转成整型后再转成字符串，如果想要整型就去掉该行
                elif ctype == 3:
                    date = datetime(*xldate_as_tuple(cell, 0))
                    cell = date.strftime('%Y/%m/%d %H:%M:%S')
                elif ctype == 4:
                    cell = True if cell == 1 else False
                str_obj[first_row_values[i]] = cell
            list.append(str_obj)
            num = num + 1

        success_num = 0
        for dict in list:
            seller_id = 0
            warehouse_id = 0
            goods_id = 0
            stock_id = 0
            sellers_sql = "SELECT id FROM sellers WHERE code = '{}';".format(dict['seller_id'])
            sellers_sql = sellers_sql.replace("''", "NULL").replace("''", "NULL")  # 处理空数据
            sellers_sql = sellers_sql.replace("'{}'", "NULL").replace("'{}'", "NULL")  # 处理空json
            conn.execute(sellers_sql)
            sellers_data = conn.fetchone()

            warehouse_sql = "SELECT id FROM warehouses WHERE code = '{}';".format(dict['warehouse_id'])
            warehouse_sql = warehouse_sql.replace("''", "NULL").replace("''", "NULL")  # 处理空数据
            warehouse_sql = warehouse_sql.replace("'{}'", "NULL").replace("'{}'", "NULL")  # 处理空json
            conn.execute(warehouse_sql)
            warehouse_data = conn.fetchone()

            brand_product_code = dict['brand_code'] + dict['product_code']
            goods_sql = "SELECT id FROM goods WHERE brand_product_code = '{}';".format(brand_product_code)
            goods_sql = goods_sql.replace("''", "NULL").replace("''", "NULL")  # 处理空数据
            goods_sql = goods_sql.replace("'{}'", "NULL").replace("'{}'", "NULL")  # 处理空json
            conn.execute(goods_sql)
            goods_data = conn.fetchone()

            if sellers_data:
                seller_id = sellers_data[0]
            if warehouse_data:
                warehouse_id = warehouse_data[0]
            if goods_data:
                goods_id = goods_data[0]
            if goods_data and warehouse_data:
                stocks_sql = "SELECT id FROM warehouse_good_stocks WHERE warehouse_id = '{}'and good_id = '{}';".format(
                    warehouse_id, goods_id)
                stocks_sql = stocks_sql.replace("''", "NULL").replace("''", "NULL")  # 处理空数据
                stocks_sql = stocks_sql.replace("'{}'", "NULL").replace("'{}'", "NULL")  # 处理空json
                conn.execute(stocks_sql)
                stocks_data = conn.fetchone()
                if stocks_data:
                    stock_id = stocks_data[0]

            num = re.sub(' ', "", re.sub(':', "", re.sub(r'/', "", dict['created_at'])))

            while True:
                number = ''.join(str(x) for x in random.sample(range(10), 4))
                number1 = ''.join(str(x) for x in random.sample(range(10), 4))
                if not number.startswith('0') and not number1.startswith('0'):
                    break
            tz = pytz.timezone('Asia/Shanghai')
            now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
            order_data = {
                'seller_id': seller_id,
                'warehouse_id': warehouse_id,
                'number': "S" + num + number,
                "out_number": dict['out_number'],
                'default_amount': abs(float(dict['default_unit_price']) * int(dict['count'])),
                'amount': abs(float(dict['amount'])),
                'purchasing_amount': abs(float(dict['purchasing_amount']) * int(dict['count'])),
                'checkout_status': 2,
                # 'status': dict['status'],
                'status': dict['status'],
                'finish_time': dict['finish_time'],
                'created_at': dict['created_at'],
            }
            order_data = tuple(order_data.values())
            old_new_sql = "INSERT INTO `{}` ({}) VALUES {};".format("sale_orders",
                                                                    "seller_id,warehouse_id,number,out_number,default_amount,amount,purchasing_amount,checkout_status,status,finish_time,created_at",
                                                                    order_data)

            conn.execute(old_new_sql)

            order_lists_data = {
                'sale_order_id': conn.lastrowid,
                'number': "ZS" + num + number,
                "sale_label": '正品',
                'count': abs(int(dict['count'])),
                'default_unit_price': abs(float(dict['default_unit_price'])),
                'unit_price': abs(float(dict['default_unit_price']) + float(dict['unit_price'])),
                'default_amount': abs(float(dict['default_unit_price']) * int(dict['count'])),
                'amount': abs(float(dict['amount'])),
                'purchasing_amount': abs(float(dict['purchasing_amount']) * int(dict['count'])),
                'invoice_status': 1,
                'settlement_status': 1,
                "stock_id": stock_id,
                'created_at': dict['created_at'],
            }
            order_lists_data = tuple(order_lists_data.values())
            order_lists_sql = "INSERT INTO `{}` ({}) VALUES {};".format("sale_order_lists",
                                                                        "sale_order_id,number,sale_label,count,default_unit_price,unit_price,default_amount,amount,purchasing_amount,invoice_status,settlement_status,stock_id,created_at",
                                                                        order_lists_data)

            conn.execute(order_lists_sql)
            success_num = success_num + 1
        target_db.commit()
        conn.close()
        data = {
            "rows": success_num
        }
        return data, None """
