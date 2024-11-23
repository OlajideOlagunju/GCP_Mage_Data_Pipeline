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
DROP TABLE IF EXISTS started_;
DROP TABLE IF EXISTS completed_;
DROP TABLE IF EXISTS added_;

-- Create Tables
CREATE TABLE `work_order_fact` (
    -- Surrogate Key
    `WorkOrder_ID` int  NOT NULL ,
    -- Foreign Key for 'wo_activity_' Table
    `Activity_ID` int  NOT NULL ,
    -- Foreign Key for 'service_request_' Table
    `ServiceRequest_ID` int  NOT NULL ,
    -- Foreign Key for 'started_' Table
    `Started_ID` int  NOT NULL ,
    -- Foreign Key for 'completed_' Table
    `Completed_ID` int  NOT NULL ,
    -- Foreign Key for 'added_' Table
    `Added_ID` int  NOT NULL ,
    -- Work Order Unique Number
    `WorkOrderNumber` int  NOT NULL ,
    PRIMARY KEY (
        `WorkOrder_ID`
    )
);

CREATE TABLE `wo_activity_` (
    -- Surrogate Key
    `Activity_ID` int  NOT NULL ,
    -- Code for the Work Order Activity
    `ActivityCode` varchar(12)  NULL ,
    -- Description of the Work Order Activity
    `ActivityDescription` varchar(300)  NULL ,
    PRIMARY KEY (
        `Activity_ID`
    )
);

CREATE TABLE `service_request_` (
    -- Surrogate Key
    `ServiceRequest_ID` int  NOT NULL ,
    -- Service Request number where applicable
    `ServiceRequestNumber` int  NULL ,
    PRIMARY KEY (
        `ServiceRequest_ID`
    )
);

CREATE TABLE `started_` (
    -- Surrogate Key
    `Started_ID` int  NOT NULL ,
    -- The Datetime string
    `Date_time` varchar(30)  NULL ,
    PRIMARY KEY (
        `Started_ID`
    )
);

CREATE TABLE `completed_` (
    -- Surrogate Key
    `Completed_ID` int  NOT NULL ,
    -- The Datetime string
    `Date_time` varchar(30)  NULL ,
    PRIMARY KEY (
        `Completed_ID`
    )
);

CREATE TABLE `added_` (
    -- Surrogate Key
    `Added_ID` int  NOT NULL ,
    -- The Datetime string
    `Date_time` varchar(30)  NULL ,
    PRIMARY KEY (
        `Added_ID`
    )
);

ALTER TABLE `work_order_fact` ADD CONSTRAINT `fk_work_order_fact_Activity_ID` FOREIGN KEY(`Activity_ID`)
REFERENCES `wo_activity_` (`Activity_ID`);

ALTER TABLE `work_order_fact` ADD CONSTRAINT `fk_work_order_fact_ServiceRequest_ID` FOREIGN KEY(`ServiceRequest_ID`)
REFERENCES `service_request_` (`ServiceRequest_ID`);

ALTER TABLE `work_order_fact` ADD CONSTRAINT `fk_work_order_fact_Started_ID` FOREIGN KEY(`Started_ID`)
REFERENCES `started_` (`Started_ID`);

ALTER TABLE `work_order_fact` ADD CONSTRAINT `fk_work_order_fact_Completed_ID` FOREIGN KEY(`Completed_ID`)
REFERENCES `completed_` (`Completed_ID`);

ALTER TABLE `work_order_fact` ADD CONSTRAINT `fk_work_order_fact_Added_ID` FOREIGN KEY(`Added_ID`)
REFERENCES `added_` (`Added_ID`);

