from .connection import get_connection

def query(
    sql: str,
    params: tuple | None = None,
):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(sql, params)

        if sql.lower().startswith('select'):
            return cursor.fetchall()

        connection.commit()
        return cursor.lastrowid

    except Exception as e:
        raise e

    finally:
        cursor.close()
        connection.close()