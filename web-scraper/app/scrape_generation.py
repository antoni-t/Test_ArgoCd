from scraping_base import ScrapingBase
from models import GenerationTable

POWER_TYPES_GENERATION = {
    1223: 'Stromerzeugung: Braunkohle',
    1224: 'Stromerzeugung: Kernenergie',
    1225: 'Stromerzeugung: Wind Offshore',
    1226: 'Stromerzeugung: Wasserkraft',
    1227: 'Stromerzeugung: Sonstige Konventionelle',
    1228: 'Stromerzeugung: Sonstige Erneuerbare',
    4066: 'Stromerzeugung: Biomasse',
    4067: 'Stromerzeugung: Wind Onshore',
    4068: 'Stromerzeugung: Photovoltaik',
    4069: 'Stromerzeugung: Steinkohle',
    4070: 'Stromerzeugung: Pumpspeicher',
    4071: 'Stromerzeugung: Erdgas'
}

REGIONS = ["DE"]

class ScrapeGeneration(ScrapingBase):
    """
    Class for scraping power generation data from an API and updating the database.

    This class extends the ScrapingBase class and provides specific functionality
    for handling power generation data. It uses the PowerGeneration model to
    interact with the corresponding database table.

    Attributes:
        Inherits attributes from ScrapingBase.
    """

    def __init__(self):
        """
        Initialize the ScrapingGeneration instance.

        This constructor initializes the ScrapingGeneration instance by calling
        the constructor of the parent ScrapingBase class with the specific
        power types and table class for power generation data.
        """
        super().__init__(POWER_TYPES_GENERATION, GenerationTable, REGIONS)