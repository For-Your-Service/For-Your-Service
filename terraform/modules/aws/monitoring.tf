# File: terraform/modules/aws/monitoring.tf
# Description: AWS Free Tier Zero-Spend Budget Alerts and Monitoring
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# AWS Budgets Zero-Spend / Free Tier Limit Alert
# -----------------------------------------------------------------------------
resource "aws_budgets_budget" "zero_spend_budget" {
  count             = var.enable_budget_alert ? 1 : 0
  name              = "${var.project_name}-free-tier-budget-${var.environment}"
  budget_type       = "COST"
  limit_amount      = "5.0"
  limit_unit        = "USD"
  time_unit         = "MONTHLY"
  time_period_start = "2026-01-01_00:00"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.owner_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.owner_email]
  }
}
