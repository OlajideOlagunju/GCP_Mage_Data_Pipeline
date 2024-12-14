SELECT fact_.WorkOrderNumber, act_.ActivityCode, act_.ActivityDescription, 
       EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', add_.Date_time)) AS Year_Added,
       DATETIME_DIFF(CURRENT_DATETIME, PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', add_.Date_time), YEAR)-3 AS Backlog_Years

FROM `WorkOrderModule.work_order_fact` AS fact_
LEFT JOIN `WorkOrderModule.added_` AS add_ on fact_.Added_ID = add_.Added_ID
LEFT JOIN `WorkOrderModule.wo_activity_` AS act_ on fact_.Activity_ID = act_.Activity_ID
LEFT JOIN `WorkOrderModule.service_request_` AS srq_ on fact_.ServiceRequest_ID = srq_.ServiceRequest_ID

WHERE fact_.Completed_ID IS NULL
ORDER BY Backlog_Years DESC;