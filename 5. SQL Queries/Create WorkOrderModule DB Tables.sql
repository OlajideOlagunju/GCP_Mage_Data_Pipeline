-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.
-- Using SQL Server Syntax

SET XACT_ABORT ON

BEGIN TRANSACTION WORKORDERMODULE

CREATE TABLE [WorkOrder] (
    -- Surrogate Key
    [WorkOrderID] int  NOT NULL ,
    -- Foreign Key for 'Activity' Table
    [ActivityID] int  NOT NULL ,
    -- Foreign Key for 'ServiceRequest' Table
    [ServiceRequestID] int  NULL ,
    -- Foreign Key for 'WorkOrderTime' Table
    [TimeID] int  NOT NULL ,
    -- Work Order Unique Number
    [WorkOrderNumber] int  NOT NULL ,
    CONSTRAINT [PK_WorkOrder] PRIMARY KEY CLUSTERED (
        [WorkOrderID] ASC
    ),
    CONSTRAINT [UK_WorkOrder_WorkOrderNumber] UNIQUE (
        [WorkOrderNumber]
    )
)

CREATE TABLE [Activity] (
    -- Surrogate Key
    [ActivityID] int  NOT NULL ,
    -- Code for the Work Order Activity
    [ActivityCode] varchar(12)  NOT NULL ,
    -- Description of the Work Order Activity
    [ActivityDescription] varchar(300)  NULL ,
    CONSTRAINT [PK_Activity] PRIMARY KEY CLUSTERED (
        [ActivityID] ASC
    )
)

CREATE TABLE [ServiceRequest] (
    -- Surrogate Key
    [ServiceRequestID] int  NULL ,
    -- Service Request number where applicable
    [ServiceRequestNumber] int  NULL ,
    CONSTRAINT [PK_ServiceRequest] PRIMARY KEY CLUSTERED (
        [ServiceRequestID] ASC
    )
)

CREATE TABLE [WorkOrderTime] (
    -- Surrogate Key
    [TimeID] int  NOT NULL ,
    -- When the work order was started
    [Started] DATETIME  NULL ,
    -- When the work order was completed
    [Completed] DATETIME  NULL ,
    -- When the work order was added into the system
    [Added] DATETIME  NOT NULL ,
    CONSTRAINT [PK_WorkOrderTime] PRIMARY KEY CLUSTERED (
        [TimeID] ASC
    )
)

ALTER TABLE [WorkOrder] WITH CHECK ADD CONSTRAINT [FK_WorkOrder_ActivityID] FOREIGN KEY([ActivityID])
REFERENCES [Activity] ([ActivityID])

ALTER TABLE [WorkOrder] CHECK CONSTRAINT [FK_WorkOrder_ActivityID]

ALTER TABLE [WorkOrder] WITH CHECK ADD CONSTRAINT [FK_WorkOrder_ServiceRequestID] FOREIGN KEY([ServiceRequestID])
REFERENCES [ServiceRequest] ([ServiceRequestID])

ALTER TABLE [WorkOrder] CHECK CONSTRAINT [FK_WorkOrder_ServiceRequestID]

ALTER TABLE [WorkOrder] WITH CHECK ADD CONSTRAINT [FK_WorkOrder_TimeID] FOREIGN KEY([TimeID])
REFERENCES [WorkOrderTime] ([TimeID])

ALTER TABLE [WorkOrder] CHECK CONSTRAINT [FK_WorkOrder_TimeID]

COMMIT TRANSACTION WORKORDERMODULE