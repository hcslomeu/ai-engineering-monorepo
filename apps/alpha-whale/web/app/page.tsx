"use client";

import { useState, useEffect } from "react";
import { PillNav } from "@/components/pill-nav";
import { ChatPanel } from "@/components/chat-panel";
import { TradingViewChart } from "@/components/tradingview-chart";

export default function Home() {
  const [mounted, setMounted] = useState(false);
  const [symbol, setSymbol] = useState("NASDAQ:NVDA");

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="h-screen w-full">
      <PillNav />

      <section className="h-screen w-full pt-24 pb-8 px-4 flex flex-col overflow-hidden">
        <div className="flex-1 flex flex-col h-full max-w-7xl mx-auto w-full gap-4">
          <div className="h-[60%] w-full rounded-2xl border bg-card overflow-hidden shadow-sm">
            <TradingViewChart symbol={symbol} />
          </div>

          <div className="h-[40%]">
            <ChatPanel onSymbolChange={setSymbol} />
          </div>
        </div>
      </section>
    </div>
  );
}
