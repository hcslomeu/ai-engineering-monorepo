import { ArrowLeftRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface ComparisonCardProps {
  metric: string;
  tickers: string[];
  data: Record<string, { date: string; value: number }[]>;
  summary: string;
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr + "T00:00:00");
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function formatValue(value: number, metric: string): string {
  if (metric === "volume") {
    return value >= 1_000_000
      ? `${(value / 1_000_000).toFixed(1)}M`
      : value.toLocaleString();
  }
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  });
}

export function ComparisonCard({
  metric,
  tickers,
  data,
  summary,
}: ComparisonCardProps) {
  if (tickers.length === 0) return null;

  const dates = data[tickers[0]]?.map((d) => d.date) ?? [];

  return (
    <Card className="w-full bg-card/60 backdrop-blur-sm border-primary/10 overflow-hidden">
      <CardHeader className="flex flex-row items-center gap-2 space-y-0 pb-1.5 pt-2.5 px-3">
        <ArrowLeftRight className="h-3.5 w-3.5 text-primary" />
        <CardTitle className="text-xs font-bold tracking-wide">
          {tickers.join(" vs ")}{" "}
          <span className="font-normal text-muted-foreground capitalize">
            ({metric})
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="px-3 pb-2.5 pt-0">
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-transparent border-primary/10">
              <TableHead className="text-[11px] text-muted-foreground">
                Date
              </TableHead>
              {tickers.map((t) => (
                <TableHead
                  key={t}
                  className="text-[11px] text-muted-foreground text-right"
                >
                  {t}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {dates.map((date, i) => (
              <TableRow
                key={date}
                className="hover:bg-muted/30 border-primary/5"
              >
                <TableCell className="text-[11px] font-medium">
                  {formatDate(date)}
                </TableCell>
                {tickers.map((t) => (
                  <TableCell
                    key={t}
                    className="text-[11px] text-right font-mono"
                  >
                    {data[t]?.[i]
                      ? formatValue(data[t][i].value, metric)
                      : "—"}
                  </TableCell>
                ))}
              </TableRow>
            ))}
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
