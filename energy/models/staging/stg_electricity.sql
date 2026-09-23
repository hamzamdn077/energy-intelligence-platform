select
    period,
    location,
    state_description,
    sector_id,
    sector_description,
    fuel_type_id,
    fuel_type_description,
    generation,
    generation_units
from {{ source('energy', 'electricity') }}