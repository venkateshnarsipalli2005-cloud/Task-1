"""
Feature Engineering Module
Create advanced time series features for sales forecasting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import linregress
import logging

logger = logging.getLogger(__name__)


class TimeSeriesFeatureEngineer:
    """Generate advanced time series features"""
    
    def __init__(self, df, date_col='date', target_col='sales'):
        """
        Initialize feature engineer
        
        Args:
            df (DataFrame): Input data with date and target columns
            date_col (str): Name of date column
            target_col (str): Name of target variable column
        """
        self.df = df.copy()
        self.date_col = date_col
        self.target_col = target_col
        self.features = None
    
    def create_time_features(self):
        """Extract time-based features"""
        df = self.df.copy()
        
        # Ensure date is datetime
        df[self.date_col] = pd.to_datetime(df[self.date_col])
        
        # Basic time features
        df['year'] = df[self.date_col].dt.year
        df['month'] = df[self.date_col].dt.month
        df['day'] = df[self.date_col].dt.day
        df['day_of_week'] = df[self.date_col].dt.dayofweek
        df['day_of_year'] = df[self.date_col].dt.dayofyear
        df['quarter'] = df[self.date_col].dt.quarter
        df['week_of_year'] = df[self.date_col].dt.isocalendar().week
        
        # Boolean features
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_month_start'] = df[self.date_col].dt.is_month_start.astype(int)
        df['is_month_end'] = df[self.date_col].dt.is_month_end.astype(int)
        df['is_quarter_start'] = df[self.date_col].dt.is_quarter_start.astype(int)
        df['is_quarter_end'] = df[self.date_col].dt.is_quarter_end.astype(int)
        df['is_year_start'] = df[self.date_col].dt.is_year_start.astype(int)
        df['is_year_end'] = df[self.date_col].dt.is_year_end.astype(int)
        
        logger.info(f"✓ Created time-based features ({len(df.columns) - len(self.df.columns)} new)")
        self.df = df
        return df
    
    def create_rolling_features(self, windows=[7, 14, 30, 90, 365]):
        """Create rolling window aggregations"""
        df = self.df.copy()
        
        for window in windows:
            df[f'rolling_mean_{window}'] = df[self.target_col].rolling(window, min_periods=1).mean()
            df[f'rolling_std_{window}'] = df[self.target_col].rolling(window, min_periods=1).std()
            df[f'rolling_min_{window}'] = df[self.target_col].rolling(window, min_periods=1).min()
            df[f'rolling_max_{window}'] = df[self.target_col].rolling(window, min_periods=1).max()
        
        logger.info(f"✓ Created rolling window features for windows: {windows}")
        self.df = df
        return df
    
    def create_lag_features(self, lags=[1, 7, 14, 30, 365]):
        """Create lag features"""
        df = self.df.copy()
        
        for lag in lags:
            df[f'lag_{lag}'] = df[self.target_col].shift(lag)
        
        # Rate of change
        df['diff_1'] = df[self.target_col].diff(1)
        df['diff_7'] = df[self.target_col].diff(7)
        df['diff_30'] = df[self.target_col].diff(30)
        
        # Percentage change
        df['pct_change_1'] = df[self.target_col].pct_change(1)
        df['pct_change_7'] = df[self.target_col].pct_change(7)
        
        logger.info(f"✓ Created lag features for lags: {lags}")
        self.df = df
        return df
    
    def create_seasonal_features(self):
        """Create seasonality indicators"""
        df = self.df.copy()
        
        # Monthly seasonality
        monthly_avg = df.groupby('month')[self.target_col].mean().to_dict()
        df['monthly_avg'] = df['month'].map(monthly_avg)
        df['monthly_seasonality'] = df[self.target_col] / (df['monthly_avg'] + 1e-6)
        
        # Day-of-week seasonality
        dow_avg = df.groupby('day_of_week')[self.target_col].mean().to_dict()
        df['dow_avg'] = df['day_of_week'].map(dow_avg)
        df['dow_seasonality'] = df[self.target_col] / (df['dow_avg'] + 1e-6)
        
        # Quarter seasonality
        quarter_avg = df.groupby('quarter')[self.target_col].mean().to_dict()
        df['quarter_avg'] = df['quarter'].map(quarter_avg)
        df['quarter_seasonality'] = df[self.target_col] / (df['quarter_avg'] + 1e-6)
        
        logger.info("✓ Created seasonal features")
        self.df = df
        return df
    
    def create_holiday_features(self, holidays=None):
        """Create holiday flags"""
        if holidays is None:
            holidays = {
                'new_year': (1, 1),
                'valentine_day': (2, 14),
                'independence_day': (7, 4),
                'black_friday': (11, 27),
                'cyber_monday': (11, 30),
                'christmas': (12, 25),
                'boxing_day': (12, 26),
            }
        
        df = self.df.copy()
        
        for holiday_name, (month, day) in holidays.items():
            df[f'is_{holiday_name}'] = ((df['month'] == month) & (df['day'] == day)).astype(int)
        
        logger.info(f"✓ Created {len(holidays)} holiday features")
        self.df = df
        return df
    
    def create_trend_features(self):
        """Create trend indicators"""
        df = self.df.copy()
        
        def calc_trend(series, window=30):
            trends = []
            for i in range(len(series)):
                if i < window:
                    x = np.arange(i + 1)
                    y = series.iloc[:i+1].values
                else:
                    x = np.arange(window)
                    y = series.iloc[i-window+1:i+1].values
                
                if len(x) > 1:
                    slope, _, _, _, _ = linregress(x, y)
                    trends.append(slope)
                else:
                    trends.append(0)
            
            return pd.Series(trends, index=series.index)
        
        df['trend_7'] = calc_trend(df[self.target_col], window=7)
        df['trend_30'] = calc_trend(df[self.target_col], window=30)
        df['trend_90'] = calc_trend(df[self.target_col], window=90)
        
        logger.info("✓ Created trend features")
        self.df = df
        return df
    
    def handle_missing_values(self):
        """Fill missing values created by feature engineering"""
        df = self.df.copy()
        
        # Forward fill then backward fill
        df = df.fillna(method='bfill').fillna(method='ffill').fillna(0)
        
        missing_count = df.isnull().sum().sum()
        logger.info(f"✓ Handled missing values (remaining: {missing_count})")
        
        self.df = df
        return df
    
    def get_features(self):
        """Get engineered feature dataframe"""
        return self.df
    
    def engineer_all_features(self):
        """Execute complete feature engineering pipeline"""
        logger.info("Starting feature engineering...")
        
        self.create_time_features()
        self.create_rolling_features()
        self.create_lag_features()
        self.create_seasonal_features()
        self.create_holiday_features()
        self.create_trend_features()
        self.handle_missing_values()
        
        logger.info(f"✓ Feature engineering complete!")
        logger.info(f"  Original features: {len(self.df.columns)}")
        logger.info(f"  Final features: {len(self.df.columns)}")
        
        return self.df


def create_features_from_raw(input_path, output_path):
    """
    Load raw data and create all features
    
    Args:
        input_path (str): Path to raw CSV
        output_path (str): Path to save engineered features
    """
    # Load data
    df = pd.read_csv(input_path)
    
    # Identify columns
    date_col = [col for col in df.columns if 'date' in col.lower()][0]
    sales_col = [col for col in df.columns if 'sales' in col.lower()][0]
    
    # Create daily aggregation
    daily_df = df.groupby(date_col)[sales_col].sum().reset_index()
    daily_df.columns = ['date', 'sales']
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    daily_df = daily_df.sort_values('date')
    
    # Engineer features
    engineer = TimeSeriesFeatureEngineer(daily_df, date_col='date', target_col='sales')
    engineered = engineer.engineer_all_features()
    
    # Save
    engineered.to_csv(output_path, index=False)
    logger.info(f"✓ Saved engineered features to {output_path}")
    
    return engineered


if __name__ == '__main__':
    # Example usage
    from data_loader import load_sample_data
    
    # Create sample data
    df = load_sample_data()
    
    # Engineer features
    engineer = TimeSeriesFeatureEngineer(df, date_col='OrderDate', target_col='Sales')
    engineered = engineer.engineer_all_features()
    
    print(f"\nEngineered features shape: {engineered.shape}")
    print(f"\nSample of engineered data:")
    print(engineered.head())
