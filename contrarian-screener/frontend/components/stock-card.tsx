import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { StockData } from "@/lib/api";
import { ArrowUpRight, ArrowDownRight, Activity } from "lucide-react";

export function StockCard({ stock }: { stock: StockData }) {
  const isBullish = stock.scores.signal.toLowerCase().includes("long");
  const isBearish = stock.scores.signal.toLowerCase().includes("short");
  
  const scoreColor = stock.scores.contrarian_score > 70 
    ? "text-emerald-500" 
    : stock.scores.contrarian_score > 40 
      ? "text-amber-500" 
      : "text-slate-500";

  return (
    <Card className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
          {stock.ticker}
          <span className="text-sm font-normal text-slate-400">${stock.price.toFixed(2)}</span>
        </CardTitle>
        <Badge variant={isBullish ? "default" : "secondary"} className={isBullish ? "bg-emerald-500/15 text-emerald-500 hover:bg-emerald-500/25" : "bg-slate-800 text-slate-400"}>
          {stock.scores.signal}
        </Badge>
      </CardHeader>
      <CardContent>
        <div className="flex items-end justify-between">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Contrarian Score</p>
            <div className={`text-3xl font-bold ${scoreColor} flex items-center gap-1`}>
              {stock.scores.contrarian_score.toFixed(0)}
              <Activity size={16} />
            </div>
          </div>
          
          <div className="text-right space-y-1">
            <div className="flex items-center justify-end gap-2 text-sm text-slate-300">
              <span className="text-slate-500">Fund.</span>
              <span>{stock.scores.fundamental_score.toFixed(0)}</span>
            </div>
            <div className="flex items-center justify-end gap-2 text-sm text-slate-300">
              <span className="text-slate-500">Sent.</span>
              <span>{stock.scores.sentiment_score.toFixed(0)}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
