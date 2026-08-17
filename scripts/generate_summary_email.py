#!/usr/bin/env python3
"""Generate daily summary email for operations team"""

from datetime import datetime


def generate_summary_html(spark):
    """Generate HTML email summary"""

    # Yesterday's stats
    stats_df = spark.sql("""
        SELECT 
          source,
          COUNT(*) as job_count,
          COUNT(DISTINCT company) as companies,
          AVG(salary.min) as avg_salary
        FROM workspace.fys_bronze.job_postings
        WHERE scrape_date = CURRENT_DATE - INTERVAL 1 DAYS
        GROUP BY source
    """)

    stats = stats_df.collect()

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            .summary {{ background-color: #f2f2f2; padding: 15px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>For Your Service - Daily Ingestion Summary</h1>
        <div class="summary">
            <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
            <p><strong>Status:</strong> ✅ Successful</p>
            <p><strong>Total Jobs:</strong> {sum(row['job_count'] for row in stats)}</p>
        </div>
        
        <h2>Per-Source Breakdown</h2>
        <table>
            <tr>
                <th>Source</th>
                <th>Jobs</th>
                <th>Companies</th>
                <th>Avg Salary</th>
            </tr>
    """

    for row in stats:
        html += f"""
            <tr>
                <td>{row['source']}</td>
                <td>{row['job_count']}</td>
                <td>{row['companies']}</td>
                <td>${int(row['avg_salary']):,}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    print("Summary Email Generator")
    print("Run: generate_summary_html(spark)")
