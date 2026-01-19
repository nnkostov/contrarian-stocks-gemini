"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

export default function ScreenerPage() {
  const { data: stocks, isLoading } = useQuery({
    queryKey: ["screen", "sp500"],
    queryFn: () => api.getTopOpportunities("sp500", 20),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white">Screener</h1>
        <p className="text-slate-400">Deep scan of S&P 500 for divergence.</p>
      </div>

      <div className="rounded-md border border-slate-800 bg-slate-900 overflow-hidden">
        <Table>
          <TableHeader className="bg-slate-950">
            <TableRow className="border-slate-800 hover:bg-slate-950">
              <TableHead className="text-slate-400">Ticker</TableHead>
              <TableHead className="text-slate-400">Price</TableHead>
              <TableHead className="text-slate-400">Signal</TableHead>
              <TableHead className="text-slate-400 text-right">Contrarian Score</TableHead>
              <TableHead className="text-slate-400 text-right">Fundamental</TableHead>
              <TableHead className="text-slate-400 text-right">Sentiment</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <TableRow key={i} className="border-slate-800">
                   <TableCell><Skeleton className="h-4 w-12 bg-slate-800" /></TableCell>
                   <TableCell><Skeleton className="h-4 w-16 bg-slate-800" /></TableCell>
                   <TableCell><Skeleton className="h-4 w-24 bg-slate-800" /></TableCell>
                   <TableCell className="text-right"><Skeleton className="h-4 w-8 ml-auto bg-slate-800" /></TableCell>
                   <TableCell className="text-right"><Skeleton className="h-4 w-8 ml-auto bg-slate-800" /></TableCell>
                   <TableCell className="text-right"><Skeleton className="h-4 w-8 ml-auto bg-slate-800" /></TableCell>
                </TableRow>
              ))
            ) : (
              stocks?.map((stock) => (
                <TableRow key={stock.ticker} className="border-slate-800 hover:bg-slate-800/50">
                  <TableCell className="font-medium text-white">{stock.ticker}</TableCell>
                  <TableCell className="text-slate-300">${stock.price.toFixed(2)}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className="border-slate-700 text-slate-400">
                      {stock.scores.signal}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right font-bold text-amber-500">
                    {stock.scores.contrarian_score.toFixed(1)}
                  </TableCell>
                  <TableCell className="text-right text-slate-400">
                    {stock.scores.fundamental_score.toFixed(1)}
                  </TableCell>
                  <TableCell className="text-right text-slate-400">
                    {stock.scores.sentiment_score.toFixed(1)}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
