from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.PostgreSqlHandler import PostgreSqlHandler
from backend.dbtimetests.DbOperationsTimeTests import DbOperationsTimeTests

if __name__ == '__main__':
    db_operations_timer = DbOperationsTimeTests()
    # db_operations_timer.test_insert_time()
    # db_operations_timer.test_update_time()
    # db_operations_timer.test_delete_time()
    db_operations_timer.test_select_time()
    db_operations_timer.print()


