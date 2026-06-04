import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
from typing import List, Dict, Any
import numpy as np

class DataProcessor:
    REQUIRED_COLUMNS = {
        'transaction_id', 'date', 'product_name', 'category',
        'quantity', 'unit_price', 'region', 'segment', 'customer_id'
    }

    @staticmethod
    def process_csv(content: bytes) -> List[Dict[str, Any]]:
        df = pd.read_csv(BytesIO(content))

        # Validate columns
        missing = DataProcessor.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Data Cleaning
        # Drop rows with missing essential data
        df = df.dropna(subset=['transaction_id', 'date', 'total_price'], errors='ignore')

        # Convert date
        df['date'] = pd.to_datetime(df['date'])

        # Calculate total price if not present
        if 'total_price' not in df.columns:
            df['total_price'] = df['quantity'] * df['unit_price']

        # Remove duplicates
        df = df.drop_duplicates(subset=['transaction_id'])

        # Validation: Ensure numeric types
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce').fillna(0.0)
        df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce').fillna(0.0)

        # Convert back to list of dicts for DB insertion
        return df.to_dict('records')

    @staticmethod
    def get_sample_data() -> List[Dict[str, Any]]:
        """Generates mock data for demo purposes"""
        data = []
        categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Beauty', 'Sports']
        regions = ['North', 'South', 'East', 'West']
        segments = ['Consumer', 'Corporate', 'Home Office']

        for i in range(100):
            quantity = np.random.randint(1, 5)
            unit_price = np.random.uniform(10, 500)
            # Mix current and previous month for growth/retention calc
            days_offset = np.random.randint(0, 60)
            date = datetime.now() - timedelta(days=days_offset)

            data.append({
                'transaction_id': f'TRX-{1000+i}',
                'date': date,
                'product_name': f'Product {i}',
                'category': np.random.choice(categories),
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': quantity * unit_price,
                'region': np.random.choice(regions),
                'segment': np.random.choice(segments),
                'customer_id': f'CUST-{np.random.randint(1, 20)}'
            })
        return data
