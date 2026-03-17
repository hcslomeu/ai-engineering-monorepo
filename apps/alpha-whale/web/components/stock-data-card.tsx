import { TrendingDown, TrendingUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { cn } from "@/lib/utils";

interface StockRow {
  date: string;
  open: number;
  close: number;
  high: number;
  low: number;
}

interface StockDataCardProps {
  ticker: string;
  data: StockRow[];
  summary: string;
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr + "T00:00:00");
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function formatPrice(value: number): string {
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  });
}

export function StockDataCard({ ticker, data, summary }: StockDataCardProps) {
  if (data.length === 0) return null;

  const latest = data[0];
  const oldest = data[data.length - 1];
  const periodChange = latest.close - oldest.open;
  const periodPct = oldest.open !== 0 ? (periodChange / oldest.open) * 100 : 0;
  const isPositive = periodChange >= 0;

  return (
    <Card className="w-full bg-card/60 backdrop-blur-sm border-primary/10 overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1.5 pt-2.5 px-3">
        <CardTitle className="text-xs font-bold tracking-wide">
          {ticker}
        </CardTitle>
        <Badge
          variant="outline"
          className={cn(
            "font-mono text-[11px] gap-1 px-1.5 py-0",
            isPositive
              ? "text-emerald-500 border-emerald-500/30"
              : "text-red-500 border-red-500/30",
          )}
        >
          {isPositive ? (
            <TrendingUp className="h-3 w-3" />
          ) : (
            <TrendingDown className="h-3 w-3" />
          )}
          {isPositive ? "+" : ""}
          {periodChange.toFixed(2)} ({periodPct.toFixed(2)}%)
        </Badge>
      </CardHeader>
      <CardContent className="px-3 pb-2.5 pt-0">
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-transparent border-primary/10">
              <TableHead className="text-[11px] text-muted-foreground">
                Date
              </TableHead>
              <TableHead className="text-[11px] text-muted-foreground text-right">
                Close
              </TableHead>
              <TableHead className="text-[11px] text-muted-foreground text-right">
                Change
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((row) => {
              const dailyChange = row.close - row.open;
              const dailyUp = dailyChange >= 0;
              return (
                <TableRow
                  key={row.date}
                  className="hover:bg-muted/30 border-primary/5"
                >
                  <TableCell className="text-[11px] font-medium">
                    {formatDate(row.date)}
                  </TableCell>
                  <TableCell className="text-[11px] text-right font-mono">
                    {formatPrice(row.close)}
                  </TableCell>
                  <TableCell
                    className={cn(
                      "text-[11px] text-right font-mono",
                      dailyUp ? "text-emerald-500" : "text-red-500",
                    )}
                  >
                    {dailyUp ? "+" : ""}
                    {dailyChange.toFixed(2)}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
        {summary && (
          <p className="mt-1.5 text-[11px] text-muted-foreground italic border-t border-primary/5 pt-1.5">
            {summary}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
