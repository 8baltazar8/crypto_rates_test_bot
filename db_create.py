import sqlite3


def create_db():
    print("FEWPOWJEFJOWEJF")
    with sqlite3.connect('user_info.db') as conn:
        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS users \
                    (id integer primary key autoincrement, \
                    tg_id varchar(50), username varchar(50), \
                    name varchar(50), surname varchar(50),
                    phone_number varchar(20),
                    isdeleted integer DEFAULT 0 NOT NULL)""")

        conn.commit()
