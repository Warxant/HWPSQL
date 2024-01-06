import time

import psycopg2
from pprint import pprint
     
#Удаление таблиц
def deletedb(cur):
      cur.execute("""DROP TABLE Clients, PhoneNumber CASCADE;
                  """)

# Функция, создающая структуру БД (таблицы)
def create_db(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS Clients(
                Id SERIAL PRIMARY KEY,
                Name VARCHAR(40),
                LastName VARCHAR(40),
                Email VARCHAR (40)
                );
                """)
    cur.execute("""CREATE TABLE IF NOT EXISTS PhoneNumber(
                client_id INTEGER REFERENCES Clients(id),
                Number varchar(11) PRIMARY KEY
                );
                """)
    
### Функция, позволяющая добавить нового клиента    
def new_client(cur, name, last_name, email, phones=None):
    cur.execute("""INSERT INTO Clients(name, lastname, email)
                    VALUES (%s, %s, %s)
                     RETURNING id, name, lastname;""",
                    (name, last_name, email))
        
    client = cur.fetchone()

    if phones is not None:
            cur.execute("""INSERT INTO PhoneNumber(client_id, number)
                        VALUES(%s, %s);
                        """,(client[0], phones))
    return 

### Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(cur, client_id, phone):
    cur.execute("""INSERT INTO PhoneNumber(client_id, number)
                    VALUES (%s, %s);
                """,(client_id, phone))
    return
   
### Функция, позволяющая изменить данные о клиенте.
def change_client(cur, client_id, name=None, lastname=None, email=None, phones=None):
    if name is not None:
            cur.execute("""UPDATE Clients SET name=%s WHERE id=%s
                        """, (name, client_id))
    if lastname is not None:
            cur.execute("""UPDATE Clients SET lastname=%s WHERE id=%s
                        """, (lastname, client_id))
    if email is not None:
            cur.execute("""UPDATE Clients SET email=%s WHERE id=%s
                        """, (email, client_id))
    if phones is not None:
            new_client(cur, client_id, phones)
        
### Функция, позволяющая удалить телефон для существующего клиента            
def delete_phone(cur, client_id, phones):
    cur.execute("""DELETE FROM PhoneNumber
                    WHERE client_id=%s and number=%s
                    """, (client_id, phones)) 
              
#  Функция, позволяющая удалить существующего клиента       
def delete_client(cur, client_id):
    cur.execute("""DELETE FROM PhoneNumber
                    WHERE PhoneNumber.client_id=%s
                    """, (client_id))
    cur.execute("""DELETE FROM Clients
                    WHERE id=%s"""
                    , (client_id))
        
    return
        
# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)  
def find_client(cur, name=None, lastname=None, email=None, phone=None):
    cur.execute("""SELECT cl.id, cl.name, cl.lastname, cl.email, pn.number FROM clients cl
                left join phonenumber pn
                ON pn.client_id = cl.id
                 WHERE  pn.client_id = cl.id 
                 AND cl.name=%s OR cl.lastname=%s OR cl.email=%s OR pn.number=%s;                
                 """, (name,lastname,email,phone))
    
    fc = cur.fetchall()
    for i in fc:
        for s in i:
            print(f'{s}', end=' ')
    print()
    return

#def find_client(cur, name=None, lastname=None, email=None, phone=None):
    if phone is not None:
        cur.execute("""SELECT cl.id, cl.name, cl.lastname, cl.email, pn.number FROM clients cl
                left join phonenumber pn
                ON pn.client_id = cl.id
                 WHERE  pn.client_id = cl.id 
                 AND cl.name=%s OR cl.lastname=%s OR cl.email=%s OR pn.number=%s;                
                 """, (name,lastname,email,phone))
    
        fc = cur.fetchall()
        for i in fc:
            for s in i:
                print(f'{s}', end=' ')
    else:
        cur.execute("""SELECT cl.id, cl.name, cl.lastname, cl.email FROM clients cl
            WHERE cl.name=%s OR cl.lastname=%s OR cl.email=%s;
            """, (name, lastname, email))
        fc = cur.fetchall()
        for i in fc:
            for s in i:
                print(f'{s}', end=' ')

    print()
    return
     
conn = psycopg2.connect(database = 'ClientBD', user = 'postgres', password = 'psql')

with conn.cursor() as cur:
    deletedb(cur)

    # create_db(cur)

    # new_client(cur, 'Андрей', 'Иванов', 'ivanovA@gmail.com', '89763456177')
    # new_client(cur, 'Ксения', 'Семёнова', 'KSemyonova@gmail.com', '89606961545')
    # print('Добавили 2-ух новых клиентов:')
    # find_client(cur, 'Андрей')
    # find_client(cur, None, 'Семёнова', None, '89606961545')
#-----------------------------------------------------------------------
    # delete_phone(cur, '1', '89763456177')
    # delete_phone(cur, '2', '89606961545')
    # print('Удаление номера телефона')
    # find_client(cur, 'Андрей', 'Иванов')
    # find_client(cur, 'Ксения', 'Семёнова')
#-----------------------------------------------------------------------
    # add_phone(cur, '1', '89374038976')
    # add_phone(cur, '2', '89453231766')
    # print('Добавление номера телефона')
    # find_client(cur, 'Андрей', 'Иванов')
    # find_client(cur, 'Ксения', 'Семёнова')
#-----------------------------------------------------------------------
    # change_client(cur, '1', None, None, 'AndreyIvanov@bk.ru')  
    # change_client(cur, '2', None, 'Алексеева')
    # print('Изменение данных клиента')
    # find_client(cur, 'Андрей')
    # find_client(cur, 'Ксения')
#------------------------------------------------------------------------
    # delete_client(cur, '1')
    # find_client(cur, 'Андрей')
    # find_client(cur, 'Ксения')

    











    conn.commit()
conn.close() 