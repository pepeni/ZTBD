from backend.data_utils.file_operations import FileOperations
from backend.data_utils.plotting import Plotting
from backend.dbtimetests.DbOperationsTimeTests import DbOperationsTimeTests

if __name__ == '__main__':
    file_operations = FileOperations()
    file_operations.create_dirs()

    db_operations_timer = DbOperationsTimeTests()
    db_operations_timer.test_insert_time()
    db_operations_timer.test_update_time()
    db_operations_timer.test_delete_time()
    db_operations_timer.test_select_simple_time()
    db_operations_timer.test_select_where_time()
    db_operations_timer.test_select_join_time()
    db_operations_timer.test_select_where_and_order_by_time()
    db_operations_timer.test_select_complicated_time()
    db_operations_timer.print()
    db_operations_timer.save_results()

    plotting = Plotting()
    plotting.create_charts_from_json()
