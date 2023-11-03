import src.connection as connection


def test_get_connection_connects_to_base():
    conn = connection.get_connection()
    def test_connection(conn):
        query = ('SELECT * FROM currency')

        data = conn.run(query)
        test_data = []
        for row in data:
            test_data.append(
                {
                    'currency_id': row[0],
                    'currency_code': row[1],
                }
            )
        return test_data
    output = test_connection(conn)
    assert isinstance(output, list)
    assert output[0]['currency_id'] == 1