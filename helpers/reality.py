class Reality:
    # TODO: use __slots__ for attributes
    class History:
        price:int = 0
        history_date = ""
        description = ""
        vievewd_count:int = 0

        def __init__(self, price=0, history_date="", description="", viewed_count=0):
            self.price = price
            self.history_date = history_date
            self.description = description
            self.viewed_count = viewed_count

    id = ""
    provider = ""
    title = ""
    price = ""
    url = ""
    publish_date = ""
    location = ""
    description = ""
    image = ""
    advertiser_name = ""
    viewed_count = ""
    history:list = list()


    def __init__(self, id, title, price, url, publish_date, location, description, advertiser_name, image, viewed_count):
        self.id = id
        self.title = title
        self.price = price
        self.url = url
        self.publish_date = publish_date
        self.location = location
        self.description = description
        self.advertiser_name = advertiser_name
        self.image = image
        self.viewed_count = viewed_count

    def set_provider(self, provider):
        self.provider = provider

    def __str__(self):
        return "Id: {}\n Title: {}\n Price: {}\n PublishDate: {}\n Location: {}\n Description: {}\n url: {}\n Advertiser: {}\n ViewedCount: {}".format(
            self.id, self.title, self.price, self.publish_date, self.location, self.description, self.url, self.advertiser_name, self.viewed_count
        )
    def toString(self):
        return "Id: {}\n Title: {}\n Price: {}\n PublishDate: {}\n Location: {}\n Description: {}\n url: {}\n Advertiser: {}\n ViewedCount: {}".format(
            self.id, self.title, self.price, self.publish_date, self.location, self.description, self.url, self.advertiser_name, self.viewed_count
        )

    def set_history(self, history):
        self.history = history

def parse_single_from_db(db_reality):
    return Reality(
        db_reality['id'],
        db_reality['title'],
        db_reality['price'],
        db_reality['url'],
        db_reality['date'],
        db_reality['location'],
        db_reality['description'],
        db_reality['advertiser_name'],
        db_reality['image'],
        db_reality['viewed_count'],
    )

def parse_many_from_db(db_reality_list):
    reality_list = []
    for db_reality in db_reality_list:
        reality_list.append(parse_single_from_db(db_reality))
    return reality_list


def parse_history_from_db(db_history_list):
    history_list = []
    for db_history in db_history_list:
        history_list.append(Reality.History(
            db_history['price'],
            db_history['update_datetime'],
            db_history['description'],
            db_history['viewed_count']
        ))
    return history_list


