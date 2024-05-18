from backend.dbtimetests.DbOperationsTimeTests import DbOperationsTimeTests

db_operations_timer = DbOperationsTimeTests()
# db_operations_timer.test_insert_time()
# db_operations_timer.test_update_time()
# db_operations_timer.test_delete_time()
db_operations_timer.test_select_time()
db_operations_timer.print()

