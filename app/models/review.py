from flask import current_app as app

class Review:

    def __init__(self, uid, pid, rating, review, date):
        self.pid = pid
        self.uid = uid
        self.date = date
        self.rating = rating
        self.review = review

 #*  @staticmethod
 #   def get(uid):
 #       rows = app.db.execute('''
#SELECT uid, pid, review_time, review_content
#FROM RatesProduct
# WHERE id = :id
# ''',
  #                            id=id)
 #       return Review(*(rows[0])) if rows else None

 # Check if the user has purchased the product
    @staticmethod
    def user_purchased_product(uid, pid):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE uid = :uid
AND pid = :pid
''',
                              uid = uid, 
                              pid = pid)
    # if the user has bought the product at least once
        if len(rows) > 0:
            return True


    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT uid, pid, review_time, review_content
FROM RatesProduct
WHERE uid = :uid
AND review_time >= :since
ORDER BY review_time DESC
''',
                              uid=uid,
                              since=since)
        return [Review(*row) for row in rows]

#get specific product review from uid and pid
    @staticmethod
    def get_product_review(uid, pid):
        rows = app.db.execute('''
SELECT *
FROM RatesProduct 
WHERE uid = :uid
AND pid = :pid
''',
                              uid=uid,
                              pid = pid)
        return Review(*(rows[0])) if rows is not None else None


    @staticmethod
    def get_recent_reviews(uid):
        rows = app.db.execute('''
SELECT *
FROM RatesProduct 
WHERE uid = :uid
ORDER BY date DESC
LIMIT 5
''',
                              uid = uid)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_product_review(uid, pid):
        rows = app.db.execute('''
SELECT *
FROM RatesProduct 
WHERE uid = :uid
AND pid = :pid
ORDER BY date DESC
''',
                              uid = uid, 
                              pid = pid)
        return Review(*(rows[0])) if rows is not None else None


    @staticmethod
    def get_all_product_reviews(uid):
        rows = app.db.execute('''
SELECT *
FROM RatesProduct 
WHERE uid = :uid
ORDER BY date DESC
''',
                              uid = uid)
        return [Review(*row) for row in rows]


#add product review to db
    @staticmethod
    def add_new_product_review(uid, pid, date, rating, review):
            
        # then add this product into RatesProduct
        try:
            rows = app.db.execute("""
INSERT INTO RatesProduct(uid, pid, rating, review, date)
VALUES(:uid, :pid, :rating, :review, :date)
""",
                                uid = uid, 
                                pid = pid, 
                                date = date, 
                                rating = rating, 
                                review = review)
            
            pid = rows[0][1]
            return pid

        except Exception as e:
            print(str(e))
            return None

# given uid and pid, delete review from RatesProduct
    @staticmethod
    def delete_product_review(uid, pid):
        # Delete review
        rows = app.db.execute('''
delete from RatesProduct
where uid = :uid and pid = :pid;
''',
                              uid=uid,
                              pid=pid)

# check if there is already a product review
    @staticmethod
    def has_product_review(uid, pid):
        rows = app.db.execute('''
SELECT *
FROM RatesProduct 
WHERE uid = :uid
AND pid = :pid
''',
                              uid = uid, 
                              pid = pid)
    # if there is already a product review from this user
        if len(rows) > 0:
            return True


class Seller_Review:

    def __init__(self, uid, sid, rating, review, date):
        self.sid = sid
        self.uid = uid
        self.date = date
        self.rating= rating
        self.review = review

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT uid, sid, review_time, review_content
FROM RatesProduct
WHERE uid = :uid
AND review_time >= :since
ORDER BY review_time DESC
''',
                              uid=uid,
                              since=since)
        return [Seller_Review(*row) for row in rows]


    @staticmethod
    def get_seller_reviews(uid):
        rows = app.db.execute('''
SELECT *
FROM RatesSeller
WHERE uid = :uid
ORDER BY date DESC
LIMIT 5
''',
                              uid=uid)
        return [Seller_Review(*row) for row in rows]

    @staticmethod
    def get_seller_review(uid, sid):
        rows = app.db.execute('''
SELECT *
FROM RatesSeller
WHERE uid = :uid
AND sid = :sid
''',
                              uid = uid, 
                              sid = sid)
        return Seller_Review(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all_seller_reviews(uid):
        rows = app.db.execute('''
SELECT *
FROM RatesSeller
WHERE uid = :uid
ORDER BY date DESC
''',
                              uid=uid)
        return [Seller_Review(*row) for row in rows]

#add product review to db
    @staticmethod
    def add_new_seller_review(uid, sid, date, rating, review):
            
        # then add this product into RatesProduct
        try:
            rows = app.db.execute("""
INSERT INTO RatesSeller(uid, sid, rating, review, date)
VALUES(:uid, :sid, :rating, :review, :date)
""",
                                uid = uid, 
                                sid = sid, 
                                date = date, 
                                rating = rating, 
                                review = review)
            
            sid = rows[0][1]
            return sid

        except Exception as e:
            print(str(e))
            return None

# given uid and pid, delete review from Rates
    @staticmethod
    def delete_seller_review(uid, sid):
        # Delete review
        rows = app.db.execute('''
delete from RatesSeller
where uid = :uid and sid = :sid;
''',
                              uid=uid,
                              sid=sid)

# check if there is already a product review
    @staticmethod
    def has_seller_review(uid, sid):
        rows = app.db.execute('''
SELECT *
FROM RatesSeller
WHERE uid = :uid
AND sid = :sid
''',
                              uid = uid, 
                              sid = sid)
    # if there is already a product review from this user
        if len(rows) > 0:
            return True


 # Check if the user has purchased from the seller
    @staticmethod
    def user_purchased_seller(uid, sid):
        rows = app.db.execute('''
SELECT *
FROM Purchases, Inventory
WHERE Purchases.uid = :uid
AND Purchases.pid = Inventory.pid
AND Inventory.sid = :sid
''',
                              uid = uid, 
                              sid = sid)
    # if the user has bought the product at least once
        if len(rows) > 0:
            return True


    








