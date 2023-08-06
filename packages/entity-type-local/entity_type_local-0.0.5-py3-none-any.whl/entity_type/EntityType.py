from dotenv import load_dotenv
from logger_local.LoggerLocal import logger_local
from circles_local_database_python.database import database
load_dotenv()
obj = {
    'component_id': 116
}
logger_local.init(object=obj)
db = database()
connection = db.connect_to_database()


class EntityType:

    def __init__(self):
        pass

    @staticmethod
    def get_entity_type_id_by_name(entity_type_name):
        entity_type_id = None
        try:
            object1 = {
                'entity_type_name': entity_type_name
            }
            logger_local.start(object=object1)
            sql_query = "SELECT entity_type_id FROM entity_type.entity_type_en_view WHERE entity_type_name = '{}'".format(
                entity_type_name)
            cursor = connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result:
                entity_type_id = result[0]
        except Exception as e:
            logger_local.exception(object=e)
        object1 = {
            'entity_type_id': entity_type_id
        }
        logger_local.end(object=object1)
        return entity_type_id

    @staticmethod
    def insert_entity_type_id_by_name(entity_type_name, user_id):
        try:
            object1 = {
                'entity_type_name': entity_type_name
            }
            logger_local.start(object=object1)
            cursor = connection.cursor()
            query_entity = "INSERT INTO entity_type.entity_type_table(`created_user_id`,`updated_user_id`)" \
                " VALUES ({}, {})".format(user_id, user_id)
            cursor.execute(query_entity)
            last_inserted_id = cursor.lastrowid
            query_entity_ml = "INSERT INTO entity_type.entity_type_ml_table(`entity_type_name`,`entity_type_id`,`lang_code`,`created_user_id`,`updated_user_id`)" \
                              " VALUES (%s, %s, %s, {}, {})".format(
                                  user_id, user_id)
            cursor.execute(query_entity_ml,
                           (entity_type_name, last_inserted_id, 'en'))
            logger_local.end(object={})
            connection.commit()
        except Exception as e:
            logger_local.exception(object=e)
        logger_local.end(object={})
