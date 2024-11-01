-- MariaDB script
-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/

-- Drop the database if it exists
DROP DATABASE IF EXISTS WorkOrderModule;

-- Create the database
CREATE DATABASE WorkOrderModule;

-- Use the database
USE WorkOrderModule;

-- Drop Tables
DROP TABLE IF EXISTS work_order_fact;
DROP TABLE IF EXISTS wo_activity_;
DROP TABLE IF EXISTS service_request_;
DROP TABLE IF EXISTS work_order_time_;
DROP TABLE IF EXISTS wo_time_type_;
DROP TABLE IF EXISTS day_of_week_;

-- Create Tables
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
    -- Foreign Key for 'work_order_fact' Table
    `WorkOrder_ID` int  NOT NULL ,
    -- Surrogate Key
    `Time_ID` int  NOT NULL ,
    -- Foreign Key for 'wo_time_type_' Table
    `TimeType_ID` int  NOT NULL ,
    -- Foreign Key for 'day_of_week_' Table
    `Day_of_week_ID` int  NOT NULL ,
    -- The Year
    `Year` int  NOT NULL ,
    -- The Month
    `Month` int  NOT NULL ,
    -- The Day
    `Day` int  NOT NULL ,
    -- The Hour
    `Hour` int  NOT NULL ,
    -- The Minute
    `Minute` int  NOT NULL ,
    -- The Second
    `Second` int  NOT NULL ,
    PRIMARY KEY (
        `Time_ID`
    )
);

CREATE TABLE `wo_time_type_` (
    -- Surrogate Key
    `TimeType_ID` int  NOT NULL ,
    -- The time description. i.e. 'Started','Completed', 'Added'
    `Time_Type` varchar(20)  NOT NULL ,
    PRIMARY KEY (
        `TimeType_ID`
    )
);

CREATE TABLE `day_of_week_` (
    -- Surrogate Key
    `Day_of_week_ID` int  NOT NULL ,
    -- The day of the week
    `DayInWeek` varchar(12)  NOT NULL ,
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

ALTER TABLE `work_order_time_` ADD CONSTRAINT `fk_work_order_time__WorkOrder_ID` FOREIGN KEY(`WorkOrder_ID`)
REFERENCES `work_order_fact` (`WorkOrder_ID`);

ALTER TABLE `work_order_time_` ADD CONSTRAINT `fk_work_order_time__TimeType_ID` FOREIGN KEY(`TimeType_ID`)
REFERENCES `wo_time_type_` (`TimeType_ID`);

ALTER TABLE `work_order_time_` ADD CONSTRAINT `fk_work_order_time__Day_of_week_ID` FOREIGN KEY(`Day_of_week_ID`)
REFERENCES `day_of_week_` (`Day_of_week_ID`);

