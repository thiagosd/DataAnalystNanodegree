__author__ = 'Thiago'
# !/usr/bin/env python
import pprint


def get_db(db_name):
    from pymongo import MongoClient

    client = MongoClient('localhost:27017')
    database = client[db_name]

    return database


if __name__ == '__main__':
    db = get_db('cities')


    # Top 10 appearing amenities
    print "Top 10 appearing amenities:"
    pprint.pprint(db.miami_florida.aggregate([{"$match": {"amenity": {"$exists": 1}}},
                                              {"$group": {"_id": "$amenity", "count": {"$sum": 1}}},
                                              {"$sort": {"count": -1}},
                                              {"$limit": 10}]))


      # Biggest religion (no surprise here)
    print "Biggest religion:"
    pprint.pprint(db.miami_florida.aggregate([
        {"$match": {"amenity": {"$exists": 1}, "amenity": "place_of_worship"}},
        {"$group": {"_id": "$religion", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}])['result'])



    print "Top 10 contributing users:"
    pprint.pprint(db.miami_florida.aggregate(
        [
            {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}, {"$limit": 10}
        ]))

    print "User with most recent post:", db.miami_florida.aggregate(
        [{"$project": {"timestamp": "$created.timestamp", "_id": "$created.user"}}, {"$sort": {"timestamp": -1}},
         {"$limit": 1}])['result']

    print "Cities with most entries:"
    pprint.pprint(
        db.miami_florida.aggregate(
            [
                {"$match": {"address.city": {"$exists": 1}}},
                {"$group": {"_id": "$address.city", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}, {"$limit": 10}
            ]))

    print "Number of contributing users who post less than 10 times:"
    pprint.pprint(
        db.miami_florida.aggregate(
        [
            {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
            {"$match": {"count": {"$lte": 10}}},
            {"$project": {"tmp": {"user": '$_id', "count": "$count"}}},
            {"$group": {"_id": "null", "total": {"$sum": 1}, "data": {"$addToSet": "$tmp"}}},
            {"$sort": {"count": -1}}
        ]))

    pprint.pprint(db.miami_florida.aggregate(
        [
            {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}, {"$limit": 10}
        ]))

    # Top 10 appearing amenities
    print "Top 10 appearing amenities:"
    pprint.pprint(
        db.miami_florida.aggregate(
            [{"$match": {"amenity": {"$exists": 1}}},
             {"$group": {"_id": "$amenity", "count": {"$sum": 1}}},
             {"$sort": {"count": -1}},
             {"$limit": 10}]
        )
    )

    # Number of bicycle_rental
    print "Number of bicycle rentals:", db.miami_florida.find({"amenity": "bicycle_rental"}).count()

    # Number of Publix
    print "Number of Publix:", db.miami_florida.find({"name": "Publix", "shop": "supermarket"}).count()

    # Number of computer shops
    print "Number of Computer shops:", db.miami_florida.find({"shop": "computer"}).count()


    print "Pharmacy with metadata :"
    pprint.pprint(
        db.miami_florida.aggregate([
            {'$match': {'amenity': 'pharmacy', 'name': {'$exists': 1}, 'opening_hours': '24/7'}},
            {'$project': {'_id': '$name', 'Street': '$addr:street', 'City': '$addr:city', 'Opening Hours': '$opening_hours'}}]
        ))


    # http://stackoverflow.com/questions/13529323/obtaining-group-result-with-group-count
