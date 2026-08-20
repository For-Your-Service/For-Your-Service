# File: terraform/modules/databricks/sql_warehouse.tf
# Description: Databricks Serverless SQL Warehouse Endpoint with Auto-Stop Cost Control
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

resource "databricks_sql_endpoint" "serverless_warehouse" {
  count                     = var.enable_sql_warehouse ? 1 : 0
  name                      = "fys-sql-warehouse-${var.environment}"
  cluster_size              = "2X-Small"
  max_num_clusters          = 1
  min_num_clusters          = 1
  auto_stop_mins            = var.sql_warehouse_auto_stop_mins
  enable_serverless_compute = true

  tags {
    custom_tags {
      key   = "Project"
      value = "ForYourService"
    }
    custom_tags {
      key   = "Environment"
      value = var.environment
    }
    custom_tags {
      key   = "CostCenter"
      value = "VeteranJobMatching"
    }
  }
}
