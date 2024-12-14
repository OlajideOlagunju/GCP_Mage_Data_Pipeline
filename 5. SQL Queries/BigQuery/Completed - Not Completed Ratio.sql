SELECT COUNT(fact_.WorkOrderNumber) AS Total_WorkOrders, 
       COUNT(fact_.Completed_ID) AS Completed, 
       CAST(COUNT(fact_.WorkOrderNumber)-COUNT(fact_.Completed_ID) AS INT64) AS Not_Completed, 
       EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', add_.Date_time)) AS Year_Added,

FROM `WorkOrderModule.work_order_fact` AS fact_
LEFT JOIN `WorkOrderModule.added_` AS add_ on fact_.Added_ID = add_.Added_ID

WHERE EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', add_.Date_time)) IS NOT NULL
GROUP BY Year_Added
ORDER BY Year_Added DESC;