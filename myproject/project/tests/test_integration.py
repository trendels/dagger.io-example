import httpx
import psycopg


def test_server():
    response = httpx.get("http://server:8080/")

    assert response.text == "<h1>Hello, World!</h1>\n"


def test_database():
    with psycopg.connect("postgres://my_user:my_password@db/my_db") as conn:
        result = conn.execute("select 1 + 1").fetchone()[0]

    assert result == 2
