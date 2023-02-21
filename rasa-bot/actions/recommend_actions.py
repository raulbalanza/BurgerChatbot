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
Recomienda una hamburguesa obteniendo sus ingredientes de la base de datos
'''
class ActionRecomiendaHamburguesa():
    
    def name(self) -> Text:
        return 'action_recomienda_' + self.hamburguesa.replace(" ", "_")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        frases = ["En ese caso lo tengo claro", "Genial, entonces es fácil", "Entonces no te puedes perder esta", "Entonces te recomiendo"]
        
        assert self.hamburguesa.upper() in BURGERS # ojo el assert debe ser en upper

        if self.hamburguesa.upper() == "MURALLA":
            especial = "la hamburguesa especial de la casa, "
        else: especial = ""

        cur.execute(f"SELECT ingredients FROM mongodb.rah.burgers WHERE name='{self.hamburguesa.upper()}'")
        ingredientes = flatten(cur.fetchall())[0]

        res = f'{random.choice(frases)}: {especial}¡una {self.hamburguesa.capitalize()}! Lleva {", ".join(ingredientes[:-1])} y {ingredientes[-1]}.'

        dispatcher.utter_message( text = res )
        return [SlotSet('burger', self.hamburguesa.lower()), SlotSet('nombre', None)] # set slots

##############################################

class ActionRecomiendaVegana(ActionRecomiendaHamburguesa, Action):
    
    def __init__(self):
        self.hamburguesa = "crispyvegana"
        
class ActionRecomiendaLotus(ActionRecomiendaHamburguesa, Action):
    
    def __init__(self):
        self.hamburguesa = "lotus"
        
class ActionRecomiendaDonuts(ActionRecomiendaHamburguesa, Action):
    
    def __init__(self):
        self.hamburguesa = "donuts burger"
        
class ActionRecomiendaMuralla(ActionRecomiendaHamburguesa, Action):
    
    def __init__(self):
        self.hamburguesa = "muralla"