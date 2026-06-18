"use client";

import React, { useState } from 'react';
import { Upload, Filter, X } from 'lucide-react';
import { DashboardFilters } from '../types';
import { api } from '../lib/api';

interface FilterBarProps {
  filters: DashboardFilters;
  onFilterChange: (filters: DashboardFilters) => void;
}

export const FilterBar: React.FC<FilterBarProps> = ({ filters, onFilterChange }) => {
  const categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Beauty', 'Sports'];
  const regions = ['North', 'South', 'East', 'West'];

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>) => {
    onFilterChange({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const clearFilters = () => {
    onFilterChange({});
  };

  return (
    <div className="flex flex-wrap items-center gap-4 p-4 bg-white rounded-xl border border-zinc-200 dark:bg-zinc-900 dark:border-zinc-800">
      <div className="flex items-center gap-2 text-zinc-500 mr-2">
        <Filter size={18} />
        <span className="text-sm font-medium">Filters</span>
      </div>

      <select
        name="category"
        value={filters.category || ''}
        onChange={handleChange}
        className="px-3 py-1.5 text-sm rounded-lg border border-zinc-200 bg-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All Categories</option>
        {categories.map(c => <option key={c} value={c}>{c}</option>)}
      </select>

      <select
        name="region"
        value={filters.region || ''}
        onChange={handleChange}
        className="px-3 py-1.5 text-sm rounded-lg border border-zinc-200 bg-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All Regions</option>
        {regions.map(r => <option key={r} value={r}>{r}</option>)}
      </select>

      <input
        type="date"
        name="start_date"
        value={filters.start_date || ''}
        onChange={handleChange}
        className="px-3 py-1.5 text-sm rounded-lg border border-zinc-200 bg-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        type="date"
        name="end_date"
        value={filters.end_date || ''}
        onChange={handleChange}
        className="px-3 py-1.5 text-sm rounded-lg border border-zinc-200 bg-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      {Object.keys(filters).length > 0 && (
        <button
          onClick={clearFilters}
          className="flex items-center gap-1 px-3 py-1.5 text-sm text-zinc-500 hover:text-zinc-900"
        >
          <X size={14} /> Clear
        </button>
      )}
    </div>
  );
};

interface UploadButtonProps {
  onUploadSuccess: () => void;
}

export const UploadButton: React.FC<UploadButtonProps> = ({ onUploadSuccess }) => {
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    try {
      await api.uploadCSV(file);
      onUploadSuccess();
      alert('File uploaded successfully');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setIsUploading(false);
      // Reset input
      e.target.value = '';
    }
  };

  return (
    <label className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700 transition-colors">
      {isUploading ? (
        <span className="animate-spin mr-2">◌</span>
      ) : (
        <Upload size={18} />
      )}
      <span className="text-sm font-medium">{isUploading ? 'Uploading...' : 'Upload CSV'}</span>
      <input
        type="file"
        accept=".csv"
        className="hidden"
        onChange={handleFileChange}
        disabled={isUploading}
      />
    </label>
  );
};
