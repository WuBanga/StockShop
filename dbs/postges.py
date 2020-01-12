from app import postgresConnect


class Postgres:

    @staticmethod
    def add_stock(title, address):
        add = postgresConnect.cursor()
        add.execute(
            f"select add_stock('{title}', '{address}')"
        )
        add.close()
        postgresConnect.commit()


    @staticmethod
    def add_goods(title):
        add = postgresConnect.cursor()
        add.execute(
            f"select add_goods('{title}')"
        )
        add.close()
        postgresConnect.commit()


    @staticmethod
    def add_stock_state(address, title, quantity):
        add = postgresConnect.cursor()
        add.execute(
            f"select add_stock_state('{address}', '{title}', {quantity})"
        )
        add.close()
        postgresConnect.commit()


    @staticmethod
    def return_address_and_id(title):
        returnCur = postgresConnect.cursor()
        returnCur.execute(
            f"select * from return_address_id_stock('{title}')"
        )
        address_id = dict(returnCur.fetchall())
        return address_id


    @staticmethod
    def return_quantity(id_stock, goods):
        returnCur = postgresConnect.cursor()
        returnCur.execute(
            f"select * from return_quantity({id_stock}, '{goods}')"
        )
        quantity = returnCur.fetchone()
        returnCur.close()
        return quantity


    @staticmethod
    def update_quantity(goods, id_stock, quantity):
        updateCur = postgresConnect.cursor()
        updateCur.execute(
            f"select update_quantity('{goods}', {id_stock}, {quantity})"
        )
        updateCur.close()
        postgresConnect.commit()


    @staticmethod
    def delete_stock(address):
        delCur = postgresConnect.cursor()
        delCur.execute(
            f"select delete_stock('{address}')"
        )
        delCur.close()
        postgresConnect.commit()


    @staticmethod
    def delete_goods(title):
        delCur = postgresConnect.cursor()
        delCur.execute(
            f"select delete_goods('{title}')"
        )
        delCur.close()
        postgresConnect.commit()


    @staticmethod
    def delete_state(address, title):
        delCur = postgresConnect.cursor()
        delCur.execute(
            f"select delete_state('{address}', '{title}')"
        )
        delCur.close()
        postgresConnect.commit()

    
    @staticmethod
    def delete_state_by_id(id_stock, goods):
        delCur = postgresConnect.cursor()
        delCur.execute(
            f"select delete_state_by_id({id_stock}, '{goods}')"
        )
        delCur.close()
        postgresConnect.commit()


    @staticmethod
    def return_stock_info(id_stock):
        returnCur = postgresConnect.cursor()
        returnCur.execute(
            f"select title, address from stock where id={id_stock}"
        )
        info = returnCur.fetchone()
        returnCur.close()
        return info


    @staticmethod
    def return_goods():
        returnCur = postgresConnect.cursor()
        returnCur.execute(
            f"select title from goods"
        )
        all_goods = returnCur.fetchall()
        returnCur.close()
        return all_goods