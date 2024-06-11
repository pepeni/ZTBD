import json
from typing import Callable

from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.CassandraHandler import CassandraHandler
from backend.db.MongoHandler import MongoHandler
from backend.db.MsSqlHandler import MsSqlHandler
from backend.db.PostgreSqlHandler import PostgreSqlHandler
import time
from . import Config
from ..data_utils.file_operations import FileOperations


def measure_function_time(function: Callable) -> float:
    start = time.time()
    function()
    end = time.time()
    return end - start


class DbOperationsTimeTests:
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SELECT_SIMPLE = "SELECT_SIMPLE"
    SELECT_WHERE = "SELECT_WHERE"
    SELECT_JOIN = "SELECT_JOIN"
    SELECT_WHERE_ORDERBY = "SELECT_WHERE_ORDERBY"
    SELECT_COMPLICATED = "SELECT_COMPLICATED"
    SELECT_COMPLICATED_AGGREGATION = "SELECT_COMPLICATED_AGGREGATION"

    MONGO = "MONGO"
    CASSANDRA = "CASSANDRA"
    POSTGRES = "POSTGRES"
    MS_SQL = "MS_SQL"

    def __init__(self) -> None:
        crime_data_processor = CrimeDataProcessor()
        self.db_handlers = {
            self.MONGO: MongoHandler(crime_data_processor),
            self.POSTGRES: PostgreSqlHandler(crime_data_processor),
            # self.CASSANDRA: CassandraHandler(crime_data_processor),
            # self.MS_SQL: MsSqlHandler(crime_data_processor)
        }
        self.results = {
            self.INSERT: {
                self.MONGO: {},
                self.CASSANDRA: {},
                self.POSTGRES: {},
                self.MS_SQL: {}
            },
            self.UPDATE: {
                self.MONGO: {},
                self.CASSANDRA: {},
                self.POSTGRES: {},
                self.MS_SQL: {}
            },
            self.DELETE: {
                self.MONGO: {},
                self.CASSANDRA: {},
                self.POSTGRES: {},
                self.MS_SQL: {}
            },
            self.SELECT_SIMPLE: {
                self.MONGO: {},
                self.CASSANDRA: {},
                self.POSTGRES: {},
                self.MS_SQL: {}
            },
            self.SELECT_WHERE: {
                self.MONGO: {},
                self.CASSANDRA: {},
                self.POSTGRES: {},
                self.MS_SQL: {}
            },
            self.SELECT_JOIN: {
                self.MONGO: {},
                self.CASSANDRA: {},
                self.POSTGRES: {},
                self.MS_SQL: {}
            },
            self.SELECT_WHERE_ORDERBY: {
                self.MONGO: {},
                self.CASSANDRA: {},
                self.POSTGRES: {},
                self.MS_SQL: {}
            },
            self.SELECT_COMPLICATED: {
                self.MONGO: {},
                self.CASSANDRA: {},
                self.POSTGRES: {},
                self.MS_SQL: {}
            },
            self.SELECT_COMPLICATED_AGGREGATION: {
                self.MONGO: {},
                self.CASSANDRA: {},
                self.POSTGRES: {},
                self.MS_SQL: {}
            }
        }

    def test_insert_time(self) -> None:
        print("------------------------------------------------")
        print("----------------INSERT TESTING------------------")
        print("------------------------------------------------\n")
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.INSERT:
                print(f"Inserting {count} records to {db_name}")
                db_handler.delete_all()
                self.results[self.INSERT][db_name][count] = measure_function_time(lambda: db_handler.insert(count))
                print()

    def test_update_time(self) -> None:
        print("------------------------------------------------")
        print("----------------UPDATE TESTING------------------")
        print("------------------------------------------------\n")
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.INSERT:
                print(f"Updating {count} records in {db_name}")
                db_handler.delete_all()
                db_handler.insert_all()
                self.results[self.UPDATE][db_name][count] = measure_function_time(lambda: db_handler.update(count))
                print()

    def test_delete_time(self) -> None:
        print("------------------------------------------------")
        print("----------------DELETE TESTING------------------")
        print("------------------------------------------------\n")
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.INSERT:
                print(f"Deleting {count} records from {db_name}")
                db_handler.delete_all()
                db_handler.insert_all()
                self.results[self.DELETE][db_name][count] = measure_function_time(lambda: db_handler.delete(count))
                print()

    def test_select_simple_time(self) -> None:
        print("------------------------------------------------")
        print("----------------SELECT SIMPLE TESTING------------------")
        print("------------------------------------------------\n")
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.RECORD_TO_SELECT:
                print(f"Selecting(simple) TOP({count}) records in {db_name}")
                db_handler.delete_all()
                db_handler.insert(Config.DB_SIZE_SELECT)
                self.results[self.SELECT_SIMPLE][db_name][count] = measure_function_time(lambda: db_handler.select(count))
                print()

    def test_select_where_time(self) -> None:
        print("------------------------------------------------")
        print("----------------SELECT WHERE TESTING------------------")
        print("------------------------------------------------\n")
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.RECORD_TO_SELECT:
                print(f"Selecting(where) TOP({count}) records in {db_name}")
                db_handler.delete_all()
                db_handler.insert(Config.DB_SIZE_SELECT)
                self.results[self.SELECT_WHERE][db_name][count] = measure_function_time(lambda: db_handler.where_select(count))
                print()

    def test_select_join_time(self) -> None:
        print("------------------------------------------------")
        print("----------------SELECT JOIN TESTING------------------")
        print("------------------------------------------------\n")
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.RECORD_TO_SELECT:
                print(f"Selecting(where) TOP({count}) records in {db_name}")
                db_handler.delete_all()
                db_handler.insert(Config.DB_SIZE_SELECT)
                self.results[self.SELECT_JOIN][db_name][count] = measure_function_time(lambda: db_handler.join_select(count))
                print()

    def test_select_where_and_order_by_time(self) -> None:
        print("------------------------------------------------")
        print("----------------SELECT WHERE AND ORDER BY TESTING------------------")
        print("------------------------------------------------\n")
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.RECORD_TO_SELECT:
                print(f"Selecting(where) TOP({count}) records in {db_name}")
                db_handler.delete_all()
                db_handler.insert(Config.DB_SIZE_SELECT)
                self.results[self.SELECT_WHERE_ORDERBY][db_name][count] = measure_function_time(lambda: db_handler.where_and_order_by_select(count))
                print()

    def test_select_complicated_time(self) -> None:
        print("------------------------------------------------")
        print("----------------SELECT COMPLICATED TESTING------------------")
        print("------------------------------------------------\n")
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.RECORD_TO_SELECT:
                print(f"Selecting(where) TOP({count}) records in {db_name}")
                db_handler.delete_all()
                db_handler.insert(Config.DB_SIZE_SELECT)
                self.results[self.SELECT_COMPLICATED][db_name][count] = measure_function_time(lambda: db_handler.complicated_select(count))
                print()

    def test_select_complicated_aggregation_time(self) -> None:
        print("------------------------------------------------")
        print("----------------SELECT COMPLICATED TESTING------------------")
        print("------------------------------------------------\n")
        for db_name, db_handler in self.db_handlers.items():
            for count in Config.RECORD_TO_SELECT:
                print(f"Selecting(where) TOP({count}) records in {db_name}")
                db_handler.delete_all()
                db_handler.insert(Config.DB_SIZE_SELECT)
                self.results[self.SELECT_COMPLICATED_AGGREGATION][db_name][count] = measure_function_time(lambda: db_handler.complicated_with_aggregation_select(count))
                print()

    def print(self) -> None:
        print(json.dumps(self.results))

    def save_results(self) -> None:
        file_operations = FileOperations()
        file_operations.save_results_to_file(self.results)
