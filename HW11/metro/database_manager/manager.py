import psycopg2
import psycopg2.extras
from psycopg2._psycopg import connection, cursor
from abc import ABC


class DBModel(ABC):  # abstract base Database model
    TABLE: str  # table name
    PK: str  # primary key column of the table

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {vars(self)}>"


class DBManager:

    def __init__(self) -> None:
        self.database = "metro"
        self.user = "amir"
        self.host = "localhost"
        self.port = 5432
        self.password = "amir1377"

        self.conn: connection = psycopg2.connect(dbname=self.database, user=self.user, password=self.password, host=self.host, port=self.port)

    def __del__(self):
        self.conn.close()  # Close the connection on delete

    def __get_cursor(self) -> cursor:
        # Changing the fetch output from Tuple to Dict utilizing RealDictCursor cursor factory
        return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def create(self, model_instance: DBModel) -> int:
        with self.conn:
            assert isinstance(model_instance, DBModel)
            curs = self.__get_cursor()
            model_vars = vars(model_instance)  # get model variables as a dict ->{'first_name':"akbar", 'last_name':...}
            model_fields_str = ",".join(
                model_vars.keys())  # get field names in string format->first_name, last_name,..
            model_values_str = ",".join(["%s"] * len(model_vars))  # generate %s, %s,... string with suitable length
            model_values_tuple = tuple(model_vars.values())  # get model values in a tuple-> ('akbar', 'babaii', ...)
            with curs:
                curs.execute(
                    f"""INSERT INTO {model_instance.TABLE}({model_fields_str}) VALUES ({model_values_str}) RETURNING ID;""",
                    model_values_tuple)
                id = str(curs.fetchone()['id'])  # get ID of inserted row
                setattr(model_instance, 'id', id)  # set ID into the input model_instance
                return id

    def read(self, model_class: type, pk) -> DBModel:  # get
        assert issubclass(model_class, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                pk ="'"+pk+"'"
                curs.execute(f"SELECT * FROM {model_class.TABLE} WHERE {model_class.PK} = {pk}")
                # curs.execute("select * from users where id='mmd49078'")
                res = curs.fetchone()
                return model_class(**dict(res))  # returns an instance of the Model with inserted values

    def update(self, model_instance: DBModel) -> None:
        assert isinstance(model_instance, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                model_vars = vars(model_instance)
                model_pk_value = getattr(model_instance, model_instance.PK)  # value of pk (for ex. 'id' in patient)
                model_set_values = [f"{field} = %s" for field in model_vars]  # -> ['first_name=%s', 'last_name'=%s,...]
                model_values_tuple = tuple(model_vars.values())
                curs.execute(f"""UPDATE {model_instance.TABLE} SET {','.join(model_set_values)}
                 WHERE {model_instance.PK} = {model_pk_value};""", model_values_tuple)

    def delete(self, model_instance: DBModel) -> None:
        assert isinstance(model_instance, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                model_pk_value = getattr(model_instance, model_instance.PK)
                curs.execute(f"""DELETE FROM {model_instance.TABLE} WHERE {model_instance.PK} = {model_pk_value};""")
                delattr(model_instance, 'id')  # deleting attribute 'id' from the deleted instance
