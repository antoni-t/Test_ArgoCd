import os
import time
import schedule
from models import wait_for_db, create_tables_if_not_exist, populate_power_type_mapping
from scrape_generation import ScrapeGeneration
from scrape_consumption import ScrapeConsumption

if __name__ == "__main__":
    wait_for_db()

    scrape_generation = ScrapeGeneration()
    scrape_consumption = ScrapeConsumption()
    # Create tables in database if they are not present
    create_tables_if_not_exist()
    # Populate tables with default values
    populate_power_type_mapping()
    scrape_generation.fetch_and_insert_X_entries(10)
    scrape_consumption.fetch_and_insert_X_entries(10)

    scraping_interval_minutes = int(os.getenv("SCRAPING_INTERVAL_MINUTES", "15"))

    schedule.every(scraping_interval_minutes).minutes.do(
        scrape_generation.fetch_and_update_data)
    schedule.every(scraping_interval_minutes).minutes.do(
        scrape_consumption.fetch_and_update_data)

    while True:
        schedule.run_pending()
        time.sleep(1)