select distinct
    period,
    year(period) as year,
    month(period) as month,
    monthname(period) as month_name
from {{ ref('int_monthly_generation') }}