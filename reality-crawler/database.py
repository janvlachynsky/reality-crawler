import pymysql.cursors

class Database:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host="sql.endora.cz", # innodb.endora.cz
                user="homeuser",        # realityuser
                password="Ab1122334455",
                port=3308,              # 3306
                database="realitydbold",# realitydb
                cursorclass=pymysql.cursors.DictCursor,
            )
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS reality (
                    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, ad_id INT, provider_id, title VARCHAR(255), price INT, location VARCHAR(255), date DATE, description VARCHAR(255), viewed_count INT, advertiser_name VARCHAR(255), image VARCHAR(255), url VARCHAR(255) UNIQUE, note VARCHAR(255),
                    FOREIGN KEY (provider_id) REFERENCES reality_provider(id)
                    ON DELETE CASCADE)""")

                cursor.execute("""CREATE TABLE IF NOT EXISTS reality_history (
                    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, reality_id INT, price INT, date DATETIME DEFAULT CURRENT_TIMESTAMP, description VARCHAR(255), viewed_count INT, note VARCHAR(255),
                    FOREIGN KEY (reality_id) REFERENCES reality(id)
                    ON DELETE CASCADE)""")

                cursor.execute("""CREATE TABLE IF NOT EXISTS reality_provider (
                    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255) UNIQUE) """)
        except:
            raise Exception("Cannot connect to DB!")

    def execute_query(self, query, single=False):
        if self.connection is None:
            self.__init__()

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            if single:
                return cursor.fetchone()
            else:
                return cursor.fetchall()

    def get_all(self):
        return self.execute_query("SELECT * FROM reality")

    def get_by_id(self, id: int):
        return self.execute_query("SELECT * FROM reality WHERE id = {}".format(id))

    def insert_one(self, reality):
        query = f"INSERT IGNORE INTO reality (ad_id, title, price, location, date, description, viewed_count, advertiser_name, image, url) VALUES ({reality.id}, '{reality.title}', {reality.price}, '{reality.location}', '{reality.publish_date}', '{reality.description}', {reality.viewed_count}, '{reality.advertiser_name}', '{reality.image}', '{reality.href}' )"
        return self.execute_query(query, single=True)

    def insert_to_history(self, reality):
        query = f"INSERT INTO reality_history (reality_id, price, description, viewed_count) VALUES ({reality.id}, {reality.price}, '{reality.description}', {reality.viewed_count})"
        print(query)
        return self.execute_query(query, single=True)

    ## TODO: generic adding method
