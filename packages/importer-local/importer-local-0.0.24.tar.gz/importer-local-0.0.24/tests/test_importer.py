import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
import pytest
from circles_importer.importer import Importer
from logger_local.LoggerLocal import logger_local
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.connection import DatabaseFunctions
LOCATION_ID = 17241
ENTITY_TYPE_ID = 1
ENTITY_ID = 1
DATA_SOURCE_ID = 7
USER_ID = 1
IMPORTER_LOCAL_PYTHON_COMPONENT_ID=114
URL = "https://example.com"
object_init = {
    'component_id': IMPORTER_LOCAL_PYTHON_COMPONENT_ID,
    'component_name':"importer_local",
    'component_category':LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework':LoggerComponentEnum.testingFramework.Python_Unittest.value
}
logger_local.init(object=object_init)


class TestImporter():
    importer=Importer()
    @pytest.mark.test
    def test_insert_record_data_source(self):
        database_conn = DatabaseFunctions('importer')
        db = database_conn.connect()
        cursor = db.cursor()
        logger_local.start(object={})
        self.importer.insert_record_data_source(
            url=URL,user_id=USER_ID,data_source_id=DATA_SOURCE_ID,location_id=LOCATION_ID,entity_type_id=ENTITY_TYPE_ID,entity_id=ENTITY_ID)
        sql_query="select source_id,entity_type_id,entity_id,url from importer.importer_table where created_user_id={} order by created_timestamp desc limit 1".format(USER_ID)
        cursor.execute(sql_query)
        token=cursor.fetchone()
        assert token[0]==DATA_SOURCE_ID
        assert token[1]==ENTITY_TYPE_ID
        assert token[2]==ENTITY_ID
        assert token[3]==URL
        logger_local.end(object={})


