"""
Data Loader Module
Handles loading, validation, and initial processing of retail sales data
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load and validate retail sales datasets"""
    
    SUPPORTED_FORMATS = ['.csv', '.xlsx', '.parquet']
    
    def __init__(self, file_path):
        """
        Initialize DataLoader
        
        Args:
            file_path (str): Path to data file
        """
        self.file_path = Path(file_path)
        self.df = None
        self.date_col = None
        self.sales_col = None
    
    def load(self):
        """Load data from file"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        suffix = self.file_path.suffix.lower()
        
        if suffix == '.csv':
            self.df = pd.read_csv(self.file_path)
        elif suffix == '.xlsx':
            self.df = pd.read_excel(self.file_path)
        elif suffix == '.parquet':
            self.df = pd.read_parquet(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
        
        logger.info(f"✓ Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
        return self.df
    
    def identify_columns(self):
        """Automatically identify date and sales columns"""
        # Find date column
        date_candidates = [col for col in self.df.columns 
                          if 'date' in col.lower() or 'time' in col.lower()]
        
        if date_candidates:
            self.date_col = date_candidates[0]
            logger.info(f"✓ Identified date column: {self.date_col}")
        
        # Find sales column
        sales_candidates = [col for col in self.df.columns 
                           if 'sales' in col.lower() or 'amount' in col.lower() 
                           or 'revenue' in col.lower()]
        
        if sales_candidates:
            self.sales_col = sales_candidates[0]
            logger.info(f"✓ Identified sales column: {self.sales_col}")
        
        return self.date_col, self.sales_col
    
    def clean(self):
        """Basic data cleaning"""
        # Remove duplicates
        initial_len = len(self.df)
        self.df = self.df.drop_duplicates()
        duplicates_removed = initial_len - len(self.df)
        
        if duplicates_removed > 0:
            logger.info(f"✓ Removed {duplicates_removed} duplicate rows")
        
        # Convert date to datetime
        if self.date_col:
            self.df[self.date_col] = pd.to_datetime(self.df[self.date_col], errors='coerce')
            logger.info(f"✓ Converted {self.date_col} to datetime")
        
        # Handle missing values
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.df[col].isnull().sum() > 0:
                self.df[col].fillna(self.df[col].mean(), inplace=True)
        
        logger.info(f"✓ Data cleaning complete")
        return self.df
    
    def validate(self):
        """Validate data quality"""
        issues = []
        
        # Check for date column
        if not self.date_col:
            issues.append("⚠ No date column identified")
        
        # Check for sales column
        if not self.sales_col:
            issues.append("⚠ No sales column identified")
        
        # Check for missing values
        missing_pct = (self.df.isnull().sum() / len(self.df) * 100).max()
        if missing_pct > 50:
            issues.append(f"⚠ High missing values: {missing_pct:.1f}%")
        
        # Check for negative sales
        if self.sales_col and (self.df[self.sales_col] < 0).any():
            issues.append("⚠ Negative sales values detected")
        
        if issues:
            for issue in issues:
                logger.warning(issue)
        else:
            logger.info("✓ Data validation passed")
        
        return len(issues) == 0


def load_sample_data():
    """Create sample retail sales data for testing"""
    dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
    n = len(dates)
    
    # Generate synthetic sales with trend and seasonality
    trend = np.linspace(0, 100, n)
    seasonality = 50 * np.sin(2 * np.pi * np.arange(n) / 365)
    noise = np.random.normal(0, 20, n)
    sales = 500 + trend + seasonality + noise
    sales = np.maximum(sales, 100)  # Ensure positive values
    
    df = pd.DataFrame({
        'OrderDate': dates,
        'Sales': sales,
        'Quantity': np.random.randint(1, 20, n),
        'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Home'], n)
    })
    
    return df


if __name__ == '__main__':
    # Example usage
    print("Data Loader Module - Retail Sales Analytics")
    print("=" * 50)
    
    # Create sample data
    sample_df = load_sample_data()
    sample_df.to_csv('../data/raw/sample_sales_data.csv', index=False)
    print("✓ Created sample data: data/raw/sample_sales_data.csv")
    
    # Test loader
    loader = DataLoader('../data/raw/sample_sales_data.csv')
    loader.load()
    loader.identify_columns()
    loader.clean()
    loader.validate()
    
    print(f"\nLoaded data shape: {loader.df.shape}")
    print(f"Date column: {loader.date_col}")
    print(f"Sales column: {loader.sales_col}")
