import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self, data: List[Dict[str, Any]]):
        self.df = pd.DataFrame(data)
        if not self.df.empty:
            self.df['date'] = pd.to_datetime(self.df['date'])

    def filter_data(self,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   category: Optional[str] = None,
                   region: Optional[str] = None,
                   segment: Optional[str] = None):
        if self.df.empty:
            return self

        filtered_df = self.df.copy()

        if start_date:
            filtered_df = filtered_df[filtered_df['date'] >= start_date]
        if end_date:
            filtered_df = filtered_df[filtered_df['date'] <= end_date]
        if category:
            filtered_df = filtered_df[filtered_df['category'] == category]
        if region:
            filtered_df = filtered_df[filtered_df['region'] == region]
        if segment:
            filtered_df = filtered_df[filtered_df['segment'] == segment]

        self.df = filtered_df
        return self

    def get_kpis(self) -> Dict[str, Any]:
        if self.df.empty:
            return {
                "total_revenue": 0, "aov": 0, "total_orders": 0,
                "growth_rate": 0, "retention_rate": 0
            }

        total_revenue = self.df['total_price'].sum()
        total_orders = self.df['transaction_id'].nunique()
        aov = total_revenue / total_orders if total_orders > 0 else 0

        # Growth Rate Calculation
        latest_month = self.df['date'].max().to_period('M')
        prev_month = latest_month - 1

        rev_current = self.df[self.df['date'].dt.to_period('M') == latest_month]['total_price'].sum()
        rev_prev = self.df[self.df['date'].dt.to_period('M') == prev_month]['total_price'].sum()

        growth_rate = ((rev_current - rev_prev) / rev_prev * 100) if rev_prev > 0 else 0

        # Retention Rate Calculation
        customers_current = set(self.df[self.df['date'].dt.to_period('M') == latest_month]['customer_id'].unique())
        customers_prev = set(self.df[self.df['date'].dt.to_period('M') == prev_month]['customer_id'].unique())

        retained = customers_current.intersection(customers_prev)
        retention_rate = (len(retained) / len(customers_prev) * 100) if len(customers_prev) > 0 else 0

        return {
            "total_revenue": round(total_revenue, 2),
            "aov": round(aov, 2),
            "total_orders": total_orders,
            "growth_rate": round(growth_rate, 2),
            "retention_rate": round(retention_rate, 2)
        }

    def get_sales_trends(self) -> List[Dict[str, Any]]:
        if self.df.empty: return []

        # Group by date (daily or monthly)
        trends = self.df.set_index('date').resample('D')['total_price'].sum().reset_index()
        trends['date'] = trends['date'].dt.strftime('%Y-%m-%d')
        return trends.to_dict('records')

    def get_product_performance(self) -> List[Dict[str, Any]]:
        if self.df.empty: return []

        perf = self.df.groupby('product_name').agg({
            'total_price': 'sum',
            'quantity': 'sum'
        }).sort_values('total_price', ascending=False).head(10).reset_index()

        return perf.to_dict('records')

    def get_customer_insights(self) -> Dict[str, Any]:
        if self.df.empty: return {}

        segment_dist = self.df.groupby('segment')['total_price'].sum().to_dict()
        region_dist = self.df.groupby('region')['total_price'].sum().to_dict()

        return {
            "segments": segment_dist,
            "regions": region_dist
        }
