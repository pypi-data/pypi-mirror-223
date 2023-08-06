import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from datetime import datetime
from dotenv import load_dotenv
import pytest
from entity_type.EntityType import EntityType



load_dotenv()

ENTITY_NAME = "TEST"+str(datetime.now())
ENTITY_NAME_INVALID = "INVALID"
USER_ID = 5000091


@pytest.mark.test
def test_insert_select():
    EntityType.insert_entity_type_id_by_name(ENTITY_NAME, USER_ID)
    entity = EntityType.get_entity_type_id_by_name(ENTITY_NAME)
    entity is not None
@pytest.mark.test
def test_select_invalid():
    entity = EntityType.get_entity_type_id_by_name(ENTITY_NAME_INVALID)
    entity is None