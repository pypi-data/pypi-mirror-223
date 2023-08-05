# Cerc co2 emission

Uses the cerc-hub as a base for co2_emission calculation, it's intended to be used after executing the complete monthly energy
balance workflow called building by building

This module processes the object-oriented generalization to be used the co2 emission workflow

# installation

> $ pip install cerc-co2_emission

# usage

> from costs.co2_emission import Co2Emission
>
> Co2Emission(building, emissions_factor).co2_emission
> 

The available scenarios are defined in the constant class as an enum