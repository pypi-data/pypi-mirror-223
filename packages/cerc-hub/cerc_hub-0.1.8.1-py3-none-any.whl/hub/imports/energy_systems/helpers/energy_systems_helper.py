"""
Energy systems helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.helpers import constants as cte


class EnergySystemsHelper:
  """
  EnergySystems helper
  """
  _montreal_custom_fuel_to_hub_fuel = {
    'gas': cte.GAS,
    'electricity': cte.ELECTRICITY,
    'renewable': cte.RENEWABLE
  }

  @staticmethod
  def montreal_custom_fuel_to_hub_fuel(fuel):
    """
    Get hub fuel from montreal_custom catalog fuel
    :param fuel: str
    :return: str
    """
    return EnergySystemsHelper._montreal_custom_fuel_to_hub_fuel[fuel]

