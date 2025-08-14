import os
from datetime import datetime, timezone
import requests
from models import databaseSession

INTERVAL_TYPES = ["hour", "quarterhour", "day", "week", "month", "year"]

class ScrapingBase:
    """
    Base class for scraping data from an API and updating the database.

    This class provides common functionality for fetching data from an API,
    inserting data into the database, and updating existing data in the database.
    It is intended to be extended by specific scraping classes for different types
    of power data (e.g., generation, consumption).

    Attributes:
        power_types (dict): A dictionary mapping power type IDs to their names.
        table_class (class): The SQLAlchemy model class corresponding to the table
                             in the database where the data will be stored.
    """

    def __init__(self, power_types, table_class, regions):
        """
        Initialize the ScrapingBase instance.

        Args:
            power_types (dict): A dictionary mapping power type IDs to their names.
            table_class (class): The SQLAlchemy model class corresponding to the table
                                 in the database where the data will be stored.
        """
        self.power_types = power_types
        self.table_class = table_class
        self.name = table_class.__tablename__
        self.regions = regions
        self.intervalType = INTERVAL_TYPES[1]

    def get_latest_timestamp_from_api(self, region, power_type):
        """
        Fetch data from the specified API URL.

        Args:
            region (str): Region to query
            power_type (int): Type of power source to query

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
            requests.exceptions.Timeout: The request took too long.
            requests.exceptions.RequestException: An error occurred while handling the request.
        """
        try:
            print(f"{datetime.now()} - {self.name}: Scraping data..")
            url = self.get_url(
                f"chart_data/{power_type}/{region}/index_{self.intervalType}.json")
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            timestamps = sorted(response.json()['timestamps'], reverse=True)
            return timestamps[0]
        except requests.exceptions.HTTPError as e:
            print(
                f"{datetime.now()} - {self.name}: HTTP error code: {e.response.status_code}")
            return None
        except requests.exceptions.Timeout:
            print(f"{datetime.now()} - {self.name}: The request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"{datetime.now()} - {self.name}: An error occurred: {e}")
            return None

    def fetch_data_from_api(self, region, power_type):
        """
        Fetch data from the specified API URL.

        Args:
            region (str): Region to query
            power_type (int): Type of power source to query

        Returns:
            dict: The data returned by the API

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
            requests.exceptions.Timeout: The request took too long.
            requests.exceptions.RequestException: An error occurred while handling the request.
        """
        try:
            print(f"{datetime.now()} - {self.name}: Scraping data..")

            timestamp = self.get_latest_timestamp_from_api(region, power_type)

            url = self.get_url(
                f"chart_data/{power_type}/{region}/{power_type}_{region}_{self.intervalType}_{timestamp}.json")

            # Set a timeout of 10 seconds
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            # Assuming the API returns JSON data
            return response.json()["series"]
        except requests.exceptions.HTTPError as e:
            print(
                f"{datetime.now()} - {self.name}: HTTP error code: {e.response.status_code}")
            return None
        except requests.exceptions.Timeout:
            print(f"{datetime.now()} - {self.name}: The request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"{datetime.now()} - {self.name}: An error occurred: {e}")
            return None

    def insert_data_into_db(self, data, region, power_type):
        """
        Insert data into the MariaDB database using SQLAlchemy.

        Args:
            data (list): A list of dictionaries containing the data to be inserted.
        """
        db = databaseSession()
        try:
            for item in data:
                # Convert timestamp to UTC
                utc_timestamp = datetime.fromtimestamp(item['timestamp']/1000, tz=timezone.utc)

                if not self.search_entry_in_db(db, utc_timestamp, region, power_type):
                    db_item = self.table_class(
                        wattage=item['wattage'],
                        timestamp=utc_timestamp,  # Use UTC timestamp
                        power_type=power_type,
                        region=region
                    )
                    db.add(db_item)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"{datetime.now()} - {self.name}: An error occurred: {e}")
        finally:
            db.close()

    def search_entry_in_db(self, db_session, timestamp, region, power_type):
        """
        Search for an entry in the database based on the provided timestamp, region, and power type.

        This method queries the database to check if an entry with the specified timestamp,
        region, and power type already exists.

        Args:
            db_session (sqlalchemy.orm.Session): The SQLAlchemy session used to interact with the database.
            timestamp (datetime): The UTC timestamp of the entry to search for.
            region (str): The region of the entry to search for.
            power_type (int): The power type of the entry to search for.

        Returns:
            bool: True if an entry with the specified parameters exists in the database, False otherwise.
        """
        db_item = db_session.query(self.table_class).filter(
            self.table_class.power_type == power_type,
            self.table_class.region == region,
            self.table_class.timestamp == timestamp  # Use UTC timestamp
        ).first()
        return db_item is not None

    def get_url(self, path):
        """
        Create the combination of base_url and the endpoint_url

        Returns:
            str: the URL to query
        """
        return os.getenv('API_BASE_URL', "http://localhost") + "/" + str(path)

    def fetch_and_insert_X_entries(self, num_values):
        """
        This function fills the latest X datapoints available from the API and initially insert into the database. For each region and power type, data will be queried.

        Args:
            num_values (int): Number of last X values to write into database

        """
        for region in self.regions:
            for power_type in self.power_types:
                data = self.fetch_data_from_api(region, power_type)

                # Filter out entries where the second value is None
                filtered_data = [item for item in data if item[1] is not None]
                # Sort the data by the first value in descending order
                sorted_data = sorted(filtered_data, key=lambda x: x[0], reverse=True)
                # Keep only the first five values
                first_X = sorted_data[:num_values]
                # Convert the first five items to a dictionary
                result = [{'timestamp': item[0], 'wattage': item[1]} for item in first_X]
                if len(result) > 0:
                    self.insert_data_into_db(result, region, power_type)

    def fetch_and_update_data(self):
            """
            Fetch and update the latest data from the API and insert it into the database.

            This method calls the `fetch_and_insert_X_entries` method with a default value of 5,
            which means it will fetch and insert the latest 5 data points for each region and power type.

            Returns:
                None
            """
            self.fetch_and_insert_X_entries(5)