"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { StockCard } from "@/components/stock-card";
import { Skeleton } from "@/components/ui/skeleton";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Dashboard() {
  const { data: opportunities, isLoading, refetch, isRefetching } = useQuery({
    queryKey: ["opportunities"],
    queryFn: () => api.getTopOpportunities("test", 10), // Using 'test' universe for speed
  });

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Market Pulse</h1>
          <p className="text-slate-400">Top contrarian opportunities identified today.</p>
        </div>
        <Button 
          variant="outline" 
          size="sm" 
          onClick={() => refetch()}
          disabled={isLoading || isRefetching}
          className="border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-300"
        >
          <RefreshCw className={`mr-2 h-4 w-4 ${isRefetching ? "animate-spin" : ""}`} />
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isLoading ? (
          Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-[140px] bg-slate-900/50 rounded-xl border border-slate-800 p-6 space-y-4">
              <div className="flex justify-between">
                <Skeleton className="h-6 w-20 bg-slate-800" />
                <Skeleton className="h-5 w-24 bg-slate-800" />
              </div>
              <div className="flex justify-between items-end pt-2">
                 <Skeleton className="h-10 w-16 bg-slate-800" />
                 <div className="space-y-2">
                    <Skeleton className="h-4 w-20 bg-slate-800" />
                    <Skeleton className="h-4 w-20 bg-slate-800" />
                 </div>
              </div>
            </div>
          ))
        ) : opportunities?.length === 0 ? (
          <div className="col-span-full py-12 text-center text-slate-500 bg-slate-900/30 rounded-xl border border-slate-800 border-dashed">
            No opportunities found above the threshold.
          </div>
        ) : (
          opportunities?.map((stock) => (
            <StockCard key={stock.ticker} stock={stock} />
          ))
        )}
      </div>
    </div>
  );
}