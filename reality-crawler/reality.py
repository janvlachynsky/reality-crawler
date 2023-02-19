class Reality:
    id = ""
    provider = ""
    title = ""
    price = ""
    href = ""
    publish_date = ""
    location = ""
    description = ""
    image = ""
    advertiser_name = ""
    viewed_count = ""

    def __init__(self, id, title, price, href, publish_date, location, description, advertiser_name, viewed_count):
        self.id = id
        self.title = title
        self.price = price
        self.href = href
        self.publish_date = publish_date
        self.location = location
        self.description = description
        self.advertiser_name = advertiser_name
        self.viewed_count = viewed_count

    def set_provider(self, provider):
        self.provider = provider

    def __str__(self):
        return "Id: {}\n Title: {}\n Price: {}\n PublishDate: {}\n Location: {}\n Description: {}\n Href: {}\n Advertiser: {}\n ViewedCount: {}".format(
            self.id, self.title, self.price, self.publish_date, self.location, self.description, self.href, self.advertiser_name, self.viewed_count
        )
    def toString(self):
        return "Id: {}\n Title: {}\n Price: {}\n PublishDate: {}\n Location: {}\n Description: {}\n Href: {}\n Advertiser: {}\n ViewedCount: {}".format(
            self.id, self.title, self.price, self.publish_date, self.location, self.description, self.href, self.advertiser_name, self.viewed_count
        )
