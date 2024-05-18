import json
from typing import Callable

from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.CassandraHandler import CassandraHandler
from backend.db.MongoHandler import MongoHandler
from backend.db.MsSqlHandler import MsSqlHandler
from backend.db.PostgreSqlHandler import PostgreSqlHandler
import time
from . import Config


def measure_function_time(function: Callable):
    start = time.time()
    function()
    end = time.time()
    return end - start


class DbOperationsTimeTests:
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SELECT = "SELECT"

    MONGO = "MONGO"
    POSTGRES = "POSTGRES"
    CASSANDRA = "CASSANDRA"
    MS_SQL = "MS_SQL"

    def __init__(self):
        crime_data_processor = CrimeDataProcessor()
        self.db_handlers = {
            self.MONGO: MongoHandler(crime_data_processor),
            # self.POSTGRES: PostgreSqlHandler(crime_data_processor),
            # self.CASSANDRA: CassandraHandler(crime_data_processor),
            # self.MS_SQL: MsSqlHandler(crime_data_processor)
        }
        self.results = {
            self.INSERT: {
                self.MONGO: {},
                self.POSTGRES: {},
                self.CASSANDRA: {},
                self.MS_SQL: {}
            },
            self.UPDATE: {
                self.MONGO: {},
                self.POSTGRES: {},
                self.CASSANDRA: {},
                self.MS_SQL: {}
            },
            self.DELETE: {
                self.MONGO: {},
                self.POSTGRES: {},
                self.CASSANDRA: {},
                self.MS_SQL: {}
            },
            self.SELECT: {
                self.MONGO: {},
                self.POSTGRES: {},
                self.CASSANDRA: {},
                self.MS_SQL: {}
            }
        }

    def test_insert_time(self):
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.INSERT:
                db_handler.delete_all()
                self.results[self.INSERT][db_name][count] = measure_function_time(lambda: db_handler.insert(count))

    def test_update_time(self):
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.INSERT:
                db_handler.delete_all()
                db_handler.insert_all()
                self.results[self.UPDATE][db_name][count] = measure_function_time(lambda: db_handler.update(count))

    def test_delete_time(self):
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.INSERT:
                db_handler.delete_all()
                db_handler.insert_all()
                self.results[self.DELETE][db_name][count] = measure_function_time(lambda: db_handler.delete(count))

    def test_select_time(self):
        for db_name, db_handler in self.db_handlers.items():
            for dbSize in Config.DB_SIZE_TO_SELECT:
                self.results[self.SELECT][db_name][dbSize] = {}
                for count in Config.RECORD_TO_SELECT:
                    self.results[self.SELECT][db_name][dbSize][count] = {}
                    db_handler.delete_all()
                    db_handler.insert(dbSize)
                    self.results[self.SELECT][db_name][dbSize][count]["select"] = measure_function_time(lambda: db_handler.select(count))
                    self.results[self.SELECT][db_name][dbSize][count]["where_select"] = measure_function_time(lambda: db_handler.where_select(count))
                    self.results[self.SELECT][db_name][dbSize][count]["join_select"] = measure_function_time(lambda: db_handler.join_select(count))
                    self.results[self.SELECT][db_name][dbSize][count]["where_and_order_by_select"] = measure_function_time(lambda: db_handler.where_and_order_by_select(count))
                    self.results[self.SELECT][db_name][dbSize][count]["complicated_select"] = measure_function_time(lambda: db_handler.complicated_select(count))

    def print(self):
        print(json.dumps(self.results))
