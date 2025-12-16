# Power BI Dashboards

This directory contains Power BI dashboard files.

## Files

### sales_forecast.pbix
- Main interactive dashboard
- Contains all visualizations and analysis
- Import data from: `/outputs/powerbi_data.csv`
- Refresh schedule: Daily (configurable)

## Creating Your Dashboard

### Steps:
1. Open Power BI Desktop
2. Import `/outputs/powerbi_data.csv`
3. Follow `/POWERBI_GUIDE.md` for visualizations
4. Save as `sales_forecast.pbix` in this folder
5. Publish to Power BI Service

### Key Visualizations to Create:
- KPI Cards (total sales, forecast, growth %)
- Time series line chart (historical + forecast)
- Monthly breakdown by category
- Seasonal patterns (monthly, quarterly, day-of-week)
- Model performance metrics
- Key insights & recommendations

### Power BI Features to Use:
- Interactive slicers (date range, year, month)
- Drill-through for detailed analysis
- Tooltips for additional context
- Bookmarks for navigation
- Conditional formatting for highlights

## Publishing to Power BI Service

1. File → Publish
2. Select workspace
3. Configure data refresh schedule
4. Share with stakeholders
5. Set up mobile-optimized view

See `/POWERBI_GUIDE.md` for complete instructions.
