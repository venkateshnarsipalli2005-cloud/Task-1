# Power BI Dashboard Setup Guide

## Overview

This guide explains how to build an interactive Power BI dashboard using the forecasted sales data from this project.

## Prerequisites

- Power BI Desktop (latest version recommended)
- Data file: `outputs/powerbi_data.csv`
- Forecast output: `outputs/analysis_summary_report.json`

## Step 1: Load Data into Power BI

### 1.1 Open Power BI Desktop
1. Launch Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Navigate to `outputs/powerbi_data.csv`
4. Click "Load"

### 1.2 Transform Data
1. In Power Query Editor:
   - Ensure "date" column is formatted as Date
   - Ensure "sales" column is formatted as Decimal
   - Set "data_type" as text category
2. Click "Close & Apply"

## Step 2: Create Data Model

### 2.1 Add Calendar Table (Recommended)
```
Calendar = 
CALENDAR(
    MIN('powerbi_data'[date]),
    MAX('powerbi_data'[date])
)
```

### 2.2 Create Relationships
1. Create relationship between:
   - `powerbi_data[date]` → `Calendar[Date]`
   - Set as "One-to-Many"

## Step 3: Build Visualizations

### 3.1 KPI Cards (Page 1: Overview)

**Total Sales (Historical)**
```
Total Sales = SUM(powerbi_data[sales])
WHERE powerbi_data[data_type] = "Historical"
```

**12-Month Forecast**
```
Total Forecast = SUM(powerbi_data[sales])
WHERE powerbi_data[data_type] = "Forecast"
```

**Expected Growth**
```
Expected Growth % = 
DIVIDE(
    [Total Forecast] - [Total Sales],
    [Total Sales]
)
```

### 3.2 Time Series Line Chart (Page 1: Main Visual)

1. Add Line Chart visual
2. Axes:
   - X-axis: date
   - Y-axis: sales
3. Legend:
   - data_type (Historical vs Forecast)
4. Formatting:
   - Enable data labels
   - Set line width to 2
   - Use distinct colors: Blue for Historical, Orange for Forecast

### 3.3 Confidence Interval Chart (Page 2: Forecast Details)

1. Add Area Chart
2. Axes:
   - X-axis: date
   - Y-axis: sales
3. Add fields for:
   - forecast_lower
   - forecast_upper
4. Apply blue transparency to confidence band

### 3.4 Monthly Breakdown (Page 2)

1. Add Column Chart
2. Axes:
   - Category: month_name
   - Value: sum(sales)
3. Add slicer for year

### 3.5 Seasonal Analysis (Page 3: Insights)

Create these visualizations:

**By Month**
```
Monthly Analysis = 
SUMMARIZECOLUMNS(
    powerbi_data[month_name],
    "Avg Sales", AVERAGE(powerbi_data[sales])
)
```

**By Day of Week**
```
Day of Week Analysis = 
SUMMARIZECOLUMNS(
    powerbi_data[day_of_week],
    "Avg Sales", AVERAGE(powerbi_data[sales])
)
```

**By Quarter**
```
Quarterly Analysis = 
SUMMARIZECOLUMNS(
    powerbi_data[quarter],
    "Total Sales", SUM(powerbi_data[sales])
)
```

## Step 4: Add Interactive Elements

### 4.1 Slicers
Add the following slicers:
1. **Date Range** - Date slicer for filtering by period
2. **Year** - Filter by year
3. **Data Type** - Toggle between Historical/Forecast
4. **Quarter** - Filter by quarter

### 4.2 Buttons
Create navigation buttons:
1. "Overview" - Navigate to Page 1
2. "Forecast" - Navigate to Page 2
3. "Insights" - Navigate to Page 3
4. "Refresh Data" - Refresh to latest data

## Step 5: Create Report Pages

### Page 1: Overview & Trends
- Title: "Sales Overview & 12-Month Forecast"
- KPI Cards (top):
  - Total Historical Sales
  - Total 12-Month Forecast
  - Expected Growth %
  - Average Daily Sales
- Main Chart: Time series line chart (Historical + Forecast)
- Secondary: Year-to-date comparison

### Page 2: Forecast Details
- Confidence Interval Chart
- Monthly Breakdown
- Key Metrics Table:
  - Peak Month (Forecast)
  - Low Month (Forecast)
  - Forecast Average

### Page 3: Seasonal Insights
- Monthly Pattern (Bar Chart)
- Day-of-Week Performance (Column Chart)
- Quarterly Trends (Line Chart)
- Anomalies/Outliers Table

### Page 4: Key Findings & Recommendations
- Text boxes with key insights from `analysis_summary_report.json`
- Bullet list of strategic recommendations
- Model performance metrics
- Data quality summary

## Step 6: Formatting & Design

### Color Scheme
- **Historical Data**: Steel Blue (#4472C4)
- **Forecast Data**: Coral/Orange (#FFA500)
- **Positive Trend**: Green (#70AD47)
- **Negative Trend**: Red (#C5504C)
- **Background**: Light Gray (#F2F2F2)

### Typography
- Title: Bold, 18pt
- Subtitle: Regular, 14pt
- Labels: Regular, 11pt
- KPI Values: Bold, 16pt

### Layout
- 16:9 aspect ratio
- Consistent margins (20px)
- Aligned grid layout
- Clear visual hierarchy

## Step 7: Advanced Features

### 7.1 Tooltips
Add custom tooltips showing:
```
Date: [date]
Sales: $[sales:0,]
Type: [data_type]
Confidence: ±[forecast_upper - forecast_lower]
```

### 7.2 Drill-Through Pages
- Create drill-through from months to daily data
- Enable drill-through on any date field

### 7.3 What-If Analysis (Optional)
Add parameter for sensitivity analysis:
```
Growth Factor = PARAMETER(
    Default Value: 1.0,
    Min: 0.8,
    Max: 1.2,
    Step: 0.1
)
```

### 7.4 Automatic Refresh
1. Go to File → Options
2. Enable "Refresh data"
3. Set to refresh daily at specific time
4. Connect to data source for auto-update

## Step 8: Publish & Share

### 8.1 Save Report
1. File → Save
2. Save as: `sales_forecast_dashboard.pbix`
3. Location: `dashboards/` folder

### 8.2 Publish to Power BI Service
1. File → Publish
2. Select workspace
3. Configure refresh schedule
4. Set up alerts for forecasted values

### 8.3 Share with Stakeholders
1. Share report via Power BI Service
2. Create mobile-optimized version
3. Set row-level security (RLS) if needed

## DAX Formulas Reference

### Measures
```
# Total Sales Historical
Total Sales Historical = 
CALCULATE(
    SUM(powerbi_data[sales]),
    powerbi_data[data_type] = "Historical"
)

# Average Daily Sales
Avg Daily Sales = 
AVERAGEX(
    CALENDAR(MIN(powerbi_data[date]), MAX(powerbi_data[date])),
    CALCULATE(SUM(powerbi_data[sales]))
)

# Year-over-Year Growth
YoY Growth = 
DIVIDE(
    CALCULATE(SUM(powerbi_data[sales]), YEAR(powerbi_data[date]) = YEAR(TODAY())),
    CALCULATE(SUM(powerbi_data[sales]), YEAR(powerbi_data[date]) = YEAR(TODAY()) - 1)
) - 1

# Forecast Accuracy (if actual data available)
Forecast Accuracy = 
IF(
    HASONEVALUE(powerbi_data[data_type]),
    1 - DIVIDE(
        ABS(SUM(powerbi_data[sales]) - [Actual Sales]),
        [Actual Sales]
    ),
    BLANK()
)
```

## Common Issues & Solutions

### Issue: Data not loading
**Solution**: Check CSV formatting, ensure date format is recognized

### Issue: Slow performance
**Solution**: Create aggregated tables for large datasets, optimize queries

### Issue: Forecast not showing
**Solution**: Verify data_type field contains "Forecast", check date range

### Issue: Formatting lost after refresh
**Solution**: Save custom formatting in Power BI theme file

## Next Steps

1. ✅ Load data into Power BI
2. ✅ Create basic visualizations
3. ✅ Add interactivity with slicers
4. ✅ Format and design dashboard
5. ✅ Add advanced features
6. ✅ Publish to Power BI Service
7. ✅ Set up automatic refresh schedule

## Resources

- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [DAX Function Reference](https://dax.guide/)
- [Power BI Best Practices](https://docs.microsoft.com/power-bi/guidance/)

---

**Dashboard Version**: 1.0  
**Last Updated**: December 2025  
**Data Source**: Sales Forecasting Pipeline
