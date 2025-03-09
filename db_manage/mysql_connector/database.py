import os
import json

from db_manage.mysql_connector.db_connector import DBConnector
from db_manage.values import schemas_path



class Database:
    def __init__(self, name):
        self.name = name.title()
        self.schemas = os.path.join(f"{schemas_path}", f"{name}.json")
        self.init()

    def init(self):
        with DBConnector() as db:
            db.create_db_if_doest_exist(self.name)
        with DBConnector(self.name) as db:
            db.create_tables_if_doest_exist(self.schemas)

    def add_object(self, object_type, data):
        with DBConnector(self.name) as db:
            id = db.write_row(object_type.title(), data)
            return id

    def get_list_of_objects(self, object_type, conditions={}, inJson=False):
        objs = []
        with DBConnector(self.name) as db:
            rows = db.get_rows(object_type.title(), conditions)
        if inJson:
            return rows
        command_str = self.create_class(object_type.title())
        for row in rows:
            exec(f"{command_str}\nobjs.append({object_type.title()}(row))")
        return objs

    def get_object_by_id(self, object_type, id, inJson=False):
        with DBConnector(self.name) as db:
            row = db.get_row(object_type.title(), {"id": id})
        if inJson:
            return row
        command_str = self.create_class(object_type.title())
        exec(f"{command_str}\nrow = {object_type.title()}(row)")
        return row
    
    def update_object(self, object_type, id, data):
        with DBConnector(self.name) as db:
            row = db.update_row(object_type.title(), id, data)

    def delete_object(self, object_type, id):
        with DBConnector(self.name) as db:
            row = db.delete_row(object_type.title(), id)


    def create_class(self, class_name):
        command_str = f"class {class_name}:\n\t"
        command_str += f"def __init__(self, data):\n\t\t"
        with open(f"{self.schemas}", 'r') as f:
            object_schema = json.loads(f.read())[class_name.title()]
        command_str += f"self.id = data[\"id\"]\n\t\t"
        for attr in object_schema.keys():
            command_str += f"self.{attr} = data[\"{attr}\"] if \"{attr}\" in data else None\n\t\t"
        return command_str
        