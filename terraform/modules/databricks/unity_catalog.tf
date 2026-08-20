# File: terraform/modules/databricks/unity_catalog.tf
# Description: Databricks Unity Catalog Schemas for Bronze, Silver, and Gold Layers
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. Bronze Schema: Raw Job Postings & API Ingestion
# -----------------------------------------------------------------------------
resource "databricks_schema" "bronze" {
  count        = var.enable_unity_catalog ? 1 : 0
  catalog_name = var.catalog_name
  name         = "${local.schema_prefix}_bronze"
  comment      = "Raw ingestion layer for USAJOBS, JSearch, Adzuna, and Glassdoor job postings (${var.environment})"

  properties = {
    "delta.autoOptimize.optimizeWrite" = "true"
    "delta.autoOptimize.autoCompact"   = "true"
    "layer"                            = "bronze"
    "project"                          = "foryourservice"
  }
}

# -----------------------------------------------------------------------------
# 2. Silver Schema: Normalized Veteran Profiles, O*NET Skills, Cleaned Jobs
# -----------------------------------------------------------------------------
resource "databricks_schema" "silver" {
  count        = var.enable_unity_catalog ? 1 : 0
  catalog_name = var.catalog_name
  name         = "${local.schema_prefix}_silver"
  comment      = "Enriched silver layer containing normalized veteran profiles, MOS crosswalks, and deduplicated jobs (${var.environment})"

  properties = {
    "delta.autoOptimize.optimizeWrite" = "true"
    "delta.autoOptimize.autoCompact"   = "true"
    "layer"                            = "silver"
    "project"                          = "foryourservice"
  }
}

# -----------------------------------------------------------------------------
# 3. Gold Schema: 384-Dim Embeddings, Matching Vectors, Performance Metrics
# -----------------------------------------------------------------------------
resource "databricks_schema" "gold" {
  count        = var.enable_unity_catalog ? 1 : 0
  catalog_name = var.catalog_name
  name         = "${local.schema_prefix}_gold"
  comment      = "Production gold layer with neural embeddings, compatibility scorecards, and reporting tables (${var.environment})"

  properties = {
    "delta.autoOptimize.optimizeWrite" = "true"
    "delta.autoOptimize.autoCompact"   = "true"
    "layer"                            = "gold"
    "project"                          = "foryourservice"
  }
}
