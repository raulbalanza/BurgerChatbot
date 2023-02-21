db = db.getSiblingDB('rah');

db.createCollection('pedidos');

db.createCollection('_schema');
db.getCollection("_schema").insertOne({
    "table": "pedidos",
    "fields": [
        {
        "name": "_id",
        "type": "ObjectId",
        "hidden": true,
        "comment": null
        },
        {
        "name": "burger",
        "type": "varchar",
        "hidden": false,
        "comment": null
        },
        {
        "name": "name",
        "type": "varchar",
        "hidden": false,
        "comment": null
        },
        {
        "name": "time",
        "type": "timestamp(3)",
        "hidden": false,
        "comment": null
        }
    ]
});

db.createCollection('burgers');
db.burgers.insertMany([
    {
        "name": "BABY",
        "price": 6.5,
        "ingredients": [
            "120g de ternera",
            "queso gouda"
        ]
    },
    {
        "name": "CHICKENCRISPY",
        "price": 10.25,
        "ingredients": [
            "130g de pollo rebozado",
            "huevo",
            "bacon",
            "queso gouda",
            "salsa deluxe"
        ]
    },
    {
        "name": "SUPERCHEESE",
        "price": 11.2,
        "ingredients": [
            "200g de ternera",
            "queso cheddar",
            "queso gouda",
            "queso brie",
            "queso de cabra",
            "salsa roquefort"
        ]
    },
    {
        "name": "MURALLA",
        "price": 11.2,
        "ingredients": [
            "200g de ternera",
            "lechuga",
            "bacon",
            "queso gouda",
            "huevo",
            "mayonesa"
        ]
    },
    {
        "name": "SUPREME",
        "price": 15.1,
        "ingredients": [
            "200g de angus",
            "canónigo",
            "rúcula",
            "queso brie",
            "cebolla confitada",
            "foie"
        ]
    },
    {
        "name": "REINA",
        "price": 12.95,
        "ingredients": [
            "200g de ternera",
            "foie",
            "canónigo",
            "cebolla caramelizada",
            "sal laminada"
        ]
    },
    {
        "name": "JALAPEÑA",
        "price": 11.9,
        "ingredients": [
            "200g de ternera",
            "queso cheddar",
            "cebolla caramelizada",
            "crema de cheddar",
            "guacamole",
            "jalapeños"
        ]
    },
    {
        "name": "AFRICANA",
        "price": 11.95,
        "ingredients": [
            "200g de angus",
            "queso de cabra",
            "lechuga",
            "bacon",
            "cebolla caramelizada"
        ]
    },
    {
        "name": "PULL PORK",
        "price": 13.6,
        "ingredients": [
            "200g de angus",
            "cebolla caramelizada",
            "bacon",
            "pull pork",
            "salsa bbq",
            "queso cheddar"
        ]
    },
    {
        "name": "VEGANA GOURMET",
        "price": 12.9,
        "ingredients": [
            "pan de romero",
            "150g de hamburguesa beyond",
            "hummus",
            "brotes",
            "escalivada",
            "tomate",
            "queso vegano"
        ]
    },
    {
        "name": "CRISPYVEGANA",
        "price": 12.9,
        "ingredients": [
            "pechuga de corn flakes vegana",
            "brotes",
            "queso vegano",
            "tomate",
            "pepinillos",
            "salsa vegana"
        ]
    },
    {
        "name": "CHEESEBACON",
        "price": 9.3,
        "ingredients": [
            "120g de ternera",
            "crema de cheddar",
            "bacon",
            "queso gouda",
            "queso cheddar"
        ]
    },
    {
        "name": "DONUTS BURGER",
        "price": 13.5,
        "ingredients": [
            "donuts glaseado",
            "120g de ternera",
            "queso cheddar",
            "cebolla caramelizada",
            "bacon",
            "huevo",
            "salsa burger"
        ]
    },
    {
        "name": "COUNTRY",
        "price": 14.2,
        "ingredients": [
            "200g de hamburguesa de angus",
            "cebolla caramelizada",
            "queso gouda",
            "queso cheddar",
            "confitura de bacon",
            "bacon",
            "costillar baja temperatura",
            "salsa bourbon"
        ]
    },
    {
        "name": "LOTUS",
        "price": 13.95,
        "ingredients": [
            "2x 120g de ternera",
            "queso gouda",
            "queso cheddar",
            "bacon",
            "patatas paja",
            "tierra de lotus",
            "galleta lotus"
        ]
    },
    {
        "name": "HEAVY",
        "price": 13.95,
        "ingredients": [
            "3x 120g de ternera",
            "bacon",
            "lechuga",
            "queso gouda",
            "huevo",
            "carne mechada",
            "cebolla",
            "salsa bbq"
        ]
    },
    {
        "name": "MEXICAN",
        "price": 13.95,
        "ingredients": [
            "200g de ternera",
            "queso cheddar",
            "guacamole",
            "crema de cheddar",
            "mix de frijoles",
            "jalapeños",
            "jeringuilla extra picante"
        ]
    },
    {
        "name": "AMERICAN BURGER",
        "price": 14.95,
        "ingredients": [
            "320g de vaca",
            "rúcula",
            "canónigo",
            "queso cheddar",
            "cebolla confitada",
            "pepinillos",
            "salsa chili dulce",
            "bacon",
            "salsa burger"
        ]
    }
]);