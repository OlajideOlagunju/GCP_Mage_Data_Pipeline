WITH Added_Table AS (
                     SELECT Added_ID,
                     EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', a.Date_time)) AS Year_ 
                     FROM `WorkOrderModule.added_` AS a)

SELECT SUM(COUNT(fact_.WorkOrderNumber)) 
       OVER (ORDER BY add_.Year_) AS Cumulative_Backlog_Count, 
       add_.Year_ AS Year_Added,

FROM `WorkOrderModule.work_order_fact` AS fact_
LEFT JOIN Added_Table AS add_ on fact_.Added_ID = add_.Added_ID

WHERE fact_.Completed_ID IS NULL AND 
       add_.Year_ IS NOT NULL AND EXTRACT(YEAR FROM CURRENT_DATETIME)-add_.Year_>3
GROUP BY Year_Added
ORDER BY Year_Added DESC;