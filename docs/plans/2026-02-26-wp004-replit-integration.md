# WP-004 AlphaWhale Web — Replit Design Integration

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Port the Replit "Sinalizador" design into the monorepo as a Next.js app, rebranded as AlphaWhale with English copy and Mag 7 stocks. Full-screen trading workspace with TradingView chart + SSE chat.

**Architecture:** Next.js 15 App Router with shadcn/ui (New York style). Design tokens ported from Replit's CSS variables. Chat panel wired to FastAPI SSE backend via `fetch` + `ReadableStream`. No server components for interactive features — pages are `"use client"`.

**Tech Stack:** Next.js 15, React 19, Tailwind CSS 4, shadcn/ui, next-themes, framer-motion, react-ts-tradingview-widgets, lucide-react

**Source reference:** `/Users/humbertolomeu/ai-engineering-monorepo/uploaded-files/replit-design/`

**Learning mode note:** Frontend is vibe-coded. No line-by-line TS/JSX explanations. High-level overviews per task. No code contribution requests for TS/React. Batch related files.

---

## Task 1: Next.js Scaffold + Dependencies

**Goal:** Working Next.js app with all dependencies installed.

**Files:**
- Create: `apps/alpha-whale/web/package.json`
- Create: `apps/alpha-whale/web/tsconfig.json`
- Create: `apps/alpha-whale/web/next.config.ts`
- Create: `apps/alpha-whale/web/postcss.config.mjs`
- Create: `apps/alpha-whale/web/project.json` (Nx targets)
- Delete: `apps/alpha-whale/web/src/` (empty leftover directory)

**Step 1: Create `package.json`**

```json
{
  "name": "alpha-whale-web",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "next dev --port 3000",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.3.4",
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "next-themes": "^0.4.6",
    "framer-motion": "^12.23.24",
    "react-ts-tradingview-widgets": "^1.2.8",
    "lucide-react": "^0.545.0",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "tailwind-merge": "^3.3.1",
    "tw-animate-css": "^1.4.0",
    "@radix-ui/react-avatar": "^1.1.11",
    "@radix-ui/react-scroll-area": "^1.2.10",
    "@radix-ui/react-slot": "^1.2.4",
    "@radix-ui/react-tooltip": "^1.2.8"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4.1.14",
    "tailwindcss": "^4.1.14",
    "@types/react": "^19.2.0",
    "@types/react-dom": "^19.2.0",
    "typescript": "^5.9.2",
    "@types/node": "^20.19.0",
    "eslint": "^9.28.0",
    "eslint-config-next": "^15.3.4"
  }
}
```

**Step 2: Create `tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**Step 3: Create `next.config.ts`**

API proxy rewrites `/api/*` to FastAPI backend. Security headers per CLAUDE.md.

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/:path*",
      },
    ];
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
        ],
      },
    ];
  },
  productionBrowserSourceMaps: false,
};

export default nextConfig;
```

**Step 4: Create `postcss.config.mjs`**

```javascript
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

**Step 5: Create `project.json`** (Nx integration)

```json
{
  "name": "alpha-whale-web",
  "$schema": "../../../node_modules/nx/schemas/project-schema.json",
  "projectType": "application",
  "sourceRoot": "apps/alpha-whale/web",
  "targets": {
    "dev": {
      "command": "pnpm next dev --port 3000",
      "options": { "cwd": "apps/alpha-whale/web" }
    },
    "build": {
      "command": "pnpm next build",
      "options": { "cwd": "apps/alpha-whale/web" }
    },
    "lint": {
      "command": "pnpm next lint",
      "options": { "cwd": "apps/alpha-whale/web" }
    }
  }
}
```

**Step 6: Delete empty `src/` and install dependencies**

```bash
rm -rf apps/alpha-whale/web/src
cd apps/alpha-whale/web && pnpm install
```

**Step 7: Verify**

```bash
# Should install without errors
pnpm --filter alpha-whale-web exec next --version
```

**Step 8: Commit**

```bash
git add apps/alpha-whale/web/package.json apps/alpha-whale/web/tsconfig.json apps/alpha-whale/web/next.config.ts apps/alpha-whale/web/postcss.config.mjs apps/alpha-whale/web/project.json
git commit -m "feat(web): scaffold Next.js app with dependencies and Nx integration"
```

---

## Task 2: Design System — CSS Tokens + Fonts + shadcn Config

**Goal:** Port the Replit design tokens (olive green palette, fonts, dark/light mode) into the Next.js app.

**Source:** `uploaded-files/replit-design/client/src/index.css`

**Files:**
- Create: `apps/alpha-whale/web/app/globals.css` (design tokens from Replit)
- Create: `apps/alpha-whale/web/app/layout.tsx` (root layout with fonts + theme)
- Create: `apps/alpha-whale/web/lib/utils.ts` (shadcn `cn` utility)
- Create: `apps/alpha-whale/web/components.json` (shadcn config)

**Step 1: Create `globals.css`**

Port directly from Replit's `index.css`. Identical token structure — olive green palette, stone neutrals, dark/light mode via `.dark` class.

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --font-sans: "Plus Jakarta Sans", "Inter", sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  --color-background: hsl(var(--background));
  --color-foreground: hsl(var(--foreground));
  --color-card: hsl(var(--card));
  --color-card-foreground: hsl(var(--card-foreground));
  --color-popover: hsl(var(--popover));
  --color-popover-foreground: hsl(var(--popover-foreground));
  --color-primary: hsl(var(--primary));
  --color-primary-foreground: hsl(var(--primary-foreground));
  --color-secondary: hsl(var(--secondary));
  --color-secondary-foreground: hsl(var(--secondary-foreground));
  --color-muted: hsl(var(--muted));
  --color-muted-foreground: hsl(var(--muted-foreground));
  --color-accent: hsl(var(--accent));
  --color-accent-foreground: hsl(var(--accent-foreground));
  --color-destructive: hsl(var(--destructive));
  --color-destructive-foreground: hsl(var(--destructive-foreground));
  --color-border: hsl(var(--border));
  --color-input: hsl(var(--input));
  --color-ring: hsl(var(--ring));

  --radius-xl: 1.5rem;
  --radius-lg: var(--radius);
  --radius-md: calc(var(--radius) - 2px);
  --radius-sm: calc(var(--radius) - 4px);
}

:root {
  --background: 60 5% 96%;
  --foreground: 20 14% 4%;
  --card: 0 0% 100%;
  --card-foreground: 20 14% 4%;
  --popover: 0 0% 100%;
  --popover-foreground: 20 14% 4%;
  --border: 0 0% 90%;
  --input: 0 0% 90%;
  --primary: 82 65% 27%;
  --primary-foreground: 0 0% 100%;
  --secondary: 60 5% 90%;
  --secondary-foreground: 20 14% 4%;
  --muted: 60 5% 90%;
  --muted-foreground: 25 5% 45%;
  --accent: 60 5% 90%;
  --accent-foreground: 20 14% 4%;
  --destructive: 0 84% 60%;
  --destructive-foreground: 0 0% 100%;
  --radius: 1rem;
  --ring: 82 65% 27%;
}

.dark {
  --background: 24 10% 10%;
  --foreground: 60 5% 96%;
  --card: 24 10% 15%;
  --card-foreground: 60 5% 96%;
  --popover: 24 10% 15%;
  --popover-foreground: 60 5% 96%;
  --border: 24 10% 20%;
  --input: 24 10% 20%;
  --primary: 74 64% 42%;
  --primary-foreground: 24 10% 10%;
  --secondary: 24 10% 20%;
  --secondary-foreground: 60 5% 96%;
  --muted: 24 10% 20%;
  --muted-foreground: 60 5% 70%;
  --accent: 24 10% 20%;
  --accent-foreground: 60 5% 96%;
  --destructive: 0 84% 60%;
  --destructive-foreground: 0 0% 100%;
  --ring: 74 64% 42%;
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply font-sans antialiased bg-background text-foreground;
  }
  ::selection {
    background-color: #d9e8aa;
    color: #1a1a1a;
  }
  .dark ::selection {
    background-color: #416b17;
    color: #ffffff;
  }
}
```

**Step 2: Create `lib/utils.ts`**

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

**Step 3: Create `app/layout.tsx`**

Root layout with Google Fonts (Plus Jakarta Sans + JetBrains Mono), `next-themes` ThemeProvider, and metadata.

```tsx
import type { Metadata } from "next";
import { ThemeProvider } from "next-themes";
import "./globals.css";

export const metadata: Metadata = {
  title: "AlphaWhale — AI Trading Assistant",
  description: "Conversational AI assistant for stock market analysis",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@200..800&family=JetBrains+Mono:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
          storageKey="alphawhale-theme"
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

**Step 4: Create `components.json`** (shadcn config for Next.js)

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "iconLibrary": "lucide",
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

**Step 5: Commit**

```bash
git add apps/alpha-whale/web/app/globals.css apps/alpha-whale/web/app/layout.tsx apps/alpha-whale/web/lib/utils.ts apps/alpha-whale/web/components.json
git commit -m "feat(web): design system tokens, fonts, and shadcn config from Replit design"
```

---

## Task 3: shadcn/ui Components

**Goal:** Install the shadcn components needed for the workspace page.

**Components needed:** `button`, `card`, `badge`, `input`, `scroll-area`, `avatar`, `tooltip`

**Step 1: Install shadcn components**

```bash
cd apps/alpha-whale/web
npx shadcn@latest add button card badge input scroll-area avatar tooltip
```

This creates files in `components/ui/` automatically.

**Step 2: Verify component files exist**

```bash
ls apps/alpha-whale/web/components/ui/
```

Expected: `button.tsx`, `card.tsx`, `badge.tsx`, `input.tsx`, `scroll-area.tsx`, `avatar.tsx`, `tooltip.tsx`

**Step 3: Commit**

```bash
git add apps/alpha-whale/web/components/
git commit -m "feat(web): install shadcn/ui components (button, card, badge, input, scroll-area, avatar, tooltip)"
```

---

## Task 4: PillNav — Floating Navigation Header

**Goal:** Glassmorphism floating nav bar with AlphaWhale branding, external links, and theme toggle.

**Source:** `uploaded-files/replit-design/client/src/pages/Home.tsx` → `PillNav` component (lines 35-73)

**Files:**
- Create: `apps/alpha-whale/web/components/pill-nav.tsx`

**Step 1: Create `pill-nav.tsx`**

Adapted from Replit's PillNav:
- "Sinalizador" → "AlphaWhale" with whale emoji
- Portuguese nav links → Docs, GitHub, About (external links)
- "Assinar" CTA → removed (portfolio, not SaaS)
- Theme toggle kept (dark/light via next-themes)
- Glassmorphism styling kept (`bg-card/80 backdrop-blur-md`)

```tsx
"use client";

import { useTheme } from "next-themes";
import { Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function PillNav() {
  const { theme, setTheme } = useTheme();

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
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          >
            {theme === "dark" ? (
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
```

**Step 2: Commit**

```bash
git add apps/alpha-whale/web/components/pill-nav.tsx
git commit -m "feat(web): PillNav floating header with AlphaWhale branding and theme toggle"
```

---

## Task 5: SSE Client Utility

**Goal:** Create the SSE client that connects to the FastAPI backend (`POST /api/chat/stream`).

**SSE Contract (from `apps/alpha-whale/api/routes.py`):**
```
POST /api/chat/stream
Body: { "message": "string" }

Response (SSE):
  event: message, data: {"token": "Hello"}    ← append token
  event: error,   data: {"error": "..."}      ← show error
  event: message, data: [DONE]                ← stop streaming
```

**Files:**
- Create: `apps/alpha-whale/web/lib/sse-client.ts`

**Step 1: Create `sse-client.ts`**

Uses `fetch` + `ReadableStream` to consume the SSE stream. No external libraries needed.

```typescript
export interface SSECallbacks {
  onToken: (token: string) => void;
  onError: (error: string) => void;
  onDone: () => void;
}

export async function streamChat(
  message: string,
  callbacks: SSECallbacks,
  signal?: AbortSignal
): Promise<void> {
  const response = await fetch("/api/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
    signal,
  });

  if (!response.ok) {
    callbacks.onError(`Server error: ${response.status}`);
    callbacks.onDone();
    return;
  }

  const reader = response.body?.getReader();
  if (!reader) {
    callbacks.onError("No response stream");
    callbacks.onDone();
    return;
  }

  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6).trim();

          if (data === "[DONE]") {
            callbacks.onDone();
            return;
          }

          try {
            const parsed = JSON.parse(data);
            if (parsed.token) {
              callbacks.onToken(parsed.token);
            }
            if (parsed.error) {
              callbacks.onError(parsed.error);
            }
          } catch {
            // Skip malformed JSON lines
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }

  callbacks.onDone();
}
```

**Step 2: Commit**

```bash
git add apps/alpha-whale/web/lib/sse-client.ts
git commit -m "feat(web): SSE client utility for FastAPI chat streaming"
```

---

## Task 6: Chat Panel Component

**Goal:** Chat panel with message bubbles, input, and SSE streaming. Adapted from Replit's `ChatSection` but wired to real backend.

**Source:** `uploaded-files/replit-design/client/src/pages/Home.tsx` → `ChatSection` (lines 76-121)

**Files:**
- Create: `apps/alpha-whale/web/components/chat-panel.tsx`

**Step 1: Create `chat-panel.tsx`**

Adapted from Replit's ChatSection:
- Local state mock → real SSE streaming via `streamChat()`
- Portuguese placeholder → English: "e.g. How is NVDA performing this week?"
- Portuguese welcome message → English
- Added: streaming state indicator, error display, auto-scroll
- Added: Enter key to send, disabled input while streaming
- Added: AbortController to cancel in-flight streams

```tsx
"use client";

import { useRef, useState, useEffect, useCallback } from "react";
import { Send, Square, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { streamChat } from "@/lib/sse-client";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function ChatPanel() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello! The market is open. What would you like to know about today?",
    },
  ]);
  const [isStreaming, setIsStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || isStreaming) return;

    const userMessage: Message = { role: "user", content: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsStreaming(true);

    const assistantIndex =
      messages.length + 1; // +1 for the user message we just added
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    const controller = new AbortController();
    abortRef.current = controller;

    try {
      await streamChat(
        trimmed,
        {
          onToken: (token) => {
            setMessages((prev) => {
              const updated = [...prev];
              const last = updated[updated.length - 1];
              if (last?.role === "assistant") {
                updated[updated.length - 1] = {
                  ...last,
                  content: last.content + token,
                };
              }
              return updated;
            });
          },
          onError: (error) => {
            setMessages((prev) => {
              const updated = [...prev];
              const last = updated[updated.length - 1];
              if (last?.role === "assistant") {
                updated[updated.length - 1] = {
                  ...last,
                  content: `Error: ${error}`,
                };
              }
              return updated;
            });
          },
          onDone: () => {
            setIsStreaming(false);
            abortRef.current = null;
          },
        },
        controller.signal
      );
    } catch {
      if (!controller.signal.aborted) {
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          if (last?.role === "assistant" && !last.content) {
            updated[updated.length - 1] = {
              ...last,
              content:
                "Connection error — is the backend running? Start it with: poetry run uvicorn api.main:app",
            };
          }
          return updated;
        });
      }
      setIsStreaming(false);
      abortRef.current = null;
    }
  };

  const handleStop = () => {
    abortRef.current?.abort();
    setIsStreaming(false);
    abortRef.current = null;
  };

  return (
    <div className="max-w-3xl mx-auto w-full flex flex-col h-full justify-end pb-4">
      <ScrollArea className="flex-1 px-4 mb-4" ref={scrollRef}>
        <div className="space-y-4">
          {messages.map((m, i) => (
            <div
              key={i}
              className={cn(
                "flex gap-3",
                m.role === "user" ? "flex-row-reverse" : "flex-row"
              )}
            >
              <Avatar className="h-8 w-8 border">
                {m.role === "assistant" ? (
                  <div className="bg-primary w-full h-full flex items-center justify-center text-primary-foreground text-[10px] font-bold">
                    AI
                  </div>
                ) : (
                  <AvatarFallback>
                    <User className="h-4 w-4" />
                  </AvatarFallback>
                )}
              </Avatar>
              <div
                className={cn(
                  "rounded-2xl px-4 py-2 text-sm max-w-[80%]",
                  m.role === "assistant"
                    ? "bg-muted/50 border"
                    : "bg-primary text-primary-foreground"
                )}
              >
                {m.content}
                {isStreaming &&
                  i === messages.length - 1 &&
                  m.role === "assistant" && (
                    <span className="inline-block w-1.5 h-4 bg-foreground/50 ml-0.5 animate-pulse" />
                  )}
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>

      <div className="px-4">
        <div className="relative flex items-center">
          <Input
            className="rounded-full bg-card/80 backdrop-blur-sm border h-12 pl-6 pr-14 shadow-sm focus-visible:ring-primary"
            placeholder="e.g. How is NVDA performing this week?"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
            disabled={isStreaming}
          />
          {isStreaming ? (
            <Button
              size="icon"
              variant="destructive"
              className="absolute right-1.5 h-9 w-9 rounded-full"
              onClick={handleStop}
            >
              <Square className="h-3 w-3" />
            </Button>
          ) : (
            <Button
              size="icon"
              className="absolute right-1.5 h-9 w-9 rounded-full bg-primary hover:bg-primary/90"
              onClick={handleSend}
              disabled={!input.trim()}
            >
              <Send className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add apps/alpha-whale/web/components/chat-panel.tsx
git commit -m "feat(web): ChatPanel with SSE streaming, auto-scroll, and stop button"
```

---

## Task 7: Home Page — Full-Screen Trading Workspace

**Goal:** Assemble the full-screen workspace: PillNav + TradingView chart (60%) + chat panel (40%).

**Source:** `uploaded-files/replit-design/client/src/pages/Home.tsx` → `Home` component (lines 140-186, hero section only)

**Files:**
- Create: `apps/alpha-whale/web/app/page.tsx`

**Step 1: Create `app/page.tsx`**

Adapted from Replit's hero section:
- `BMFBOVESPA:PETR4` → `NASDAQ:NVDA`
- Portuguese scroll text → removed (no below-fold content)
- Bouncing arrow → removed
- Marketing/FAQ/footer sections → removed
- `mounted` hydration guard kept (TradingView widget needs client-side rendering)

```tsx
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
          {/* Chart — 60% */}
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

          {/* Chat — 40% */}
          <div className="h-[40%]">
            <ChatPanel />
          </div>
        </div>
      </section>
    </div>
  );
}
```

**Step 2: Verify dev server starts**

```bash
cd apps/alpha-whale/web && pnpm dev
```

Open `http://localhost:3000` — should see:
- Floating PillNav with "AlphaWhale" branding and theme toggle
- TradingView chart showing NVDA
- Chat panel with welcome message and input

**Step 3: Commit**

```bash
git add apps/alpha-whale/web/app/page.tsx
git commit -m "feat(web): full-screen trading workspace with TradingView chart and chat panel"
```

---

## Task 8: ESLint Config + .gitignore Update

**Goal:** Quality tooling and git hygiene.

**Files:**
- Create: `apps/alpha-whale/web/eslint.config.mjs`
- Modify: root `.gitignore` (add `.next/`)

**Step 1: Create `eslint.config.mjs`**

```javascript
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({ baseDirectory: __dirname });

const eslintConfig = [...compat.extends("next/core-web-vitals", "next/typescript")];

export default eslintConfig;
```

**Step 2: Add `.next/` to root `.gitignore`**

Append to the "compiled output" section:
```
.next
```

**Step 3: Run lint**

```bash
cd apps/alpha-whale/web && pnpm lint
```

Expected: passes (or minor warnings to fix).

**Step 4: Commit**

```bash
git add apps/alpha-whale/web/eslint.config.mjs .gitignore
git commit -m "chore(web): ESLint config and .gitignore update for Next.js"
```

---

## Task 9: Final Verification + Feature Branch

**Goal:** Verify everything works end-to-end and create the feature branch.

**Step 1: Full build check**

```bash
cd apps/alpha-whale/web && pnpm build
```

Expected: Next.js builds successfully.

**Step 2: Nx integration check**

```bash
pnpm nx run alpha-whale-web:build
pnpm nx run alpha-whale-web:lint
```

**Step 3: Manual visual verification**

Start dev server and confirm:
- [ ] PillNav renders with glassmorphism effect
- [ ] Theme toggle switches dark ↔ light
- [ ] TradingView chart loads with NVDA data
- [ ] Chat welcome message displays
- [ ] Typing a message and pressing Enter shows it as a user bubble
- [ ] Without backend: shows connection error message (not crash)
- [ ] With backend (`poetry run uvicorn api.main:app`): tokens stream progressively
- [ ] Stop button appears during streaming and cancels the stream

**Step 4: Squash into feature branch and push**

```bash
git checkout -b feature/WP-004-chat-ui
# commits are already on this branch from tasks 1-8
git push -u origin feature/WP-004-chat-ui
```

---

## What's NOT in This Plan

- Unit/component tests for React → deferred (WP-004 plan: "keep scope focused")
- CI frontend job → Phase E of WP-004 (separate task after this integration)
- Sidebar navigation → revisit in WP-107 when market dashboard is added
- Mobile responsive layout → WP-107 (when both panels have real content)
- Message persistence → future WP
- Multiple conversation threads → future WP
