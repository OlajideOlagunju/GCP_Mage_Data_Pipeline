SELECT CAST(FLOOR((COUNT(fact_.Completed_ID) / COUNT(fact_.WorkOrderNumber))*100) AS INT64) AS Resolution_Rate, 
       EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', add_.Date_time)) AS Year_Added

FROM `WorkOrderModule.work_order_fact` AS fact_
LEFT JOIN `WorkOrderModule.added_` AS add_ on fact_.Added_ID = add_.Added_ID

WHERE EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', add_.Date_time)) IS NOT NULL
GROUP BY Year_Added
ORDER BY Year_Added DESC;