class Reality:
    # TODO: use __slots__ for attributes
    class History:
        price:int = 0
        update_datetime = ""
        description = ""
        vievewd_count:int = 0

        def __init__(self, price=0, update_datetime="", description="", viewed_count=0, **kwargs):
            self.price = price
            self.update_datetime = update_datetime
            self.description = description
            self.viewed_count = viewed_count

    id = ""
    provider = ""
    title = ""
    price = ""
    url = ""
    date = ""
    location = ""
    description = ""
    image = ""
    advertiser_name = ""
    viewed_count = ""
    flags = ""
    is_favourite = False
    is_hidden = False
    is_expired = False
    history:list = list()


    def __init__(self, id, title, price, url, date, location, description, advertiser_name, image, viewed_count, flags = "", is_favourite = 0, is_hidden = 0, is_expired = 0, **kwargs):
        self.id = id
        self.title = title
        self.price = price
        self.url = url
        self.date = date
        self.location = location
        self.description = description
        self.advertiser_name = advertiser_name
        self.image = image
        self.viewed_count = viewed_count
        # TODO remove flags, replaced by is_favourite, is_hidden, is_expired
        self.flags = flags
        self.is_favourite = is_favourite
        self.is_hidden = is_hidden
        self.is_expired = is_expired

    def set_provider(self, provider):
        self.provider = provider

    def __str__(self):
        return "Id: {}\n Title: {}\n Price: {}\n PublishDate: {}\n Location: {}\n Description: {}\n url: {}\n Advertiser: {}\n ViewedCount: {}".format(
            self.id, self.title, self.price, self.date, self.location, self.description, self.url, self.advertiser_name, self.viewed_count
        )

    def toString(self):
        return "Id: {}\n Title: {}\n Price: {}\n PublishDate: {}\n Location: {}\n Description: {}\n url: {}\n Advertiser: {}\n ViewedCount: {}".format(
            self.id, self.title, self.price, self.date, self.location, self.description, self.url, self.advertiser_name, self.viewed_count
        )

    def set_history(self, history):
        self.history = history

def parse_single_from_db(db_reality):
    return Reality(**db_reality)

def parse_many_from_db(db_reality_list):
    reality_list = []
    for db_reality in db_reality_list:
        reality_list.append(parse_single_from_db(db_reality))
    return reality_list


def parse_history_from_db(db_history_list):
    history_list = []
    for db_history in db_history_list:
        history_list.append(Reality.History(**db_history))
    return history_list


