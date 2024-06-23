import mysql.connector
class MySQLDatabase:
    def __init__(self, host, user, password, database):
        """
        Initializes the MySQLDatabase object with connection parameters and sets up placeholders for connection and cursor.

        Parameters:
        - host (str): The hostname or IP address of the MySQL server.
        - user (str): The username used to authenticate with MySQL.
        - password (str): The password used to authenticate with MySQL.
        - database (str): The name of the database to use.

        Returns:
        None
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    def connect(self):
        """
        Establishes a connection to the MySQL database using the instance's connection parameters.

        Returns:
        None
        """
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.cursor = self.connection.cursor()
    def disconnect(self):
        """
        Closes the connection to the MySQL database if it is open.

        Returns:
        None
        """
        if self.connection:
            self.connection.close()
    def create_database(self):
        """
        Creates the database specified by the instance's database parameter if it does not already exist.

        Returns:
        None
        """
        self.connect()
        query = f"CREATE DATABASE IF NOT EXISTS {self.database}"
        self.cursor.execute(query)
        self.disconnect()
    def create_table(self, table_name, columns):
        """
        Creates a table with the specified name and columns if it does not already exist.

        Parameters:
        - table_name (str): The name of the table to create.
        - columns (list of str): A list of column definitions, e.g., ["id INT AUTO_INCREMENT PRIMARY KEY", "name VARCHAR(255)"].

        Returns:
        None
        """
        self.connect()
        columns_str = ', '.join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.cursor.execute(query)
        self.connection.commit()
        self.disconnect()
    def insert_record(self, table_name, data):
        """
        Inserts a record into the specified table.

        Parameters:
        - table_name (str): The name of the table to insert the record into.
        - data (dict): A dictionary where keys are column names and values are the corresponding values to insert.

        Returns:
        None
        """
        self.connect()
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{value}'" for value in data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(query)
        self.connection.commit()
        self.disconnect()
    def select_records(self, table_name, condition=None):
        """
        Selects records from the specified table, optionally filtered by a condition.

        Parameters:
        - table_name (str): The name of the table to select records from.
        - condition (str, optional): A condition for filtering records, e.g., "id > 10". Defaults to None.

        Returns:
        list: A list of tuples representing the selected records.
        """
        self.connect()
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        self.disconnect()
        return records
    def update_record(self, table_name, data, condition):
        """
        Updates records in the specified table that meet the given condition.

        Parameters:
        - table_name (str): The name of the table to update records in.
        - data (dict): A dictionary where keys are column names and values are the new values for those columns.
        - condition (str): A condition that identifies which records to update.

        Returns:
        None
        """
        self.connect()
        updates = ', '.join([f"{key}='{value}'" for key, value in data.items()])
        query = f"UPDATE {table_name} SET {updates} WHERE {condition}"
        self.cursor.execute(query)
        self.connection.commit()
        self.disconnect()
    def delete_record(self, table_name, condition):
        """
        Deletes records from the specified table that meet the given condition.

        Parameters:
        - table_name (str): The name of the table to delete records from.
        - condition (str): A condition that identifies which records to delete.

        Returns:
        None
        """
        self.connect()
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.connection.commit()
        self.disconnect()
