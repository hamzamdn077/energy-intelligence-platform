select
    period,
    location,
    state_description,
    fuel_type_id,
    fuel_type_description,
    total_generation,
    generation_units
from {{ ref('int_monthly_generation') }}