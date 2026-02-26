"use client";

import { useState, useEffect } from "react";
import { useTheme } from "next-themes";
import { AdvancedRealTimeChart } from "react-ts-tradingview-widgets";
import { PillNav } from "@/components/pill-nav";
import { ChatPanel } from "@/components/chat-panel";

export default function Home() {
  const { resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

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
            <AdvancedRealTimeChart
              symbol="NASDAQ:NVDA"
              theme={resolvedTheme === "dark" ? "dark" : "light"}
              autosize
              hide_top_toolbar
              hide_side_toolbar
              allow_symbol_change={false}
              save_image={false}
              container_id="tradingview_chart"
            />
          </div>

          <div className="h-[40%]">
            <ChatPanel />
          </div>
        </div>
      </section>
    </div>
  );
}
