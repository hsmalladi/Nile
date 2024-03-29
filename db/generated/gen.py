from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import datetime

# this file is used for generating the data for the database

# the number of each category we want in our tables
# only need to change these numbers and can rerun with all the data
# we want
num_users = 100
num_products = 2000
num_purchases = 2500
inventory = 2000
cart=2000
reviews=5000
order=4000


Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

# generate the users
def gen_users():
    users = set()
    with open('./db/data/Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            # their information
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name = profile['name']
            address = fake.address()
            balance = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            users.add(uid)
            # write to file
            writer.writerow([uid, name, email, balance, address, password])
        print(f'{num_users} generated')
    return users

# generate the products
def gen_products():
    products = set()
    with open('./db/data/Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            products.add(pid)
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            # create the information for the table
            name = fake.sentence(nb_words=4)[:-1]
            image = 0
            category = fake.random_element(elements=("Clothing & Accessories", "Books", "Electronics", 
                                                "Home Goods", "Food & Grocery", "Beauty & Health", "Toys",
                                                "Pet Supplies", "Sports & Outdoors", "Automotive"))
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            description = fake.sentence(nb_words=10)[:-1]
            # write to the file
            writer.writerow([pid, name, category, image, price, description])
        print(f'{num_products} generated;')
    return products

# generate the random seller ids
def gen_sellers():
    sellers = set()
    with open("./db/data/Sellers.csv", "w") as f:
        writer = get_csv_writer(f)
        print('Seller...', end=' ', flush=True)
        for id in range(100):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            # guaranteeing a seller is also a user
            sid = fake.random_int(max=num_users-1)
            while sid in sellers:
                sid = fake.random_int(max=num_users-1)
            sellers.add(sid)
            # write to the csv
            writer.writerow([sid])
    return sellers

# getting inventory products
def gen_inventory(sellers, products):
    with open('./db/data/Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        used_keys = set()
        print('Inventory...', end=' ', flush=True)
        # making every product avaliable for now
        for pid in range(inventory):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            sid = fake.random_element(elements=list(sellers))
            used_keys.add(pid)
            # print(sid, pid)
            quantity = fake.random_int(min=1,max=30)
            writer.writerow([sid, pid, quantity])
        print(f'{inventory} generated')
    return

# creating the items in others carts
def gen_cart(users, products, sellers):
    combos = set()
    with open('./db/data/Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for id in range(cart):
            # Guaranteeing we have unqiue uid, pid combos and these numbers come from exisiting numbers
            uid = fake.random_element(elements=list(users))
            pid = fake.random_element(elements=list(products))
            while (uid, pid) in combos:
                uid = fake.random_element(elements=list(users))
                pid = fake.random_element(elements=list(products))
            sid = fake.random_element(elements=list(sellers))
            combos.add((uid, pid))
            quantity = fake.random_int(max=20)
            # write to the csv
            writer.writerow([uid, pid, sid, quantity])

# method to generate both product and seller reviews
def gen_rates(filename, people, users):
    combo = set()
    with open(filename, 'w') as f:
        writer = get_csv_writer(f)
        print(filename, end=' ', flush=True)
        for num in range(reviews):
            # ensuring the fid and uid combos are unqiue based on database design
            fid = fake.random_element(elements=people)
            uid = fake.random_element(elements=users)
            while (fid, uid) in combo:
                fid = fake.random_element(elements=people)
                uid = fake.random_element(elements=users)
            # generating rating info 
            date = fake.date_time_this_month().strftime("%Y-%m-%d %H:%M:%S")
            rating = fake.random_int(min=1, max=5)
            review = fake.sentence(nb_words=40)[:-1]
            # writing to file
            writer.writerow([uid, fid, rating, review, date])

# generating the orders
def gen_orders(users):
    orders = set()
    with open("./db/data/Orders.csv", 'w') as f:
        writer = get_csv_writer(f)
        print("Orders...", end=' ', flush=True)
        # making sure oid is unqiue
        for oid in range(order):
            orders.add(oid)
            # Update sid to select from sellers
            uid = fake.random_element(elements=users)
            date_ordered = fake.date_time_this_month().strftime("%Y-%m-%d %H:%M:%S")
            fufilled = fake.random_element(elements=('true', 'false'))
            
            writer.writerow([oid, uid, date_ordered, fufilled])
    return orders

# generating the purchases
def gen_purchases(orders, users, products):
    with open('./db/data/Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        oiddict = {}
        # confirming some purchases belong in the same order
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            
            # if the user already was involved in another purchase in this order, add accordingly
            oid = fake.random_element(elements=list(orders))
            if oid in oiddict:
                uid = oiddict[oid]
            else:
                uid = fake.random_element(elements=list(users))
                oiddict[oid] = uid
            # more purchase information
            pid = fake.random_element(elements=list(products))
            quantity = fake.random_int(min=0, max = 20)
            time_purchased = fake.date_time_this_month().strftime("%Y-%m-%d %H:%M:%S")
            unit_price_at_time_of_payment = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            fufilled = fake.random_element(elements=('true', 'false'))
            writer.writerow([id, oid, uid, pid, quantity, time_purchased, unit_price_at_time_of_payment, fufilled])
        print(f'{num_purchases} generated')



# run all the generation scripts
users = gen_users()
products = gen_products()
sellers = gen_sellers()
gen_inventory(sellers, products)
gen_rates("./db/data/RatesSeller.csv", sellers, users)
gen_rates("./db/data/RatesProduct.csv", products, users)
orders = gen_orders(users)
gen_purchases(orders, users, products)
gen_cart(users, products, sellers)

