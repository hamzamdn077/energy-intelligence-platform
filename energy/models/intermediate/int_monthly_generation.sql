select
    e.period,
    e.location,
    e.state_description,
    f.fuel_category,
    e.fuel_type_description,
    sum(e.generation) as total_generation,
    e.generation_units
from {{ ref('stg_electricity') }} e
left join {{ ref('fuel_categories') }} f
    on e.fuel_type_id = f.fuel_type_id
where e.generation is not null
group by
    e.period,
    e.location,
    e.state_description,
    f.fuel_category,
    e.fuel_type_description,
    e.generation_units