from sqlalchemy import create_engine
from sqlalchemy.orm import registry
import pickle

class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class DBConnection(metaclass=Singleton):

    def __init__(
        self,
        username,
        password,
        dbtype="oracle",
        addr="127.0.0.1",
        port="1521",
        dbname="orclpdb",
        schema=None,
        path=None,
        metadata=None,
        cache=True
    ) -> None:

        if dbtype == "oracle":
            self.engine = create_engine(
                f"oracle+cx_oracle://{username}:{password}@{addr}:{port}/?service_name={dbname}")
        elif dbtype == "sqlite":
            if path == None:
                raise ValueError("数据库为sqlite时必须指定path")
            self.engine = create_engine(
                f"sqlite:///{path}")

        self.mapper_registry = registry(metadata=metadata)

        if metadata is None:
            self.mapper_registry.metadata.reflect(
                bind=self.engine, schema=schema)
            # TODO:写缓存metadata的代码
            if cache:
            # 序列化元数据对象
                with open('metadata.pkl', 'wb') as f:
                    pickle.dump(self.mapper_registry.metadata, f)

        self.conn = self.engine.connect().execution_options(stream_results=True)

    @property
    def tables(self):
        return self.mapper_registry.metadata.tables