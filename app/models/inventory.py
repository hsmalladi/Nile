import os
from flask import current_app as app
from werkzeug.utils import secure_filename


class Inventory:
    def __init__(self, sid, pid, image, category, name, quantity, unit_price, description):
        self.sid = sid
        self.pid = pid
        self.image = image
        self.category = category
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price
        self.description = description

    # given id of seller, return list of products in their inventory (and associated info)
    @staticmethod
    def get_by_sid(sid):
        rows = app.db.execute('''
select sid, pid, image, category, name, quantity, unit_price, description
from Inventory join Products
    on Inventory.pid = Products.id
where sid = :sid
''',
                              sid=sid)
        return [Inventory(*row) for row in rows]

    # given seller id and pid, return details on 1 product
    @staticmethod
    def get_by_sid_and_pid(sid, pid):
        rows = app.db.execute('''
select sid, pid, image, category, name, quantity, unit_price, description
from Inventory join Products
    on Inventory.pid = Products.id
where sid = :sid and pid = :pid
''',
                              sid=sid,
                              pid=pid)
        return Inventory(*(rows[0])) if rows is not None else None

    # PRIVATE HELPER METHOD
    # given product image, category, name, unit_price, description
    # insert into Products table
    # and return id
    @staticmethod
    def insert_new_product(image, category, name, unit_price, description):
        try:
            rows = app.db.execute("""
INSERT INTO Products(image, category, name, unit_price, description)
VALUES(:image, :category, :name, :unit_price, :description)
RETURNING id;
""",
                                  image=image,
                                  category=category,
                                  name=name,
                                  unit_price=unit_price,
                                  description=description)
            
            pid = rows[0][0]
            return pid

        except Exception as e:
            print(str(e))
            return None

    # PRIVATE HELPER METHOD
    # given id,
    # insert this person into the Sellers table
    @staticmethod
    def insert_new_seller(sid):
        try:
            rows = app.db.execute("""
INSERT INTO Sellers(id)
VALUES(:id)
RETURNING id;
""",
                                  id=sid)
            
            sid = rows[0][0]
            return sid

        except Exception as e:
            print(str(e))
            return None


    # given seller id AND product image, category, name, quantity, unit_price, description
    # insert into Products table
    # insert into Sellers table
    # insert into Inventory table
    @staticmethod
    def add_new_inventory_item(sid, image, category, name, quantity, unit_price, description):
        # insert into Products
        pid = Inventory.insert_new_product(image.read(), category, name, unit_price, description)

        if not pid:
            return None

        # insert into Sellers (in case this person is not yet a seller)
        Inventory.insert_new_seller(sid)
            
        # then connect this product into Inventory
        try:
            rows = app.db.execute("""
INSERT INTO Inventory(sid, pid, quantity)
VALUES(:sid, :pid, :quantity)
RETURNING sid, pid;
""",
                                sid=sid,
                                pid=pid,
                                quantity=quantity)
            pid = rows[0][1]
            return pid

        except Exception as e:
            print(str(e))
            return None


    # given sid and pid, edit product quantity
    @staticmethod
    def edit_inventory_item(sid, pid, quantity):
        rows = app.db.execute('''
update Inventory
set quantity = :quantity
where sid = :sid and pid = :pid;
''',
                              sid=sid,
                              pid=pid,
                              quantity=quantity)



    # PRIVATE HELPER METHOD 
    # given product id, delete product from Products
    @staticmethod
    def delete_product(pid):
        rows = app.db.execute('''
delete from Products
where id = :pid;
''',
                              pid=pid)

    # PRIVATE HELPER METHOD 
    # given seller id, delete person from Sellers
    @staticmethod
    def delete_seller(sid):
        rows = app.db.execute('''
delete from Sellers
where id = :sid;
''',
                              sid=sid)                     

    # given sid and pid, delete product from inventory
    @staticmethod
    def delete_inventory_item(sid, pid):
        # Delete product from Inventory
        rows = app.db.execute('''
delete from Inventory
where sid = :sid and pid = :pid;
''',
                              sid=sid,
                              pid=pid)

        # Then delete product from Products
        Inventory.delete_product(pid)
        
        # If this seller is now no longer selling ANY products, delete them from Sellers
        if (len(Inventory.get_by_sid(sid)) == 0):
            Inventory.delete_seller(sid)
