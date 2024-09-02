from sqlalchemy import text
import sqlalchemy


def create_object_db(path: str) -> tuple[int, None] | tuple[int, str]:
    """Создание Базы Данных по пути path"""

    for_create_path = path[:path.rfind('/')]
    for_create_db = path[path.rfind('/') + 1:]

    try:
        with sqlalchemy.create_engine(for_create_path, isolation_level='AUTOCOMMIT').connect() as connection:
            connection.execute(text(f'CREATE DATABASE {for_create_db}'))
        print(f'База данных {for_create_db} успешно создалась')
        return 1, None
    except (sqlalchemy.exc.OperationalError, UnicodeDecodeError) as e:
        return -1, e
    except sqlalchemy.exc.ProgrammingError as e:
        return -2, e