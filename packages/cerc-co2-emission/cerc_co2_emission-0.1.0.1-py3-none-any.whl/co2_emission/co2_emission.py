"""
CO2 emission module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from hub.city_model_structure.building import Building
import hub.helpers.constants as cte


class Co2Emission:
  """
  Cost class
  """

  def __init__(self, building: Building, emissions_factor=None):
    if emissions_factor is None:
      emissions_factor = {cte.GAS: 0.2025,
                          cte.ELECTRICITY: 0.00113,
                          cte.DIESEL: 0.2683,
                          cte.RENEWABLE: 0}
    self._emissions_factor = emissions_factor
    self._building = building

  @property
  def building(self) -> Building:
    """
    Get current building.
    """
    return self._building

  @property
  def operational_co2(self) -> dict:
    """
    Get operational_co2
    :return: dict
    """
    results = {}
    for energy_system in self._building.energy_systems:
      fuel_type = energy_system.generation_system.generic_generation_system.fuel_type
      for demand_type in energy_system.demand_types:
        if demand_type == cte.ELECTRICITY:
          continue
        results_by_time_period = {}
        if demand_type == cte.HEATING:
          for time_period in self._building.heating_consumption:
            values = []
            for value in self._building.heating_consumption[time_period]:
              values.append(value * self._emissions_factor[fuel_type])
            results_by_time_period[time_period] = values
        if demand_type == cte.COOLING:
          for time_period in self._building.cooling_consumption:
            values = []
            for value in self._building.cooling_consumption[time_period]:
              values.append(value * self._emissions_factor[fuel_type])
            results_by_time_period[time_period] = values
        if demand_type == cte.DOMESTIC_HOT_WATER:
          for time_period in self._building.domestic_hot_water_consumption:
            values = []
            for value in self._building.domestic_hot_water_consumption[time_period]:
              values.append(value * self._emissions_factor[fuel_type])
            results_by_time_period[time_period] = values
        results[demand_type] = results_by_time_period

    results_by_time_period = {}
    for time_period in self._building.lighting_electrical_demand:
      values = []
      for value in self._building.lighting_electrical_demand[time_period]['insel meb']:
        values.append(value * self._emissions_factor[cte.ELECTRICITY])
      results_by_time_period[time_period] = values
    results[cte.LIGHTING] = results_by_time_period

    results_by_time_period = {}
    for time_period in self._building.appliances_electrical_demand:
      values = []
      for value in self._building.appliances_electrical_demand[time_period]['insel meb']:
        values.append(value * self._emissions_factor[cte.ELECTRICITY])
      results_by_time_period[time_period] = values
    results[cte.APPLIANCES] = results_by_time_period

    return results
