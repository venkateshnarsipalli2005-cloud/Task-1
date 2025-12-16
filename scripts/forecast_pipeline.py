"""
Forecast Pipeline Module
End-to-end forecasting workflow for retail sales prediction
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging

from fbprophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error, r2_score
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ForecastPipeline:
    """Complete forecasting pipeline"""
    
    def __init__(self, data_path, output_path='../outputs'):
        """
        Initialize pipeline
        
        Args:
            data_path (str): Path to processed features CSV
            output_path (str): Path to save outputs
        """
        self.data_path = Path(data_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(exist_ok=True)
        
        self.df = None
        self.df_train = None
        self.df_test = None
        self.models = {}
        self.predictions = {}
        self.forecast = None
    
    def load_data(self):
        """Load engineered features"""
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date').reset_index(drop=True)
        
        logger.info(f"✓ Loaded data: {len(self.df)} rows, {len(self.df.columns)} columns")
        return self.df
    
    def train_test_split(self, test_ratio=0.2):
        """Split data into train/test sets"""
        split_date = self.df['date'].quantile(test_ratio)
        self.df_train = self.df[self.df['date'] <= split_date].reset_index(drop=True)
        self.df_test = self.df[self.df['date'] > split_date].reset_index(drop=True)
        
        logger.info(f"✓ Train: {len(self.df_train)} | Test: {len(self.df_test)}")
        return self.df_train, self.df_test
    
    def train_prophet(self):
        """Train Prophet model"""
        try:
            prophet_train = self.df_train[['date', 'sales']].copy()
            prophet_train.columns = ['ds', 'y']
            
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                interval_width=0.95
            )
            
            model.fit(prophet_train)
            
            # Predict on test
            future = model.make_future_dataframe(periods=len(self.df_test))
            forecast = model.predict(future)
            test_predictions = forecast.iloc[-len(self.df_test):]['yhat'].values
            
            self.models['Prophet'] = model
            self.predictions['Prophet'] = test_predictions
            
            logger.info("✓ Prophet model trained")
            return model, test_predictions
        except Exception as e:
            logger.error(f"✗ Prophet error: {str(e)}")
            return None, None
    
    def train_arima(self, order=(5, 1, 2)):
        """Train ARIMA model"""
        try:
            model = ARIMA(self.df_train['sales'], order=order)
            result = model.fit()
            
            # Predict on test
            test_predictions = result.get_forecast(steps=len(self.df_test)).predicted_mean.values
            test_predictions = np.maximum(test_predictions, 0)  # Ensure positive
            
            self.models['ARIMA'] = result
            self.predictions['ARIMA'] = test_predictions
            
            logger.info("✓ ARIMA model trained")
            return result, test_predictions
        except Exception as e:
            logger.error(f"✗ ARIMA error: {str(e)}")
            return None, None
    
    def train_xgboost(self):
        """Train XGBoost model"""
        try:
            feature_cols = [col for col in self.df_train.columns 
                           if col not in ['date', 'sales']]
            
            X_train = self.df_train[feature_cols].fillna(0)
            y_train = self.df_train['sales']
            X_test = self.df_test[feature_cols].fillna(0)
            
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            model = XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )
            
            model.fit(X_train_scaled, y_train, verbose=False)
            test_predictions = model.predict(X_test_scaled)
            
            self.models['XGBoost'] = (model, scaler, feature_cols)
            self.predictions['XGBoost'] = test_predictions
            
            logger.info("✓ XGBoost model trained")
            return model, test_predictions
        except Exception as e:
            logger.error(f"✗ XGBoost error: {str(e)}")
            return None, None
    
    def evaluate_models(self):
        """Evaluate all models"""
        results = []
        
        for model_name, predictions in self.predictions.items():
            mae = mean_absolute_error(self.df_test['sales'], predictions)
            rmse = np.sqrt(mean_squared_error(self.df_test['sales'], predictions))
            mape = mean_absolute_percentage_error(self.df_test['sales'], predictions)
            r2 = r2_score(self.df_test['sales'], predictions)
            
            results.append({
                'Model': model_name,
                'MAE': float(mae),
                'RMSE': float(rmse),
                'MAPE': float(mape),
                'R²': float(r2)
            })
            
            logger.info(f"{model_name} | MAE: ${mae:.2f} | R²: {r2:.4f}")
        
        self.results_df = pd.DataFrame(results)
        return self.results_df
    
    def generate_forecast(self, periods=365):
        """Generate future forecasts"""
        try:
            # Use best model (Prophet)
            if 'Prophet' in self.models:
                model = self.models['Prophet']
                future_dates = model.make_future_dataframe(periods=periods)
                forecast = model.predict(future_dates)
                
                forecast_future = forecast[forecast['ds'] > self.df['date'].max()][
                    ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
                ].copy()
                
                forecast_future.columns = ['date', 'forecast', 'forecast_lower', 'forecast_upper']
                forecast_future['forecast'] = forecast_future['forecast'].clip(lower=0)
                forecast_future['forecast_lower'] = forecast_future['forecast_lower'].clip(lower=0)
                forecast_future['forecast_upper'] = forecast_future['forecast_upper'].clip(lower=0)
                
                self.forecast = forecast_future
                logger.info(f"✓ Generated {len(forecast_future)} days of forecasts")
                return forecast_future
        except Exception as e:
            logger.error(f"✗ Forecast error: {str(e)}")
            return None
    
    def save_results(self):
        """Save all results to files"""
        # Save model comparison
        if hasattr(self, 'results_df'):
            self.results_df.to_json(
                self.output_path / 'model_comparison_results.json',
                orient='records'
            )
            logger.info("✓ Saved model comparison results")
        
        # Save predictions
        predictions_df = pd.DataFrame({
            'date': self.df_test['date'],
            'actual_sales': self.df_test['sales']
        })
        
        for model_name, preds in self.predictions.items():
            predictions_df[f'{model_name.lower()}_pred'] = preds
        
        predictions_df.to_csv(self.output_path / 'test_predictions.csv', index=False)
        logger.info("✓ Saved test predictions")
        
        # Save forecast
        if self.forecast is not None:
            # Combine with historical for Power BI
            historical = pd.DataFrame({
                'date': self.df['date'],
                'sales': self.df['sales'],
                'data_type': 'Historical',
                'forecast_lower': np.nan,
                'forecast_upper': np.nan
            })
            
            forecast_data = self.forecast.copy()
            forecast_data['data_type'] = 'Forecast'
            forecast_data['sales'] = forecast_data['forecast']
            forecast_data = forecast_data[['date', 'sales', 'data_type', 'forecast_lower', 'forecast_upper']]
            
            combined = pd.concat([historical, forecast_data], ignore_index=True)
            combined.to_csv(self.output_path / 'powerbi_data.csv', index=False)
            logger.info("✓ Saved Power BI data")
    
    def run_pipeline(self):
        """Execute complete pipeline"""
        logger.info("="*60)
        logger.info("Starting Forecasting Pipeline")
        logger.info("="*60)
        
        self.load_data()
        self.train_test_split()
        
        logger.info("\nTraining models...")
        self.train_prophet()
        self.train_arima()
        self.train_xgboost()
        
        logger.info("\nEvaluating models...")
        self.evaluate_models()
        
        logger.info("\nGenerating forecasts...")
        self.generate_forecast()
        
        logger.info("\nSaving results...")
        self.save_results()
        
        logger.info("="*60)
        logger.info("✓ Pipeline complete!")
        logger.info("="*60)


if __name__ == '__main__':
    pipeline = ForecastPipeline('../data/processed/engineered_features.csv')
    pipeline.run_pipeline()
