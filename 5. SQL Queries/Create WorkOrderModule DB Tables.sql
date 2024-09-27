
CREATE TABLE `work_order_fact` (
    -- Surrogate Key
    `WorkOrder_ID` int  NOT NULL ,
    -- Foreign Key for 'wo_activity_' Table
    `Activity_ID` int  NOT NULL ,
    -- Foreign Key for 'service_request_' Table
    `ServiceRequest_ID` int  NULL ,
    -- Foreign Key for 'work_order_time_' Table
    `TimeID` int  NOT NULL ,
    -- Work Order Unique Number
    `WorkOrderNumber` int  NOT NULL ,
    PRIMARY KEY (
        `WorkOrder_ID`
    ),
    CONSTRAINT `uc_work_order_fact_WorkOrderNumber` UNIQUE (
        `WorkOrderNumber`
    )
);

CREATE TABLE `wo_activity_` (
    -- Surrogate Key
    `ActivityID` int  NOT NULL ,
    -- Code for the Work Order Activity
    `ActivityCode` varchar(12)  NOT NULL ,
    -- Description of the Work Order Activity
    `ActivityDescription` varchar(300)  NULL ,
    PRIMARY KEY (
        `ActivityID`
    )
);

CREATE TABLE `service_request_` (
    -- Surrogate Key
    `ServiceRequest_ID` int  NULL ,
    -- Service Request number where applicable
    `ServiceRequestNumber` int  NULL ,
    PRIMARY KEY (
        `ServiceRequest_ID`
    )
);

CREATE TABLE `work_order_time_` (
    -- Surrogate Key
    `Time_ID` int  NOT NULL ,
    -- Foreign Key for 'wo_time_started_' Table
    `Started_ID` int  NULL ,
    -- Foreign Key for 'wo_time_completed_' Table
    `Completed_ID` int  NULL ,
    -- Foreign Key for 'wo_time_added_' Table
    `Added_ID` int  NULL ,
    PRIMARY KEY (
        `Time_ID`
    )
);

CREATE TABLE `wo_time_started_` (
    -- Surrogate Key
    `Started_ID` int  NULL ,
    -- When the work order was started
    `Started_time` DATETIME  NULL ,
    -- Foreign Key for 'day_of_week_' Table
    `Day_of_week_ID` int  NULL ,
    -- The Year the Work Order was added
    `Year` int  NULL ,
    -- The Month the Work Order was added
    `Month` int  NULL ,
    -- The Day the Work Order was added
    `Day` int  NULL ,
    -- The Hour the Work Order was added
    `Hour` int  NULL ,
    -- The Minute the Work Order was added
    `Minute` int  NULL ,
    -- The Second the Work Order was added
    `Second` int  NULL ,
    PRIMARY KEY (
        `Started_ID`
    )
);

CREATE TABLE `wo_time_completed_` (
    -- Surrogate Key
    `Completed_ID` int  NULL ,
    -- When the work order was completed
    `Completed_time` DATETIME  NULL ,
    -- Foreign Key for 'day_of_week_' Table
    `Day_of_week_ID` int  NULL ,
    -- The Year the Work Order was added
    `Year` int  NULL ,
    -- The Month the Work Order was added
    `Month` int  NULL ,
    -- The Day the Work Order was added
    `Day` int  NULL ,
    -- The Hour the Work Order was added
    `Hour` int  NULL ,
    -- The Minute the Work Order was added
    `Minute` int  NULL ,
    -- The Second the Work Order was added
    `Second` int  NULL ,
    PRIMARY KEY (
        `Completed_ID`
    )
);

CREATE TABLE `wo_time_added_` (
    -- Surrogate Key
    `Added_ID` int  NOT NULL ,
    -- When the work order was added into the system
    `Added_time` DATETIME  NOT NULL ,
    -- Foreign Key for 'day_of_week_' Table
    `Day_of_week_ID` int  NOT NULL ,
    -- The Year the Work Order was added
    `Year` int  NOT NULL ,
    -- The Month the Work Order was added
    `Month` int  NOT NULL ,
    -- The Day the Work Order was added
    `Day` int  NOT NULL ,
    -- The Hour the Work Order was added
    `Hour` int  NOT NULL ,
    -- The Minute the Work Order was added
    `Minute` int  NOT NULL ,
    -- The Second the Work Order was added
    `Second` int  NOT NULL ,
    PRIMARY KEY (
        `Added_ID`
    )
);

CREATE TABLE `day_of_week_` (
    -- Surrogate Key
    `Day_of_week_ID` int  NOT NULL ,
    -- The day of the week
    `dayinweek` varchar(12)  NOT NULL ,
    PRIMARY KEY (
        `Day_of_week_ID`
    )
);

ALTER TABLE `work_order_fact` ADD CONSTRAINT `fk_work_order_fact_Activity_ID` FOREIGN KEY(`Activity_ID`)
REFERENCES `wo_activity_` (`ActivityID`);

ALTER TABLE `work_order_fact` ADD CONSTRAINT `fk_work_order_fact_ServiceRequest_ID` FOREIGN KEY(`ServiceRequest_ID`)
REFERENCES `service_request_` (`ServiceRequest_ID`);

ALTER TABLE `work_order_fact` ADD CONSTRAINT `fk_work_order_fact_TimeID` FOREIGN KEY(`TimeID`)
REFERENCES `work_order_time_` (`Time_ID`);

ALTER TABLE `work_order_time_` ADD CONSTRAINT `fk_work_order_time__Started_ID` FOREIGN KEY(`Started_ID`)
REFERENCES `wo_time_started_` (`Started_ID`);

ALTER TABLE `work_order_time_` ADD CONSTRAINT `fk_work_order_time__Completed_ID` FOREIGN KEY(`Completed_ID`)
REFERENCES `wo_time_completed_` (`Completed_ID`);

ALTER TABLE `work_order_time_` ADD CONSTRAINT `fk_work_order_time__Added_ID` FOREIGN KEY(`Added_ID`)
REFERENCES `wo_time_added_` (`Added_ID`);

ALTER TABLE `wo_time_started_` ADD CONSTRAINT `fk_wo_time_started__Day_of_week_ID` FOREIGN KEY(`Day_of_week_ID`)
REFERENCES `day_of_week_` (`Day_of_week_ID`);

ALTER TABLE `wo_time_completed_` ADD CONSTRAINT `fk_wo_time_completed__Day_of_week_ID` FOREIGN KEY(`Day_of_week_ID`)
REFERENCES `day_of_week_` (`Day_of_week_ID`);

ALTER TABLE `wo_time_added_` ADD CONSTRAINT `fk_wo_time_added__Day_of_week_ID` FOREIGN KEY(`Day_of_week_ID`)
REFERENCES `day_of_week_` (`Day_of_week_ID`);

