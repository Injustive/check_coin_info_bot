CREATE_TABLE_QUERY = """
                        CREATE TABLE IF NOT EXISTS coins_info (id serial PRIMARY KEY, 
                        user_id int NOT NULL UNIQUE, 
                        coins varchar[] NOT NULL)
                    """

INSERT_OR_UPDATE_QUERY = """
            INSERT INTO coins_info(user_id, coins)
            VALUES ($1, $2)
            ON CONFLICT(user_id) DO UPDATE SET coins = array_append(coins_info.coins, $3)
        """

GET_COINS_LIST_QUERY = "SELECT coins FROM coins_info WHERE user_id = $1"

DELETE_COIN_QUERY = "UPDATE coins_info SET coins = array_remove(coins_info.coins, $1) WHERE user_id = $2"
