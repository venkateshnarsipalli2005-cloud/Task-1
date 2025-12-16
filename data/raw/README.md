# Place raw sales data files here

## Supported Formats
- `.csv` - Comma-separated values (recommended)
- `.xlsx` - Excel workbooks
- `.parquet` - Apache Parquet format

## Data Requirements
Your CSV should contain at minimum:
- **Date column** (any name with "date" or "time")
- **Sales column** (any name with "sales", "amount", or "revenue")

## Example Format
```
OrderDate,Sales,Quantity,Category
2020-01-01,1500.00,10,Electronics
2020-01-02,2100.50,15,Clothing
...
```

## Sample Datasets
Download from:
1. [Superstore Sales (Kaggle)](https://www.kaggle.com/rohitsahoo/sales-forecasting)
2. [Retail Sales Forecasting (Kaggle)](https://www.kaggle.com/datasets/manjeetsingh/retail-sales-forecasting)
3. [Rossmann Store Sales (Kaggle)](https://www.kaggle.com/c/rossmann-store-sales)

## Quick Start
```bash
# Generate sample data
python scripts/data_loader.py
```

This creates `sample_sales_data.csv` automatically.
