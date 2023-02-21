from typing import Any, Text, Dict, List
from datetime import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import trino, random

##############################################

def flatten(list):
    return [item for sublist in list for item in sublist]

##############################################

# connect to trino
cur = trino.dbapi.connect(
    host = 'trino',
    port = 8080,
    user = 'user'
).cursor()

BURGERS = flatten(cur.execute(
    'SELECT name FROM mongodb.rah.burgers').fetchall()) 

##############################################

'''
Devuelve la hamburguesa del dia:
    Dada la fecha de hoy, por ejemplo, 19/01/2023
    se toma la fecha como entero 19012023 y se 
    calcula modulo cantidad_de_hamburguesas para 
    tener un indice con el que calcular una 
    hamburguesa por dia.
'''
class ActionBurgerDelDia(Action):
    
    def name(self) -> Text:
        return 'action_burger_dia'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        index = int(datetime.today().strftime('%d%m%Y')) % len(BURGERS)

        burger_dia = BURGERS[index]

        cur.execute(f"SELECT ingredients FROM mongodb.rah.burgers WHERE name='{burger_dia}'")
        ingredientes = flatten(cur.fetchall())[0]

        dispatcher.utter_message(
            text=f'La hamburguesa del día es... ¡una {burger_dia.lower()}!\n' +  
            f'Lleva {", ".join(ingredientes[:-1])} y {ingredientes[-1]}.'
        )
        return []

##############################################

'''
Devuelve las 3 hamburguesas mas baratas de la carta
'''
class ActionBurgersMasBaratas(Action):
    
    def name(self) -> Text:
        return 'action_burgers_baratas'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur.execute(f"SELECT name,price FROM mongodb.rah.burgers ORDER BY price LIMIT 3")
        baratas = cur.fetchall()

        msg = ''
        for [burger, price] in baratas:
            msg += f' - {burger.capitalize()} por {price:.2f} euros\n'

        dispatcher.utter_message(
            text=f'Las hamburguesas más baratas son:\n{msg}'
        )
        return []

##############################################

'''
Devuelve las 3 hamburguesas mas caras de la carta
'''
class ActionBurgersMasCaras(Action):
    
    def name(self) -> Text:
        return 'action_burgers_caras'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur.execute(f"SELECT name,price FROM mongodb.rah.burgers ORDER BY price DESC LIMIT 3")
        caras = cur.fetchall()

        msg = ''
        for [burger, price] in caras:
            msg += f' - {burger.capitalize()} por {price:.2f} euros\n'

        dispatcher.utter_message(
            text=f'Las hamburguesas más caras son:\n{msg}'
        )
        return []

##############################################

'''
Devuelve las hamburguesas con el ingrediente solicitado
'''
class ActionBurgersConIngrediente(Action):
    
    def name(self) -> Text:
        return 'action_burgers_con_ingrediente'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ingrediente = str(next(tracker.get_latest_entity_values('ingrediente'), None)).lower().strip()

        cur.execute(f"SELECT name,price FROM mongodb.rah.burgers WHERE CARDINALITY( FILTER (ingredients, i -> i LIKE '%{ingrediente}%')) > 0")
        burgers = cur.fetchall()
        n = len(burgers)
        MAX_TO_SHOW = 3

        res = f'Hay {n} hamburguesa{"" if n == 1 else "s"} con {ingrediente}'
        if n == 0:
            res = f'Me temo que no hay hamburguesas con ese ingrediente.'
        elif n > MAX_TO_SHOW:
            res += f', algunas de ellas son:\n'
            for [burger,price] in burgers[:MAX_TO_SHOW]:
                res += f' - La {burger.lower()} por {price:.2f} euros\n'
        else: 
            res += ':\n'
            for [burger,price] in burgers:
                res += f' - La {burger.lower()} por {price:.2f} euros\n'

        dispatcher.utter_message( text = res )
        return []

##############################################

'''
Devuelve los ingredientes de la hamburguesa solicitada
'''
class ActionIngredientesDeBurger(Action):
    
    def name(self) -> Text:
        return 'action_ingredientes_de_burger'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        burger = str(next(tracker.get_latest_entity_values('burger'), None)).upper().strip()

        if burger in BURGERS:

            cur.execute(f"SELECT ingredients FROM mongodb.rah.burgers WHERE name='{burger}'")
            ingredientes = flatten(cur.fetchall())[0]

            res = f'La {burger.lower()} lleva {", ".join(ingredientes[:-1])} y {ingredientes[-1]}.'

        else:
            res = 'Lo siento, no encuentro esa hamburguesa en la carta.'

        dispatcher.utter_message( text = res )
        return []

##############################################

'''
Almacena el pedido en la base de datos
'''
class ActionAlmacenarPedido(Action):
    
    def name(self) -> Text:
        return 'action_almacenar_pedido'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        frases = ['Pedido realizado: una {burger} para {nombre}', 'Pedido confirmado: ¡una {burger} para {nombre}!']

        err = "Lo siento, ha habido un error, empecemos de nuevo"

        burger = tracker.get_slot('burger')
        nombre = tracker.get_slot('nombre')

        if burger is None or nombre is None:
            dispatcher.utter_message( text = err )
        else:
            burger = str(tracker.get_slot('burger')).lower().strip()
            if burger.upper() in BURGERS:
                name = str(tracker.get_slot('nombre')).lower().strip()

                QUERY=f'''INSERT INTO mongodb.rah.pedidos (burger,name,time)
                    VALUES ('{burger}','{name}',current_timestamp)'''

                cur.execute(QUERY)
                dispatcher.utter_message( text = random.choice(frases).format(burger=burger.capitalize(), nombre=str(nombre).capitalize()) )
            else:
                dispatcher.utter_message( text = err )

        return [SlotSet('burger', None), SlotSet('nombre', None)] # reset slots

##############################################