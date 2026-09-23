select distinct
    location,
    state_description
from {{ ref('int_monthly_generation') }}