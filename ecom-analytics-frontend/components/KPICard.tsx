import React from 'react';
import { LucideIcon } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface KPICardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: number;
  suffix?: string;
  className?: string;
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  icon: Icon,
  trend,
  suffix,
  className
}) => {
  const isPositive = trend && trend > 0;

  return (
    <div className={cn(
      "p-6 bg-white rounded-xl shadow-sm border border-zinc-200 dark:bg-zinc-900 dark:border-zinc-800",
      className
    )}>
      <div className="flex items-center justify-between mb-4">
        <div className="p-2 bg-blue-50 text-blue-600 rounded-lg dark:bg-blue-900/20 dark:text-blue-400">
          <Icon size={20} />
        </div>
        {trend !== undefined && (
          <div className={cn(
            "text-xs font-medium px-2 py-1 rounded-full",
            isPositive
              ? "bg-emerald-50 text-emerald-600 dark:bg-emerald-900/20 dark:text-emerald-400"
              : "bg-rose-50 text-rose-600 dark:bg-rose-900/20 dark:text-rose-400"
          )}>
            {isPositive ? '+' : ''}{trend}%
          </div>
        )}
      </div>
      <div>
        <p className="text-sm font-medium text-zinc-500 dark:text-zinc-400">{title}</p>
        <h3 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50 mt-1">
          {typeof value === 'number' ? value.toLocaleString() : value}
          {suffix && <span className="text-sm font-normal ml-1">{suffix}</span>}
        </h3>
      </div>
    </div>
  );
};
