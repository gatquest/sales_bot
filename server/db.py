from datetime import datetime
import sqlite3
from config import DATABASE_NAME
from serialize import ReplyGetOrder, CreateOrder




    
def db_get_order(order_number: int) -> ReplyGetOrder:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE order_number = ?', (order_number,))
        item = cursor.fetchone()
        return item


def db_create_order(data: CreateOrder):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        if data.to_russia:
            cursor.execute('SELECT MAX(order_number) FROM orders')
            last_order_number = cursor.fetchone()[0]
        else:
            cursor.execute('SELECT MAX(order_number) FROM orders WHERE order_number < 2000')
            last_order_number = cursor.fetchone()[0]

        new_order_number = last_order_number + 1

        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''INSERT INTO orders (order_number, client_name, order_date) 
                       VALUES (?, ?, ?)''', 
                       (new_order_number, 
                       data.client_name, 
                       order_date))
        conn.commit()
        return new_order_number
    

async def db_put_image_to_order(order_number: int, image_path: str):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE orders SET image_path = ? WHERE order_number = ?', (image_path, order_number))
        conn.commit()
        return True
