# encoding: utf-8
"""
@project: djangoModel->synchronous_mysql_synchronous
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 使用pandas，数据库同步脚本
@created_time: 2023/5/18 17:47
"""
import json
import os
import time

from django.core.management.base import BaseCommand, no_translations
from pandas import DataFrame
import pandas as pd
import pymysql
import sqlalchemy
from sqlalchemy import create_engine

from config.config import JConfig
from xj_migrate.utils.custom_tool import format_params_handle, write_to_log, force_transform_type


# 迁移配置协议结构：
# [
#     {
#         "source_table": "flow_flow",
#         "target_table": "flow_flow2",
#         "primary_key": "id",
#         "filter_fields": [
#         ],
#         "remove_fields": [
#         ],
#         "alice_fields": {
#             "module_name": "module_name2"
#         },
#         # note 追加模式启用 relate_other_table_key
#         "relate_other_table_key": [
#             {
#                 "source_table": "flow_flow",
#                 "source_field": "flow_flow2",
#                 "foreign_key": "id"
#             }
#         ],
#         # note 后面面扩展功能实现数据清洗，然后再入库。
#         "data_cleaning": []
#     }
# ]

# 自定义异常类，记录异常，并打印错误信息
class MigrateError(Exception):
    def __init__(self, err_msg=None, *args, catch_err=None, **kwargs):
        super().__init__(self)
        self.err_msg = err_msg or str(catch_err)
        self.catch_err = catch_err

    def __str__(self):
        if self.catch_err:
            write_to_log(prefix="迁移异常", err_obj=self.catch_err)
        else:
            write_to_log(prefix="迁移异常", content=self.err_msg)
        err_msg = self.err_msg or str(self.catch_err)
        return err_msg


class Command(BaseCommand):
    # note 注意不同结构的表进行同步时候，需要设计好迁移的表的执行顺序、字段映射、迁移表映射。还有外键冲突，
    # 报错 TypeError: __init__() got multiple values for argument 'schema' ===>>> 处理方案： 更新依赖包：sqlalchemy==1.4.46，pandas==1.3.5
    # 报错：sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1054, "Unknown column 'index' in 'field list'") ===>>> 处理：index=False

    help = "同步数据库中配置表的结构和数据"
    from_engine = None  # 迁移源数据库配置
    to_engines = []  # 被迁移的数据配置
    migrate_configure = {}  # 迁移的表映射
    append_table_id_mapping = {}  # 追加模式的时候字段冲突，主键ID映射。其他关联的表获自行获取修改关联ID。
    __conflict_record = {}

    def get_conflict_record(self, *args, table_name=None, conflict_key=None, **kwargs):
        # 获取冲突记录
        if table_name is None:
            return self.__conflict_record
        elif not table_name is None and conflict_key is None:
            return self.__conflict_record.get(table_name, {})
        elif not table_name is None and not conflict_key is None:
            return self.__conflict_record.get(table_name, {}).get(conflict_key, None)
        return self.__conflict_record

    def set_conflict_record(self, *args, table_name=None, conflict_key=None, conflict_value=None, **kwargs):
        # 创建冲突映射
        if not self.__conflict_record.get(table_name):
            self.__conflict_record[table_name] = {}
        self.__conflict_record[table_name][conflict_key] = conflict_value
        # 同步到本地文件中
        self.conflict_record_fp.seek(0)
        self.conflict_record_fp.truncate()
        json.dump(self.__conflict_record, self.conflict_record_fp)

    def add_arguments(self, parser):
        parser.add_argument('--type',
                            dest='type',
                            default="replace",
                            help='迁移数据库，采用追加模式还是替换模式')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = JConfig()
        today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        save_path = self.config.get_base_dir() + "/resource_files/backup_files/" + today + '/'
        # ============ section 数据库连接相关 start===================
        self.from_engine = None
        self.to_engines = []
        self.from_db_map = self.config.get_list_by_cut(
            section="xj_migrate",
            option="migrate_from_db",
            map_key_list=["host", "user", "password", "database", "port"],
            cut_char=","
        )
        self.migrate_to_dbs = self.config.parse_lines_tuple(
            section="xj_migrate",
            option="migrate_to_dbs",
            cut_char=",",
            map_key_list=["host", "user", "password", "database", "port"]
        )
        # 来源数据库创建连接
        self.from_engine, err = self.create_connect(self.from_db_map, use_create_engine=True)
        if err:
            raise MigrateError("无法连接迁移源")
        # 同步的数据库创建连接
        for i in self.migrate_to_dbs:
            conn, err = self.create_connect(i, use_create_engine=True)
            if err:
                raise MigrateError("无法连接目标源")
            self.to_engines.append(conn)
        # ============ section 数据库连接相关 end  ===================

        # 迁移配置
        self.migrate_configure = self.config.load_json_configure("migrate_configure.json", default=[])
        self.target_table_to_primary_key = {i["target_table"]: i["primary_key"] for i in self.migrate_configure}
        self.migrate_configure = {i["source_table"]: i for i in self.migrate_configure}
        self.migrate_tables = self.config.get_list_by_cut(section="xj_migrate", option="migrate_tables", cut_char=",")

        # 冲突记录
        conflict_record_file_name = "conflict_record_" + str(int(time.time())) + ".json"
        self.conflict_record_fp = open(save_path + conflict_record_file_name, mode="w", encoding="utf-8")
        self.__conflict_record = {}

    @staticmethod
    def create_connect(config_dict: dict = None, use_sqlalchemy: bool = True, **kwargs):
        """
        构建数据库连接
        :param config_dict: 数据库参数
        :param use_sqlalchemy: 是否使用sqlalchemy引擎
        :return: data,err
        """
        # ================== section 获取基础参数 start ===============================
        config_dict, is_pass = force_transform_type(variable=config_dict, var_type="only_dict", default={})
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        config_dict.update(kwargs)
        host = config_dict.get("host", None)
        user = config_dict.get("user", None)
        password = config_dict.get("password", None)
        database = config_dict.get("database", None)
        port, is_pass = force_transform_type(variable=config_dict.get("port", None), var_type="int")
        use_sqlalchemy, is_pass = force_transform_type(variable=use_sqlalchemy, var_type="bool", default=False)
        if not host or not user or not password or not port:
            return None, "参数错误"
        # ================== section 获取基础参数 end ===============================
        try:
            # 使用sqlalchemy引擎
            if use_sqlalchemy:
                # 注意由于pandas兼容问题，写入的时候需要使用
                mysql_client_str = 'mysql+pymysql://' + str(user) + ':' + str(password) + '@' + str(host) + ':' + str(port) + '/' + str(database)
                return create_engine(mysql_client_str), None
            else:
                # 直接使用pymysql
                config_dict["port"], is_pass = force_transform_type(variable=config_dict.get("port", 3306), var_type="int", default=3306)
                return pymysql.connect(host=host, user=user, password=password, database=database, port=port), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def insert_by_sql(table, conn, keys, insert_tuple):
        """
        执行sql插入数据
        :param table: 表对象
        :param conn: 连接对象
        :param keys: 插入字段列表
        :param data_iter: 遍历数据
        :return: code ,err_msg
        """
        # 插入数据keys
        insert_keys_str = ""
        for k in keys:
            insert_keys_str = insert_keys_str + ("" if not insert_keys_str else ",") + k
        # 拼接values
        insert_value_str = ""
        for k in keys:
            insert_value_str = insert_value_str + ("" if not insert_value_str else ",") + "%s"
        # 拼接sql
        sql = """INSERT INTO `{TABLE_NAME}` ({INSERT_KEYS}) VALUES({INSERT_VALUES});""".format(
            TABLE_NAME=table.name,
            INSERT_KEYS=insert_keys_str,
            INSERT_VALUES=insert_value_str,
        )
        # 创建数据库游标对象
        dbapi_conn = conn.connection
        with dbapi_conn.cursor() as cursor:
            try:
                cursor.execute(sql, insert_tuple)  # 防止sql注入，使用占位替换方式
                insert_id = dbapi_conn.insert_id()
                return 0, None, insert_id
            except Exception as io_err:
                code, msg = io_err.args
                return code, msg, None

    @staticmethod
    def table_fields_types(engine, table_name: str = None):
        table = sqlalchemy.Table(table_name, sqlalchemy.MetaData(), autoload=True, autoload_with=engine)
        return {k: v.type for k, v in table.c.items()}

    def data_backup(self, pf, table_name="", save_type="to_json"):
        """在同步之前，把目标表做一次备份"""
        if not save_type in save_type:
            return False, "不是有效的保存方式"
        today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        save_path = self.config.get_base_dir() + "/resource_files/backup_files/" + today + '/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_name = table_name + "-" + today + "-backup"
        save_path = save_path + save_name
        if save_type == "to_json":
            pf.to_json(save_path + ".json")
        elif save_type == "to_csv":
            pf.to_csv(save_path + ".csv")
        elif save_type == "to_excel":
            pf.to_excel(save_path + ".xlsx")

    def replace_insert(self, df: DataFrame, migrate_table, to_engine, fields_dtype, source_table, **kwargs):
        """替换默认插入"""
        df.to_sql(
            name=migrate_table,
            con=to_engine,
            if_exists="replace",
            dtype=fields_dtype,
            index=False
        )
        # note 替换模式会覆盖掉原有的主键ID，所以需要重新加回来。 暂时pandas还没有更好的解决办法
        primary_key = self.migrate_configure.get(source_table, {}).get("primary_key", "id")
        con = to_engine.connect()
        con.execute("""ALTER TABLE `{}`
        MODIFY COLUMN `{}` bigint(20) NOT NULL AUTO_INCREMENT FIRST,
        ADD PRIMARY KEY (`{}`);""".format(migrate_table, primary_key, primary_key))

    def append_insert(self, df: DataFrame, migrate_table, to_engine, fields_mapping, source_table, **kwargs):
        """追加模式插入"""
        # note 保存之前处理外键关联的问题，所以设计好导入的顺序。先导入的结果会影响后面的结果
        df.to_sql(
            name=migrate_table,
            con=to_engine,
            if_exists="append",
            dtype=fields_mapping,
            index=False,
            method=self.append_insert_callback
        )

    def append_insert_callback(self, table, conn, keys, data_iter, **kwargs):
        """
        Pandas中to_sql方法的回调函数
        :param table:Pandas的table
        :param conn:数据库驱动连接对象
        :param keys:要存入的字段名
        :param data_iter:DataFrame对象也就是数据迭代器
        :return:
        """
        primary_key = self.target_table_to_primary_key.get(str(table.name), "id")
        for item in data_iter:
            code, err_msg, last_insert_id = self.insert_by_sql(table, conn, keys, item)
            value_map = {k: v for k, v in zip(keys, item)}
            if code == 1062:
                # 主键冲突，去除主键，建立冲突映射
                old_primary_key = value_map.pop(primary_key, None)
                code, msg, last_insert_id = self.insert_by_sql(table, conn, list(value_map.keys()), list(value_map.values()))
                self.set_conflict_record(table_name=table.name, conflict_key=old_primary_key, conflict_value=last_insert_id)

    @no_translations
    def handle(self, *args, **options):
        # note 业务逻辑入口
        migrate_type = options["type"] if options.get("type") in ["replace", "append"] else "replace"
        if not self.migrate_tables:
            raise MigrateError("没有找到需要迁移的表")

        for table_name in self.migrate_tables:
            # 获取对应表的配置信息
            current_table_configure = self.migrate_configure.get(table_name, {})
            migrate_table = current_table_configure.get("target_table", table_name)
            # ============ section 获取源数据 start ===================
            source_pf = pd.read_sql("SELECT * FROM `" + table_name + "`", self.from_engine)
            from_table_fields = self.table_fields_types(engine=self.from_engine, table_name=table_name)
            # ============ section 获取源数据 end   ===================
            for to_engine in self.to_engines:
                target_df = source_pf
                # ============ section 迁移之前先对目标表数据进行备份 start ===================
                try:
                    copy_df = pd.read_sql("SELECT * FROM `" + migrate_table + "`", to_engine)
                    self.data_backup(copy_df, table_name=migrate_table)
                except sqlalchemy.exc.ProgrammingError:
                    pass
                except Exception as e:
                    raise MigrateError(catch_err=e)
                # ============ section 迁移之前先对目标表数据进行备份 end   ===================

                # ============ section 执行字段配置 start ===================
                # 过滤字段
                filter_fields = current_table_configure.get("filter_fields")
                if filter_fields and isinstance(filter_fields, list):
                    target_df = target_df.loc[:, filter_fields]
                # 移除字段
                remove_fields = current_table_configure.get("remove_fields")
                if remove_fields and isinstance(remove_fields, list):
                    target_df = target_df.drop(columns=remove_fields, inplace=False)
                # 别名替换
                alice_fields = current_table_configure.get("alice_fields", {})
                if alice_fields:
                    target_df = target_df.rename(columns=format_params_handle(
                        param_dict=alice_fields,
                        filter_filed_list=target_df.columns.to_list(),
                        alias_dict=alice_fields
                    ))
                # 冲突处理
                # 追加模式字段冲突处理，修改因为外键冲突受影响的数据。如：a表 b_id是b主键ID。b先迁移，但是迁移过程中主键冲突，变成了插入。得到结果： b表 ID 5 ==>> 10 ==>> a表 b_id 修改成10
                relate_keys = current_table_configure.get("relate_other_table_key", [])
                for i in relate_keys:
                    replace_params = self.get_conflict_record(table_name=i["target_table"])
                    if replace_params:
                        target_df[i["foreign_key"]].replace(replace_params, inplace=True)
                # ============ section 执行字段配置 start ===================

                # note 开始迁移
                if migrate_type == "replace":
                    self.replace_insert(
                        df=target_df,
                        migrate_table=migrate_table,
                        to_engine=to_engine,
                        fields_dtype=from_table_fields,
                        source_table=table_name
                    )
                else:
                    self.append_insert(target_df, migrate_table, to_engine, from_table_fields, table_name)

    def __del__(self):
        """迁移完成，释放内存"""
        self.conflict_record_fp.close()
