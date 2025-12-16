# Project Configuration

## Data Configuration
DATA_RAW_PATH = "data/raw"
DATA_PROCESSED_PATH = "data/processed"
OUTPUTS_PATH = "outputs"

## Time Series Parameters
# Forecast horizon (days)
FORECAST_PERIODS = 365

# Train-test split ratio
TEST_SPLIT_RATIO = 0.2

# Rolling window sizes for features
ROLLING_WINDOWS = [7, 14, 30, 90, 365]

# Lag periods for features
LAG_PERIODS = [1, 7, 14, 30, 365]

## Model Parameters

### Prophet Configuration
PROPHET_CONFIG = {
    "yearly_seasonality": True,
    "weekly_seasonality": True,
    "daily_seasonality": False,
    "changepoint_prior_scale": 0.05,
    "seasonality_prior_scale": 10,
    "interval_width": 0.95,
}

### ARIMA Configuration
ARIMA_ORDER = (5, 1, 2)  # (p, d, q)

### XGBoost Configuration
XGBOOST_CONFIG = {
    "n_estimators": 100,
    "max_depth": 6,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42,
}

## Holiday Configuration
HOLIDAYS = {
    "new_year": (1, 1),
    "valentine_day": (2, 14),
    "independence_day": (7, 4),
    "black_friday": (11, 27),
    "cyber_monday": (11, 30),
    "christmas": (12, 25),
    "boxing_day": (12, 26),
}

## Visualization Parameters
FIGURE_SIZE = (14, 6)
DPI = 300
STYLE = "whitegrid"

# Color Scheme
COLORS = {
    "historical": "#4472C4",  # Steel Blue
    "forecast": "#FFA500",     # Orange
    "positive": "#70AD47",     # Green
    "negative": "#C5504C",     # Red
    "background": "#F2F2F2",   # Light Gray
}

## Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

## Feature Engineering
# Date-based features to create
TIME_FEATURES = [
    "year", "month", "day", "day_of_week",
    "day_of_year", "quarter", "week_of_year"
]

# Boolean features to create
BOOLEAN_FEATURES = [
    "is_weekend", "is_month_start", "is_month_end",
    "is_quarter_start", "is_quarter_end",
    "is_year_start", "is_year_end"
]

## Performance Thresholds
MIN_R2_SCORE = 0.6
MAX_MAPE = 0.25  # 25%
TARGET_RMSE_PERCENT = 0.15  # 15% of mean

## Data Quality
MAX_MISSING_PERCENT = 50  # Alert if > 50% missing
MIN_DATA_POINTS = 365  # Require at least 1 year of data
