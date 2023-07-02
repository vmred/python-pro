import sqlite3
from typing import List

from variables import LESSON_3_DB_PATH


def execute_query(query_sql: str) -> List:
    '''
    Функция для выполнения запроса
    :param query_sql: запрос
    :return: результат выполнения запроса
    '''
    connection = sqlite3.connect(LESSON_3_DB_PATH)
    cur = connection.cursor()
    result = cur.execute(query_sql).fetchall()
    connection.close()
    return result


def unwrapper(records: List) -> None:
    '''
    Функция для вывода результата выполнения запроса
    :param records: список ответа БД
    '''
    for record in records:
        print(*record)


def get_employees() -> None:
    '''
    Возвращает список
    '''
    query_sql = '''
        SELECT *
          FROM employees;
    '''
    unwrapper(execute_query(query_sql))


def get_customers(state_name=None, city_name=None) -> List:
    query_sql = '''
        SELECT FirstName
              ,City 
              ,State
          FROM customers
        '''
    filter_query = ''
    if city_name and state_name:
        filter_query = f" WHERE City = '{city_name}' and State = '{state_name}'"
    if city_name and not state_name:
        filter_query = f" WHERE City = '{city_name}'"
    if state_name and not city_name:
        filter_query = f" WHERE State = '{state_name}'"

    query_sql += filter_query
    return execute_query(query_sql)


def get_unique_customers_by_python():
    query_sql = '''
        SELECT FirstName
          FROM customers
    '''
    records = execute_query(query_sql)
    result = set()
    for record in records:
        result.add(record[0])
    return len(result)


def get_unique_customers_by_sql():
    query_sql = '''
            SELECT count(distinct FirstName) as first_names_qty
              FROM customers
    '''

    result = execute_query(query_sql)[0][0]
    return result


def get_invoice_items_profit() -> float:
    """
    Sums profit by invoice_items table
    :return:
        profit value
    """
    query_sql = 'select SUM(ii.UnitPrice * ii.Quantity) from invoice_items as ii;'
    return execute_query(query_sql)[0][0]


def get_repeatable_customers() -> List:
    """
    Gets customer's names from customers table which occurs more than 1 time
    :return:
        List of items (first name, appearance count)
    """
    query_sql = '''
        select c.FirstName, count(*) 
        from customers c 
        group by c.FirstName
        HAVING count(*) > 1
        order by c.FirstName;
    '''
    return execute_query(query_sql)
