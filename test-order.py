import trino

# connect to trino
conn = trino.dbapi.connect(
    host = 'localhost',
    port = 8080,
    user = 'user'
)

BURGERS = ['baby', 'chickencrispy', 'supercheese', 'muralla', 
'supreme', 'reina', 'jalapeña', 'africana', 'pull pork', 
'vegana gourmet', 'crispyvegana', 'cheesebacon', 'donuts burger', 
'country', 'lotus', 'heavy', 'mexican', 'american burger']

burger = input('>>> burger? >>> ').lower().strip()
assert burger in BURGERS
name = input('>>> a nombre de? >>> ').strip()

QUERY=f'''INSERT INTO mongodb.rah.pedidos (burger,name,time)
VALUES ('{burger}','{name}',current_timestamp)'''

cur = conn.cursor()
cur.execute(QUERY)

print('hecho!')