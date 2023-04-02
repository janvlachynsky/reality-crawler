import pymysql.cursors


class Database:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port= int(self.port),
                cursorclass=pymysql.cursors.DictCursor,
            )
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reality_provider
                        (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255) UNIQUE)
                    ENGINE=INNODB;
                    """)

                cursor.execute("""
                    INSERT IGNORE INTO reality_provider (name) VALUES ('Bazos')
                    """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reality
                        (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, ad_id VARCHAR(255), provider_id INT, title VARCHAR(255), price INT, location VARCHAR(255), date DATE, description VARCHAR(255), viewed_count INT, advertiser_name VARCHAR(255), image VARCHAR(255), url VARCHAR(255) UNIQUE, note VARCHAR(255), flags VARCHAR(255),
                    FOREIGN KEY (provider_id) REFERENCES reality_provider(id)
                    ON DELETE CASCADE)
                    ENGINE=INNODB;
                    """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reality_history
                        (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, reality_id INT, price INT, update_datetime DATETIME DEFAULT CURRENT_TIMESTAMP, description VARCHAR(255), viewed_count INT, note VARCHAR(255),
                    FOREIGN KEY (reality_id) REFERENCES reality(id)
                    ON DELETE CASCADE)
                    ENGINE=INNODB;
                    """)
        except:
            raise Exception("Cannot connect to DB!")

    def execute_query(self, query, single=False):
        if self.connection is None:
            self.__init__(self.host, self.user, self.password, self.database, self.port)

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
            if single:
                return cursor.fetchone()
            else:
                return cursor.fetchall()

    # Inserts one reality entry into DB
    def insert_one(self, r):
        print("Inserting", r.title, r.url)
        query = f"""
            INSERT IGNORE INTO reality
                (ad_id, provider_id, title, price, location, date, description, viewed_count, advertiser_name, image, url)
            VALUES ('{r.id}', {r.provider}, '{r.title}', {r.price}, '{r.location}', '{r.date}', '{r.description}', {r.viewed_count}, '{r.advertiser_name}', '{r.image}', '{r.url}' )
            ON DUPLICATE KEY UPDATE
                price = {r.price},
                description = '{r.description}',
                viewed_count = {r.viewed_count},
                image = '{r.image}';
            """
        return self.execute_query(query, single=True)

    # Inserts current data to history table
    def insert_to_history(self, reality):
        print("Inserting to history", reality.title, reality.url)
        try:
            id = self.get_reality_id_from_ad_id(reality.id).get("id")
        except:
            print("Could not get id from DB, probalby not inserted yet! {}, {}".format(reality.id, reality.url))
            raise
        query = f"""
            INSERT INTO reality_history
                (reality_id, price, description, viewed_count)
            VALUES
                ({id}, {reality.price}, '{reality.description}', {reality.viewed_count});
            """
        return self.execute_query(query, single=True)

    # Getters
    def get_realities(self):
        return self.execute_query("SELECT * FROM reality order by date DESC")

    def get_reality_by_id(self, id: int):
        return self.execute_query("SELECT * FROM reality WHERE id = {}".format(id))

    def get_reality_id_from_ad_id(self, ad_id):
        return self.execute_query(f"""SELECT id FROM reality
                                      WHERE ad_id = '{ad_id}'
                                      """, single=True)

    def get_reality_history(self, reality):
        try:
            id = self.get_reality_id_from_ad_id(reality.id).get("id")
        except:
            raise Exception("Could not get id from DB, probalby not inserted yet! {}, {}".format(reality.id, reality.url))
        return self.get_reality_history_by_id(id)

    def get_reality_history_by_id(self, id: int):
        query = f"SELECT * FROM reality_history WHERE reality_id = {id}"
        return self.execute_query(query)

    ## TODO: generic adding method

    # Deactivates old realities
    # Old reality is a reality that has not been updated for more than 1 hour from the last update
    def deactivate_old_realities(self):
        query = """
            UPDATE reality r
                LEFT JOIN
                    (SELECT * from reality_history rh group by reality_id order by update_datetime DESC)
                    rh ON r.id = rh.reality_id
                SET flags = 'DELETED'
                WHERE rh.update_datetime <
                    (SELECT MAX(update_datetime) FROM reality_history) - INTERVAL 1 HOUR
            """
        return self.execute_query(query)
