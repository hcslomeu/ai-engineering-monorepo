"use client";

import { useEffect, useRef, useState } from "react";
import { Send, Square, User } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { streamChat } from "@/lib/sse-client";
import { cn } from "@/lib/utils";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const WELCOME_MESSAGE: Message = {
  role: "assistant",
  content: "Hello! The market is open. What would you like to know about today?",
};

const SYMBOL_PATTERN = /\b(?:show|chart|display|switch to|pull up)\s+([A-Z]{1,5}(?::[A-Z]{1,5})?)\b/i;

function extractSymbol(text: string): string | null {
  const match = text.match(SYMBOL_PATTERN);
  if (!match) return null;
  const raw = match[1].toUpperCase();
  return raw.includes(":") ? raw : `NASDAQ:${raw}`;
}

interface ChatPanelProps {
  onSymbolChange?: (symbol: string) => void;
}

export function ChatPanel({ onSymbolChange }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const scrollBottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    return () => {
      abortRef.current?.abort();
    };
  }, []);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || isStreaming) return;

    const detected = extractSymbol(trimmed);
    if (detected && onSymbolChange) {
      onSymbolChange(detected);
    }

    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setInput("");
    setIsStreaming(true);
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
              updated[updated.length - 1] = {
                ...updated[updated.length - 1],
                content: updated[updated.length - 1].content + token,
              };
              return updated;
            });
          },
          onError: (error) => {
            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                ...updated[updated.length - 1],
                content: `Error: ${error}`,
              };
              return updated;
            });
          },
          onDone: () => {
            setIsStreaming(false);
            abortRef.current = null;
          },
        },
        controller.signal,
      );
    } catch (err) {
      const wasAborted =
        err instanceof Error && err.name === "AbortError";

      if (!wasAborted) {
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          if (last.role === "assistant" && last.content === "") {
            updated[updated.length - 1] = {
              ...last,
              content:
                "Connection error — is the backend running? Start it with: poetry run uvicorn api.main:app",
            };
          }
          return updated;
        });
      }
    } finally {
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
      <ScrollArea className="flex-1 px-4 mb-4">
        <div className="flex flex-col gap-4 py-4">
          {messages.map((message, index) => {
            const isUser = message.role === "user";
            const isLastAssistant =
              !isUser &&
              index === messages.length - 1 &&
              isStreaming;

            return (
              <div
                key={index}
                className={cn(
                  "flex items-end gap-2",
                  isUser ? "flex-row-reverse" : "flex-row",
                )}
              >
                <Avatar className="h-8 w-8 shrink-0">
                  {isUser ? (
                    <AvatarFallback>
                      <User className="h-4 w-4" />
                    </AvatarFallback>
                  ) : (
                    <AvatarFallback className="bg-primary text-primary-foreground text-xs">
                      AI
                    </AvatarFallback>
                  )}
                </Avatar>
                <div
                  className={cn(
                    "rounded-2xl px-4 py-2 text-sm max-w-[80%]",
                    isUser
                      ? "bg-foreground text-background"
                      : "bg-card border",
                  )}
                >
                  {message.content}
                  {isLastAssistant && (
                    <span className="inline-block w-1.5 h-4 bg-foreground/50 ml-0.5 animate-pulse" />
                  )}
                </div>
              </div>
            );
          })}
          <div ref={scrollBottomRef} />
        </div>
      </ScrollArea>

      <div className="px-4">
        <div className="relative">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                void handleSend();
              }
            }}
            disabled={isStreaming}
            placeholder="e.g. How is NVDA performing this week?"
            className="rounded-full bg-card/80 backdrop-blur-sm border h-12 pl-6 pr-14 shadow-sm focus-visible:ring-primary"
          />
          {isStreaming ? (
            <Button
              aria-label="Stop streaming"
              onClick={handleStop}
              variant="destructive"
              size="icon"
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full h-8 w-8"
            >
              <Square className="h-4 w-4" />
            </Button>
          ) : (
            <Button
              aria-label="Send message"
              onClick={() => void handleSend()}
              size="icon"
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full h-8 w-8"
            >
              <Send className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
