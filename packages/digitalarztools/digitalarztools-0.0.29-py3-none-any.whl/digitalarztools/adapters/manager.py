import os.path
import traceback
from sqlite3 import Error
from urllib import parse
from typing import Union

from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import Engine, create_engine, select, func, Connection
from sqlalchemy.orm import Session

load_dotenv()
class DBString(BaseModel):
    host: str
    user: str
    password: str
    name: str
    port: str


class DBParams(BaseModel):
    engine: str
    con_str: Union[str, DBString]  # either provide file_path or DBString


class DBManager:
    def __init__(self, db_info: Union[DBParams, Engine]):
        if isinstance(db_info, Engine):
            self.engine: Engine = db_info
        else:
            self.engine: Engine = self.create_sql_alchemy_engine(db_info)
        if self.engine is None:
            raise Exception("Enable to create sql alchemy engine")

    def get_engine(self):
        return self.engine

    def get_session(self):
        return Session(self.engine)

    @classmethod
    def for_sqlite3(cls, db_fp: str) -> 'DBManager':
        """ create a database connection to a SQLite database """
        engine: Engine = cls.create_sql_alchemy_engine(DBParams(**{"engine": "sqlite", "con_params": db_fp}))
        if not os.path.exists(db_fp):
            conn: Connection = None
            try:
                # listen(engine, 'connect', load_spatialite)
                conn = engine.connect()
                conn.execute(".load mod_spatialite.dylib")
                conn.execute(select([func.InitSpatialMetaData()]))
            #     conn = sqlite3.connect(db_fp)
            #     print(sqlite3.version)
            #     engine = create_engine(f"sqlite:////{db_fp}")
            #     return cls(engine)
            except Error as e:
                print(e)
            finally:
                if conn:
                    conn.close()
        return cls(engine)

    @staticmethod
    def create_sql_alchemy_engine(config: DBParams) -> Engine:
        try:
            if config.engine in ["sqlite"]:
                db_string = f'{config.engine}:///{config.con_str}'
            else:
                params = config.con_str
                db_string = f'{config.engine}://{params.user}:{parse.quote(params.password)}@{params.host}:{params.port}/{params.name}'
            return create_engine(db_string, echo=True)
        except Exception as e:
            # da_logger.error()
            traceback.print_exc()
