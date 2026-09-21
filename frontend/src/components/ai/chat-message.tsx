"use client";

import { useState } from "react";
import { 
  Bot, 
  User as UserIcon, 
  Sparkles, 
  ChevronDown, 
  ChevronUp, 
  CheckCircle2, 
  Table as TableIcon,
  BarChart2,
  TrendingUp
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export interface ChatMessageData {
  id: string;
  role: "user" | "assistant";
  content: string;
  analysis?: {
    intent?: string;
    metric?: string;
    group_by?: string;
    aggregation?: string;
    limit?: number;
    rows_analyzed?: number;
    results?: Array<{ label: string; value: number }>;
    chart?: {
      type: "bar" | "line";
      title?: string;
      labels: string[];
      values: number[];
    };
  };
  methodology?: string;
  timestamp: string;
}

function formatChartValue(val: number): string {
  if (Math.abs(val) >= 1_000_000) return `$${(val / 1_000_000).toFixed(1)}M`;
  if (Math.abs(val) >= 1_000) return `$${(val / 1_000).toFixed(1)}k`;
  if (Math.abs(val) < 1 && val !== 0) return `${(val * 100).toFixed(1)}%`;
  return `$${val.toLocaleString(undefined, { maximumFractionDigits: 1 })}`;
}

export function ChatMessageItem({ message }: { message: ChatMessageData }) {
  const isUser = message.role === "user";
  const [showDetails, setShowDetails] = useState(false);

  const analysis = message.analysis;
  const chart = analysis?.chart;
  const labels = chart?.labels || [];
  const values = chart?.values || [];
  const maxValue = values.length > 0 ? Math.max(...values, 1) : 1;

  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-indigo-600 to-blue-500 text-white flex items-center justify-center shrink-0 text-xs font-bold shadow-sm">
          <Sparkles className="h-4 w-4" />
        </div>
      )}

      <div className={`space-y-2 max-w-[88%] ${isUser ? "items-end" : "items-start"}`}>
        <div
          className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${
            isUser
              ? "bg-indigo-600 text-white rounded-tr-none font-medium"
              : "bg-card text-card-foreground rounded-tl-none border"
          }`}
        >
          {/* Main Markdown Text rendering */}
          <div className="space-y-2.5">
            {message.content.split("\n").map((line, i) => {
              if (line.startsWith("### ")) {
                return <h4 key={i} className="font-bold text-base text-foreground mt-2 mb-1">{line.replace("### ", "")}</h4>;
              }
              if (line.startsWith("- ")) {
                return (
                  <div key={i} className="flex items-start gap-2 pl-1 text-xs sm:text-sm">
                    <span className="text-indigo-500 font-bold">•</span>
                    <span>{line.replace("- ", "")}</span>
                  </div>
                );
              }
              if (line.match(/^\d+\.\s+\*\*/)) {
                const parts = line.split(" - ");
                return (
                  <div key={i} className="flex items-center justify-between py-1.5 px-3 rounded-lg bg-muted/40 text-xs sm:text-sm my-1 border border-border/40 hover:bg-muted/60 transition-colors">
                    <span className="font-semibold text-foreground truncate max-w-[65%]">{parts[0]}</span>
                    <span className="font-mono font-bold text-indigo-600 dark:text-indigo-400 shrink-0">{parts[1] || ""}</span>
                  </div>
                );
              }
              if (line.startsWith("> ")) {
                return (
                  <div key={i} className="p-3 my-2 rounded-lg bg-indigo-50/70 dark:bg-indigo-950/40 border-l-4 border-indigo-500 text-xs text-indigo-950 dark:text-indigo-200">
                    {line.replace("> ", "")}
                  </div>
                );
              }
              if (line.startsWith("---")) {
                return <hr key={i} className="my-2 border-border/50" />;
              }
              if (line.startsWith("**Verification Details:**")) {
                return (
                  <p key={i} className="text-[11px] text-muted-foreground flex items-center gap-1.5 pt-1">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500 shrink-0" />
                    <span>{line.replace("**Verification Details:**", "").trim()}</span>
                  </p>
                );
              }
              return line ? <p key={i} className={isUser ? "text-white" : "text-foreground/90"}>{line}</p> : null;
            })}
          </div>

          {/* Embedded Native SVG / Visual Distribution Bar Chart */}
          {labels.length > 0 && !isUser && (
            <div className="mt-4 pt-3 border-t border-border/50 space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-foreground flex items-center gap-1.5">
                  {chart?.type === "line" ? <TrendingUp className="h-3.5 w-3.5 text-indigo-500" /> : <BarChart2 className="h-3.5 w-3.5 text-indigo-500" />}
                  {chart?.title || "Visual Distribution"}
                </span>
                <Badge variant="secondary" className="text-[10px] uppercase font-bold">
                  {chart?.type || "Bar"} Chart
                </Badge>
              </div>

              <div className="p-3 rounded-xl bg-muted/25 border border-border/40 space-y-2">
                {labels.slice(0, 6).map((label, idx) => {
                  const val = values[idx] || 0;
                  const pct = Math.min(100, Math.max(4, (val / maxValue) * 100));
                  return (
                    <div key={idx} className="space-y-1">
                      <div className="flex justify-between text-[11px]">
                        <span className="text-muted-foreground font-medium truncate max-w-[65%]">{label}</span>
                        <span className="font-mono font-bold text-foreground">{formatChartValue(val)}</span>
                      </div>
                      <div className="h-2 w-full bg-muted/60 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-indigo-500 to-blue-500 rounded-full transition-all duration-500"
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Analysis Audit & Methodology Drawer */}
          {analysis && analysis.intent && !isUser && (
            <div className="mt-3 pt-2.5 border-t border-border/40">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowDetails(!showDetails)}
                className="h-6 px-2 text-[11px] text-muted-foreground hover:text-foreground font-medium flex items-center gap-1 w-full justify-between"
              >
                <span className="flex items-center gap-1.5">
                  <TableIcon className="h-3 w-3 text-indigo-500" />
                  Analytics Audit Details
                </span>
                {showDetails ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
              </Button>

              {showDetails && (
                <div className="mt-2 p-3 rounded-lg bg-muted/50 text-xs space-y-2 border border-border/50 animate-in fade-in-50">
                  <div className="grid grid-cols-2 gap-2 text-[11px]">
                    <div><span className="text-muted-foreground">Intent:</span> <span className="font-semibold uppercase">{analysis.intent}</span></div>
                    <div><span className="text-muted-foreground">Metric:</span> <span className="font-semibold">{analysis.metric || "N/A"}</span></div>
                    <div><span className="text-muted-foreground">Dimension:</span> <span className="font-semibold">{analysis.group_by || "N/A"}</span></div>
                    <div><span className="text-muted-foreground">Rows Analyzed:</span> <span className="font-semibold">{analysis.rows_analyzed?.toLocaleString() || "N/A"}</span></div>
                  </div>
                  {message.methodology && (
                    <div className="text-[10px] text-muted-foreground pt-1 border-t border-border/40">
                      Methodology: {message.methodology}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        <div className={`text-[10px] text-muted-foreground px-1 ${isUser ? "text-right" : "text-left"}`}>
          {message.timestamp}
        </div>
      </div>

      {isUser && (
        <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center shrink-0 text-xs text-muted-foreground border shadow-sm">
          <UserIcon className="h-4 w-4" />
        </div>
      )}
    </div>
  );
}

// Default export alias for compatibility
export function ChatMessage({ message }: { message: any }) {
  return <ChatMessageItem message={message} />;
}
