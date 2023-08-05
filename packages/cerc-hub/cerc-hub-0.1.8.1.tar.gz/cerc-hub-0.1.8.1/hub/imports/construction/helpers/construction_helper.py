"""
Construction helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.helpers import constants as cte


class ConstructionHelper:
  """
  Construction helper
  """
  # NREL

  _reference_city_to_nrel_climate_zone = {
    'Miami': 'ASHRAE_2004:1A',
    'Houston': 'ASHRAE_2004:2A',
    'Phoenix': 'ASHRAE_2004:2B',
    'Atlanta': 'ASHRAE_2004:3A',
    'Los Angeles': 'ASHRAE_2004:3B',
    'Las Vegas': 'ASHRAE_2004:3B',
    'San Francisco': 'ASHRAE_2004:3C',
    'Baltimore': 'ASHRAE_2004:4A',
    'Albuquerque': 'ASHRAE_2004:4B',
    'Seattle': 'ASHRAE_2004:4C',
    'Chicago': 'ASHRAE_2004:5A',
    'Boulder': 'ASHRAE_2004:5B',
    'Minneapolis': 'ASHRAE_2004:6A',
    'Helena': 'ASHRAE_2004:6B',
    'Duluth': 'ASHRAE_2004:7A',
    'Fairbanks': 'ASHRAE_2004:8A'
  }

  _reference_city_to_nrcan_climate_zone = {
    'Montreal': '6',
    'Repentigny': '6',
    "Montreal Int'l": '6',
    'Levis': '7A',
    'Quebec City': '7A',
    'Kelowna': '5',
    'Park Slope': '4'
  }

  _reference_city_to_israel_climate_zone = {
    'Eilat': 'BWh'
  }

  @staticmethod
  def yoc_to_nrel_standard(year_of_construction):
    """
    Year of construction to NREL standard
    :param year_of_construction: int
    :return: str
    """
    if int(year_of_construction) < 2009:
      standard = 'ASHRAE 90.1_2004'
    else:
      standard = 'ASHRAE 189.1_2009'
    return standard

  @staticmethod
  def city_to_nrel_climate_zone(reference_city):
    """
    City name to NREL climate zone
    :param reference_city: str
    :return: str
    """
    # todo: finish dictionary implementation
    if reference_city not in ConstructionHelper._reference_city_to_nrel_climate_zone:
      reference_city = 'Baltimore'
    return ConstructionHelper._reference_city_to_nrel_climate_zone[reference_city]

  @staticmethod
  def city_to_nrcan_climate_zone(reference_city):
    """
    City name to NRCAN climate zone
    :param reference_city: str
    :return: str
    """
    return ConstructionHelper._reference_city_to_nrcan_climate_zone[reference_city]

  @staticmethod
  def city_to_israel_climate_zone(reference_city):
    """
    City name to Israel climate zone
    :param reference_city: str
    :return: str
    """
    return ConstructionHelper._reference_city_to_israel_climate_zone[reference_city]
