# Getting Started Guide - Retail Sales Forecasting Project

## 🚀 Quick Start (5 Steps)

### Step 1: Set Up Environment

#### Windows PowerShell
```powershell
# Navigate to project directory
cd "C:\Users\venka\OneDrive\ドキュメント\GitHub\task-1"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### macOS/Linux
```bash
# Navigate to project directory
cd ~/path/to/task-1

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Prepare Data

#### Option A: Use Sample Data
```bash
python scripts/data_loader.py
# This creates sample_sales_data.csv in data/raw/
```

#### Option B: Use Your Own Data
1. Download dataset from:
   - [Superstore Sales (Kaggle)](https://www.kaggle.com/rohitsahoo/sales-forecasting)
   - [Retail Sales Forecasting (Kaggle)](https://www.kaggle.com/datasets/manjeetsingh/retail-sales-forecasting)
   - [Rossmann Store Sales (Kaggle)](https://www.kaggle.com/c/rossmann-store-sales)

2. Place CSV file in `data/raw/` folder

3. Ensure your CSV has columns:
   - Date column (any name with "date")
   - Sales/Revenue column (any name with "sales" or "amount")

### Step 3: Run Analysis Notebooks

Open Jupyter and run notebooks in order:

```bash
jupyter notebook
```

Then open and run:
1. **01_data_exploration.ipynb** - EDA & data validation
2. **02_feature_engineering.ipynb** - Create time series features
3. **03_model_training.ipynb** - Train & compare models
4. **04_forecasting_analysis.ipynb** - Generate forecasts & insights

**Or run via Python:**
```bash
# Run entire pipeline
python scripts/forecast_pipeline.py
```

### Step 4: Generate Power BI Data

The pipeline automatically creates:
- `outputs/powerbi_data.csv` - Combined historical + forecast
- `outputs/analysis_summary_report.json` - Key insights

These are ready to import into Power BI!

### Step 5: Build Power BI Dashboard

1. Open Power BI Desktop
2. Import `outputs/powerbi_data.csv`
3. Follow [POWERBI_GUIDE.md](POWERBI_GUIDE.md) for visualization steps

---

## 📊 Project Workflow

```
┌─────────────────────────────────────┐
│  1. LOAD & EXPLORE                  │
│  - data_exploration.ipynb           │
│  - Identify trends & seasonality    │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  2. FEATURE ENGINEERING             │
│  - feature_engineering.ipynb        │
│  - Create 50+ time series features  │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  3. MODEL TRAINING                  │
│  - model_training.ipynb             │
│  - Train Prophet, ARIMA, XGBoost    │
│  - Evaluate & compare models        │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  4. FORECASTING & INSIGHTS          │
│  - forecasting_analysis.ipynb       │
│  - Generate 12-month forecasts      │
│  - Extract business insights        │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  5. POWER BI DASHBOARD              │
│  - Import powerbi_data.csv          │
│  - Build interactive visualizations │
│  - Share insights with stakeholders │
└─────────────────────────────────────┘
```

---

## 📁 Project Structure

```
task-1/
├── notebooks/
│   ├── 01_data_exploration.ipynb         ← Start here
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_forecasting_analysis.ipynb
├── scripts/
│   ├── data_loader.py                    # Load & validate data
│   ├── feature_engineer.py               # Create features
│   └── forecast_pipeline.py              # Complete pipeline
├── data/
│   ├── raw/                              # Your raw CSV files
│   └── processed/                        # Engineered features
├── outputs/
│   ├── powerbi_data.csv                  # For Power BI import
│   ├── analysis_summary_report.json      # Key insights
│   ├── test_predictions.csv              # Model predictions
│   └── *.png                             # Generated charts
├── dashboards/                           # Power BI files
├── requirements.txt                      # Python dependencies
└── README.md                             # Project overview
```

---

## 🔧 Installation Troubleshooting

### Issue: Prophet Installation Error

**Solution:**
```bash
# Uninstall existing Prophet
pip uninstall pystan fbprophet

# Install specific versions
pip install pystan==2.19.1.1
pip install fbprophet
```

### Issue: XGBoost Not Working

**Solution:**
```bash
# Upgrade scikit-learn and XGBoost
pip install --upgrade scikit-learn xgboost
```

### Issue: Jupyter Not Found

**Solution:**
```bash
pip install jupyter notebook ipykernel
python -m ipykernel install --user
```

---

## 📊 Expected Outputs

After running all notebooks, you'll have:

### CSV Files
- ✅ `engineered_features.csv` - Features for modeling
- ✅ `test_predictions.csv` - Model predictions vs actuals
- ✅ `powerbi_data.csv` - Historical + forecast (for Power BI)

### JSON Files
- ✅ `model_comparison_results.json` - Model metrics (MAE, RMSE, R²)
- ✅ `analysis_summary_report.json` - Executive summary

### PNG Charts
- ✅ `01_sales_overview.png` - Historical sales analysis
- ✅ `02_seasonality_analysis.png` - Seasonal patterns
- ✅ `03_feature_engineering.png` - Feature distributions
- ✅ `04_train_test_split.png` - Data split visualization
- ✅ `05_model_predictions.png` - Model performance
- ✅ `06_model_comparison.png` - Model metrics comparison
- ✅ `07_feature_importance.png` - Top features (XGBoost)
- ✅ `08_forecast_visualization.png` - 12-month forecast

---

## 💡 Key Metrics Explained

### Forecasting Models

| Metric | Range | Interpretation |
|--------|-------|-----------------|
| **MAE** | $0+ | Avg error in dollars. Lower is better. |
| **RMSE** | $0+ | Penalizes large errors more. |
| **MAPE** | 0-100% | Percentage error. <10% = Excellent |
| **R²** | 0-1 | Variance explained. >0.8 = Strong |

### Seasonality Indicators

| Indicator | Meaning |
|-----------|---------|
| **Seasonal Strength** | How much sales vary by season |
| **Peak Month** | Highest average sales month |
| **Low Month** | Lowest average sales month |
| **Trend** | Overall growth/decline direction |

---

## 🎯 Business Use Cases

### Inventory Management
- Forecast demand by month
- Adjust stock levels based on seasonal patterns
- Plan procurement schedules

### Sales Planning
- Set realistic monthly targets
- Identify high-opportunity periods
- Allocate marketing budget

### Resource Planning
- Staff scheduling based on demand
- Warehouse capacity planning
- Supply chain optimization

### Financial Planning
- Revenue forecasting
- Budget allocation
- Margin projections

---

## 📚 Learning Resources

### Time Series Forecasting
- [Prophet Documentation](https://facebook.github.io/prophet/)
- [ARIMA Guide](https://www.statsmodels.org/stable/tsa_arima.html)
- [XGBoost Time Series](https://xgboost.readthedocs.io/)

### Power BI
- [Power BI Desktop Tutorials](https://docs.microsoft.com/power-bi/fundamentals/)
- [DAX Language Reference](https://dax.guide/)
- [Power BI Best Practices](https://docs.microsoft.com/power-bi/guidance/)

### Data Science
- [Kaggle Forecasting Competitions](https://www.kaggle.com/c/m5-forecasting-accuracy)
- [Time Series Analysis with Python](https://www.datacamp.com/courses/time-series-analysis-in-python)

---

## ✅ Checklist

- [ ] Created virtual environment
- [ ] Installed dependencies
- [ ] Placed data in `data/raw/`
- [ ] Ran data exploration notebook
- [ ] Ran feature engineering notebook
- [ ] Ran model training notebook
- [ ] Ran forecasting analysis notebook
- [ ] Verified `outputs/powerbi_data.csv` exists
- [ ] Opened Power BI Desktop
- [ ] Imported powerbi_data.csv
- [ ] Created visualizations following POWERBI_GUIDE.md
- [ ] Reviewed business insights

---

## 🆘 Getting Help

1. **Check error messages** - They usually tell you what's wrong
2. **Review documentation** - POWERBI_GUIDE.md and README.md
3. **Verify data format** - Ensure CSV has proper date & sales columns
4. **Check dependencies** - Run `pip list` to verify installations
5. **Review logs** - Notebooks print detailed progress messages

---

## 🎓 Next Steps After Completion

1. **Enhance Models**
   - Try different hyperparameters
   - Add external regressors (holidays, events)
   - Implement ensemble methods

2. **Expand Dashboard**
   - Add advanced visuals (maps, matrices)
   - Create role-based views
   - Implement RLS for multi-user access

3. **Deploy Solution**
   - Publish to Power BI Service
   - Set up automated refresh
   - Create mobile app views

4. **Extend Analysis**
   - Add segment-level forecasting
   - Implement anomaly detection
   - Create what-if scenarios

---

**Start with Step 1 and follow through all 5 steps in the Quick Start section!**

Good luck with your forecasting project! 🚀
