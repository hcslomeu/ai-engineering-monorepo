"use client";

import { useTheme } from "next-themes";
import { Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function PillNav() {
  const { resolvedTheme, setTheme } = useTheme();

  return (
    <div className="fixed top-6 left-1/2 z-50 -translate-x-1/2 w-fit">
      <div
        className={cn(
          "rounded-full border bg-card/80 backdrop-blur-md shadow-sm",
          "px-3 py-2 flex items-center gap-6"
        )}
      >
        <div className="flex items-center gap-2 pl-2">
          <span className="text-lg">🐋</span>
          <span className="text-sm font-bold tracking-tight">AlphaWhale</span>
        </div>
        <div className="hidden items-center gap-1 md:flex">
          <a
            href="https://github.com/hcslomeu/ai-engineering-monorepo"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            GitHub
          </a>
          <a
            href="#"
            className="px-3 py-1 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            Docs
          </a>
          <a
            href="#"
            className="px-3 py-1 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            About
          </a>
        </div>
        <div className="flex items-center gap-2 pr-1">
          <Button
            variant="ghost"
            size="icon"
            className="rounded-full h-8 w-8"
            onClick={() =>
              setTheme(resolvedTheme === "dark" ? "light" : "dark")
            }
          >
            {resolvedTheme === "dark" ? (
              <Sun className="h-4 w-4" />
            ) : (
              <Moon className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
