"use client";

import React, { useState, useEffect, useCallback } from 'react';
import {
  DollarSign,
  ShoppingCart,
  TrendingUp,
  Users,
  BarChart3,
  Activity
} from 'lucide-react';
import { KPICard } from '@/components/KPICard';
import { SalesTrendChart, ProductPerformanceChart } from '@/components/AnalyticsCharts';
import { FilterBar, UploadButton } from '@/components/DashboardControls';
import { api } from '@/lib/api';
import {
  KPIResponse,
  SalesTrend,
  ProductPerformance,
  DashboardFilters
} from '@/types';

export default function Dashboard() {
  const [filters, setFilters] = useState<DashboardFilters>({});
  const [kpis, setKpis] = useState<KPIResponse | null>(null);
  const [salesTrends, setSalesTrends] = useState<SalesTrend[]>([]);
  const [productPerformance, setProductPerformance] = useState<ProductPerformance[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [kpiData, trendData, performanceData] = await Promise.all([
        api.getKPIs(filters),
        api.getSalesTrends(filters),
        api.getProductPerformance(filters)
      ]);

      setKpis(kpiData);
      setSalesTrends(trendData);
      setProductPerformance(performanceData);
    } catch (err) {
      setError('Failed to fetch analytics data. Please make sure the backend is running.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    void fetchData();
  }, [fetchData]);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black text-zinc-900 dark:text-zinc-50">
      <header className="sticky top-0 z-10 bg-white border-b border-zinc-200 dark:bg-zinc-900 dark:border-zinc-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-1.5 rounded-lg text-white">
              <BarChart3 size={20} />
            </div>
            <h1 className="text-xl font-bold tracking-tight">E-com Analytics</h1>
          </div>
          <UploadButton onUploadSuccess={fetchData} />
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <FilterBar filters={filters} onFilterChange={setFilters} />
        </div>

        {error && (
          <div className="mb-8 p-4 bg-rose-50 border border-rose-200 text-rose-600 rounded-xl">
            {error}
          </div>
        )}

        {isLoading && !kpis ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin text-blue-600">
              <Activity size={32} />
            </div>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <KPICard
                title="Total Revenue"
                value={`$${kpis?.total_revenue.toLocaleString()}`}
                icon={DollarSign}
                trend={kpis?.growth_rate}
              />
              <KPICard
                title="Avg. Order Value"
                value={`$${kpis?.aov.toLocaleString()}`}
                icon={TrendingUp}
              />
              <KPICard
                title="Total Orders"
                value={kpis?.total_orders || 0}
                icon={ShoppingCart}
              />
              <KPICard
                title="Retention Rate"
                value={kpis?.retention_rate || 0}
                icon={Users}
                suffix="%"
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-zinc-200 dark:bg-zinc-900 dark:border-zinc-800">
                <h3 className="text-lg font-semibold mb-6">Sales Trends</h3>
                <SalesTrendChart data={salesTrends} />
              </div>
              <div className="bg-white p-6 rounded-xl border border-zinc-200 dark:bg-zinc-900 dark:border-zinc-800">
                <h3 className="text-lg font-semibold mb-6">Top Products</h3>
                <ProductPerformanceChart data={productPerformance} />
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
