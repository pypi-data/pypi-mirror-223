from circles_local_database_python.connection import DatabaseFunctions
from dotenv import load_dotenv
from logger_local.LoggerLocal import logger_local

load_dotenv()
object_init = {
    'component_id': 114
}
logger_local.init(object=object_init)



class Importer:
    def __init__(self):
        pass

    def insert_record_data_source(self, data_source_id: int, location_id: int, entity_type_id: int, entity_id: int, url: str, user_id: int):
        object1 = {
            'source_id': data_source_id,
            'entity_type_name': entity_type_id,
            'entity_id': entity_id,
            'url': url,
            'location_id': location_id,
            'user_id': user_id
        }
        logger_local.start(object=object1)
        try:
            database_conn = DatabaseFunctions("importer")
            db = database_conn.connect()
            cursor = db.cursor()

            cursor.execute(
                "SELECT country_id FROM location.location_table WHERE id = '{}'".format(location_id))
            country_id = cursor.fetchone()[0]
            cursor.close()
            query_importer = "INSERT INTO importer.importer_table(`source_id`,`country_id`,`entity_type_id`,`entity_id`,`url`,`created_user_id`,`updated_user_id`)" \
                " VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor = db.cursor()
            cursor.execute(
                query_importer, (data_source_id, country_id, entity_type_id, entity_id, url, user_id, user_id))
            cursor.close()
            db.commit()
            db.close()
            logger_local.info("add importer record succeeded")#view logger_local.end at the end of the function
        except Exception as e:
            logger_local.exception(object=e)
        logger_local.end(object={})


if __name__ == "__main__":
    pass
