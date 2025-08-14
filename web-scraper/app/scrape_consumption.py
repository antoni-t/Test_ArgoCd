from scraping_base import ScrapingBase
from models import ConsumptionTable

POWER_TYPES_CONSUMPTION = {
    410: 'Stromverbrauch: Gesamt (Netzlast)',
    4359: 'Stromverbrauch: Residuallast',
    4387: 'Stromverbrauch: Pumpspeicher'
}

REGIONS = ["DE"]

class ScrapeConsumption(ScrapingBase):
    """
    Class for scraping power consumption data from an API and updating the database.

    This class extends the ScrapingBase class and provides specific functionality
    for handling power consumption data. It uses the PowerConsumption model to
    interact with the corresponding database table.

    Attributes:
        Inherits attributes from ScrapingBase.
    """

    def __init__(self):
        """
        Initialize the ScrapingConsumption instance.

        This constructor initializes the ScrapingConsumption instance by calling
        the constructor of the parent ScrapingBase class with the specific
        power types and table class for power consumption data.
        """
        super().__init__(POWER_TYPES_CONSUMPTION, ConsumptionTable, REGIONS)