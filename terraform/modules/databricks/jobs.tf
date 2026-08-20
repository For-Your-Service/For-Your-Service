# File: terraform/modules/databricks/jobs.tf
# Description: Databricks Ingestion & Job Matching Automated Workflow Definitions
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# Multi-Source Ingestion & Matching Pipeline Job
# -----------------------------------------------------------------------------
resource "databricks_job" "daily_ingestion_pipeline" {
  count = var.enable_jobs ? 1 : 0
  name  = "fys-daily-ingestion-pipeline-${var.environment}"

  schedule {
    quartz_cron_expression = "0 0 6 * * ?" # Run daily at 6:00 AM UTC
    timezone_id            = "America/New_York"
    pause_status           = var.environment == "prod" ? "UNPAUSED" : "PAUSED"
  }

  task {
    task_key = "bronze_job_ingestion"

    notebook_task {
      notebook_path = "/Repos/For-Your-Service/notebooks/03_Bronze_Ingestion"
      source        = "WORKSPACE"
    }

    sql_task {
      query {
        query_id = "ingestion_health_check"
      }
      warehouse_id = var.enable_sql_warehouse ? databricks_sql_endpoint.serverless_warehouse[0].id : ""
    }
  }

  tags = local.custom_tags
}
