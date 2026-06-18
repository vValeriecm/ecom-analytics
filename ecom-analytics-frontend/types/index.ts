export interface KPIResponse {
  total_revenue: number;
  aov: number;
  total_orders: number;
  growth_rate: number;
  retention_rate: number;
}

export interface SalesTrend {
  date: string;
  total_price: number;
}

export interface ProductPerformance {
  product_name: string;
  total_price: number;
  quantity: number;
}

export interface CustomerInsights {
  segments: Record<string, number>;
  regions: Record<string, number>;
}

export interface DashboardFilters {
  start_date?: string;
  end_date?: string;
  category?: string;
  region?: string;
  segment?: string;
}
