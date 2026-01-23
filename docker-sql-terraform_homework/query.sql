--Question 3

SELECT 
    COUNT(1) AS trip_count
FROM 
    green_taxi_trips
WHERE 
    lpep_pickup_datetime >= '2025-11-01' 
    AND lpep_pickup_datetime < '2025-12-01'
    AND trip_distance <= 1.0;

-- 8007

-- Question 4

SELECT 
    lpep_pickup_datetime::DATE AS pickup_day,
    MAX(trip_distance) AS longest_distance
FROM 
    green_taxi_trips
WHERE 
    trip_distance < 100
GROUP BY 
    pickup_day
ORDER BY 
    longest_distance DESC
LIMIT 1;

-- 2025-11-14

-- Question 5

SELECT 
    z."Zone",
    SUM(t.total_amount) AS total_amount_sum
FROM 
    green_taxi_trips t
JOIN 
    taxi_zones z ON t."PULocationID" = z."LocationID"
WHERE 
    t.lpep_pickup_datetime::DATE = '2025-11-18'
GROUP BY 
    z."Zone"
ORDER BY 
    total_amount_sum DESC
LIMIT 1;

-- East Harlem North

-- Question 6

SELECT 
    z_dropoff."Zone" AS dropoff_zone,
    MAX(t.tip_amount) AS largest_tip
FROM 
    green_taxi_trips t
JOIN 
    taxi_zones z_pickup ON t."PULocationID" = z_pickup."LocationID"
JOIN 
    taxi_zones z_dropoff ON t."DOLocationID" = z_dropoff."LocationID"
WHERE 
    z_pickup."Zone" = 'East Harlem North'
    AND t.lpep_pickup_datetime >= '2025-11-01' 
    AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY 
    z_dropoff."Zone"
ORDER BY 
    largest_tip DESC
LIMIT 1;

-- Yorkville West
