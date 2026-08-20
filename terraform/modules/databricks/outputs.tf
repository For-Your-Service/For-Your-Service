# File: terraform/modules/databricks/outputs.tf
# Description: Databricks Module Resource Outputs
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

output "bronze_schema_name" {
  value       = var.enable_unity_catalog ? databricks_schema.bronze[0].name : null
  description = "Databricks Unity Catalog Bronze Schema Name"
}

output "silver_schema_name" {
  value       = var.enable_unity_catalog ? databricks_schema.silver[0].name : null
  description = "Databricks Unity Catalog Silver Schema Name"
}

output "gold_schema_name" {
  value       = var.enable_unity_catalog ? databricks_schema.gold[0].name : null
  description = "Databricks Unity Catalog Gold Schema Name"
}

output "sql_warehouse_id" {
  value       = var.enable_sql_warehouse ? databricks_sql_endpoint.serverless_warehouse[0].id : null
  description = "Databricks Serverless SQL Warehouse Endpoint ID"
}

output "sql_warehouse_http_path" {
  value       = var.enable_sql_warehouse ? "/sql/1.0/warehouses/${databricks_sql_endpoint.serverless_warehouse[0].id}" : null
  description = "Databricks SQL Warehouse HTTP Path for API and App connectors"
}

output "aws_secret_scope_name" {
  value       = var.enable_secrets ? databricks_secret_scope.aws_credentials[0].name : null
  description = "Databricks AWS credentials secret scope name"
}

output "api_secret_scope_name" {
  value       = var.enable_secrets ? databricks_secret_scope.api_keys[0].name : null
  description = "Databricks API keys secret scope name"
}
