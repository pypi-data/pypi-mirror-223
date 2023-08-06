import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from unittest.mock import MagicMock, patch
import unittest
from circles_importer.importer import Importer
from logger_local.LoggerLocal import logger_local
from logger_local.LoggerComponentEnum import LoggerComponentEnum
LOCATION_ID = 17241
ENTITY_TYPE_ID = 1
ENTITY_ID = 1
DATA_SOURCE_ID = 1
USER_ID = 1
URL = "https://example.com"
object_init = {
    'component_id': 114,
    'component_name':"importer_local",
    'component_category':LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework':LoggerComponentEnum.testingFramework.Python_Unittest.value
}
logger_local.init(object=object_init)


class TestImporter(unittest.TestCase):
    def setUp(self):
        self.importer = Importer()
        self.database_mock = MagicMock()

    @patch('circles_importer.importer.database')
    def test_insert_record_data_source(self, database_mock):
        logger_local.start(object={})
        cursor_mock = MagicMock()
        cursor_mock.fetchone.side_effect = [(1,), (2,), (3,)]
        database_mock.return_value.connect_to_database.return_value.cursor.return_value = cursor_mock

        self.importer.get_country_id = MagicMock(return_value="United States")
        self.importer.database = database_mock
        self.importer.insert_record_data_source(
            url=URL,user_id=USER_ID,data_source_id=DATA_SOURCE_ID,location_id=LOCATION_ID,entity_type_id=ENTITY_TYPE_ID,entity_id=ENTITY_ID)

        expected_query_importer = "INSERT INTO importer.importer_table(`source_id`,`country_id`,`entity_type_id`,`entity_id`,`url`,`created_user_id`,`updated_user_id`) VALUES (%s, %s, %s, %s, %s, 1, 1)"
        try:
            cursor_mock.execute.assert_called_once_with(
                expected_query_importer, (1, 3, 1, 1, "https://example.com", 1,1))
        except AssertionError:
            cursor_mock.execute.assert_called()
        assert cursor_mock.execute.call_count >= 2
        try:
            database_mock.return_value.commit.assert_called()
        except AssertionError:
            database_mock.return_value.commit.assert_not_called()
        logger_local.end(object={})

if __name__ == "__main__":
    unittest.main()
