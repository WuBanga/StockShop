from app import app, redis, es
from flask import request
from datetime import datetime

from dbs.postges import Postgres
from dbs.mongo import Mongo
from dbs.neo import Neo


@app.route('/postgres/add_stock/', methods=['POST'])
def postgres_add_stock():
    stocks = request.get_json()
    Postgres.add_stock(stocks['title'], stocks['address'])
    return '.'


@app.route('/postgres/add_goods/', methods=['POST'])
def postgres_add_goods():
    goods = request.get_json()
    Postgres.add_goods(goods['title'])
    return '.'


@app.route('/postgres/add_stock_state/', methods=['POST'])
def postgres_add_state_stock():
    state_stocks = request.get_json()
    Postgres.add_stock_state(state_stocks['address'], state_stocks['title'], state_stocks['quantity'])
    return '.'


@app.route('/redis/add/', methods=['POST'])
def redis_add():
    goodsTitles = request.get_json()
    redis.delete(goodsTitles['title'])
    
    address_id = Postgres.return_address_and_id(goodsTitles['title'])

    redis.hmset(goodsTitles['title'], address_id)
    return '.'


@app.route('/redis/get/', methods=['GET'])
def redis_get():
    requestTitle = request.get_json()
    k = requestTitle['title']
    return str(redis.hgetall(k))


@app.route('/orders/add_order/', methods=['POST'])
def add_order():
    orders = request.get_json()
    shopToStocks = Neo.get_all(orders['id_shop'])
    new_order = []

    shopToStocks.sort(key = lambda x: x[1])

    for goods in orders['goods']:
        redisdata = redis.hgetall(goods)
        
        if redisdata == {}:
            update_redis()
        
        all_stocks = {k: int(v) for k, v in redisdata.items()}
        for i in range(len(shopToStocks)):
            id_stock = shopToStocks[i][0]

            if id_stock in all_stocks.values():
                try:
                    cur_order = next(item for item in new_order if item['id_stock'] == id_stock)
                except StopIteration:
                    cur_order = {}

                cur_quantity = Postgres.return_quantity(id_stock, goods)

                new_quantity = cur_quantity[0] - orders['goods'][goods]

                if new_quantity >= 0:
                    if cur_order == {}:
                        cur_order.update({'id_shop' : orders['id_shop']})
                        cur_order.update({'id_stock' : id_stock})
                        cur_order.update({'goods': {}})
                        cur_order['goods'].update({goods: orders['goods'][goods]})

                        new_order.append(cur_order)
                    else:
                        new_order.remove(cur_order)
                        cur_order['goods'].update({goods: orders['goods'][goods]})

                        new_order.append(cur_order)
                    
                    if new_quantity == 0:
                        Postgres.delete_state_by_id(id_stock, goods)
                        redis.delete(goods)
                        address_id = Postgres.return_address_and_id(goods)
                        redis.hmset(goods, address_id)
                    else:
                        Postgres.update_quantity(goods, id_stock, new_quantity)

                    break
                else:
                    continue
    
    for order in new_order:
        id_order = Mongo.insert('orders', order, returned=True)
        body = {
            "date": f"{datetime.now():%Y-%m-%d}",
            "id_order": str(id_order)
        }
        es.index(index='orders', body=body)

    
    return '.'


@app.route('/shops/add/', methods=['POST'])
def add_shop():
    shops = request.get_json()
    Mongo.insert('shops', shops)
    return '.'


@app.route('/paths/add', methods=['POST'])
def add_path():
    paths = request.get_json()
    Mongo.insert('paths', paths)
    return '.'


@app.route('/delivery/add', methods=['GET'])
def add_delivery():
    paths = Mongo.return_collection('paths')
    Neo.delete_all()

    for doc in paths:
        id_stock = doc['id_stock']
        distance = doc['distance']
        id_shop = doc['id_shop']
        Neo.create_relation(id_stock, id_shop, distance)
    
    return '.'


@app.route('/postgres/delete_stock', methods=['DELETE'])
def delete_stock():
    stocks = request.get_json()
    Postgres.delete_stock(stocks['address'])
    return '.'


@app.route('/postgres/delete_goods', methods=['DELETE'])
def delete_goods():
    goods = request.get_json()
    Postgres.delete_goods(goods['title'])
    return '.'


@app.route('/postgres/delete_state', methods=['DELETE'])
def delete_state():
    states = request.get_json()
    Postgres.delete_state(states['address'], states['title'])
    return '.'


@app.route('/shops/delete', methods=['DELETE'])
def delete_shop():
    delete_shop = request.get_json()
    Mongo.delete('shops', delete_shop)
    
    return '.'


@app.route('/orders/get', methods=['GET'])
def get_order():
    results = []
    date = request.get_json() 
    res = es.search(index="orders", body={
        "query": {
            "term": {
                "date": f"{date['date']}"
            }
        }
    })

    for hit in res['hits']['hits']:
        result = {}
        src = hit['_source']
        order_date = src['date']
        order = Mongo.get_doc_by_id('orders', src['id_order'])
        
        for part in order:
            order_id_shop = part['id_shop']
            order_id_stock = part['id_stock']
            order_goods = part['goods']

        
        stock_info = Postgres.return_stock_info(order_id_stock)
        order_stock_title = stock_info[0]
        order_stock_address = stock_info[1]

        shop_info = Mongo.get_doc_by_part('shops', order_id_shop)

        for info in shop_info:
            order_shop_title = info['title']
            order_shop_address = info['address']
        

        result.update({'Дата заказа': order_date})
        result.update({'Название магазина': order_shop_title})
        result.update({'Адрес магазина': order_shop_address})
        result.update({'Название склада': order_stock_title})
        result.update({'Aдрес склада': order_stock_address})
        result.update({'Товары': {}})

        for goods in order_goods:
            result['Товары'].update({goods: order_goods[goods]})
        
        results.append(result)

    for i in results:
        print(i)
    
    return '.'


def update_redis():
    goods = Postgres.return_goods()
    for g in goods:
        address_id = Postgres.return_address_and_id(g[0])
        redis.hmset(g[0], address_id)
    