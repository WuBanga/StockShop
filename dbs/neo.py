from app import neo


class Neo:

    @staticmethod
    def delete_all():
        with neo.session() as session:
            session.run(
                "match (n) detach delete n"
            )


    @staticmethod
    def create_relation(id_stock, id_shop, distance):
        with neo.session() as session:
            session.run(
                "merge (a:Stock { id : $id_stock})"
                "merge (b:Shop { id : $id_shop})"
                "merge (a)-[c:Deliver { distance : $distance}]->(b)", id_stock=id_stock, id_shop=id_shop, distance=distance
            )


    @staticmethod
    def get_all(id_shop):
        with neo.session() as session:
            result = session.run(
                "match (a:Stock)-[c:Deliver]->(b:Shop { id : $id_shop})"
                "return a.id, c.distance ", id_shop=id_shop
            )
        return result.values()