"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Sparkles, Bot, User as UserIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { SuggestedQuestions } from "@/components/ai/suggested-questions";
import { api } from "@/lib/api";
import { useToast } from "@/components/ui/use-toast";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  context?: Record<string, any>;
  timestamp: string;
}

export function ChatInterface({ datasetId }: { datasetId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = async (text: string) => {
    if (!text.trim() || !datasetId) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await api.post<{ message: string; session_id: string; context?: any }>("/api/v1/chat/", {
        dataset_id: datasetId,
        message: text,
        session_id: sessionId
      });

      if (res.session_id) {
        setSessionId(res.session_id);
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: res.message || "I've analyzed the dataset for your query.",
        context: res.context,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error: any) {
      toast({
        title: "Chat Error",
        description: error.message || "Failed to communicate with analytics engine.",
        variant: "destructive"
      });
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I encountered an issue computing the requested metrics. Please verify the dataset column mappings or try a different phrasing.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full border rounded-lg overflow-hidden bg-card">
      <div className="p-3 border-b bg-muted/30 flex items-center justify-between text-xs font-medium">
        <span className="flex items-center gap-1.5 text-indigo-600 font-semibold">
          <Sparkles className="h-4 w-4" /> DataPilot Deterministic Assistant
        </span>
        <span className="text-muted-foreground font-mono">Dataset: {datasetId.slice(0, 8)}...</span>
      </div>

      <ScrollArea className="flex-1 p-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full py-16 text-center">
            <div className="h-12 w-12 rounded-full bg-indigo-50 dark:bg-indigo-950 flex items-center justify-center text-indigo-600 mb-4">
              <Bot className="h-6 w-6" />
            </div>
            <h3 className="font-semibold text-base mb-1">Ask questions about your data</h3>
            <p className="text-xs text-muted-foreground max-w-sm mb-6">
              Answers are computed directly with exact mathematical aggregations and verified facts.
            </p>
            <SuggestedQuestions onSelect={handleSend} />
          </div>
        ) : (
          <div className="space-y-4 pb-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                {msg.role === "assistant" && (
                  <div className="h-8 w-8 rounded-full bg-indigo-600 text-white flex items-center justify-center shrink-0 text-xs font-bold">
                    DP
                  </div>
                )}
                <div className="space-y-1 max-w-[80%]">
                  <div
                    className={`p-3.5 rounded-2xl text-sm leading-relaxed ${
                      msg.role === "user"
                        ? "bg-indigo-600 text-white rounded-tr-none"
                        : "bg-muted text-foreground rounded-tl-none border"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{msg.content}</p>

                    {/* Context data badges if present */}
                    {msg.context && Object.keys(msg.context).length > 0 && (
                      <div className="mt-2.5 pt-2 border-t border-muted-foreground/20 text-xs font-mono space-y-1">
                        <p className="font-sans text-[10px] text-muted-foreground uppercase font-semibold">Verified Metrics Context:</p>
                        {Object.entries(msg.context).slice(0, 3).map(([k, v]) => (
                          <div key={k} className="flex justify-between gap-4 text-indigo-700 dark:text-indigo-300">
                            <span>{k}:</span>
                            <span className="font-bold">{typeof v === 'object' ? JSON.stringify(v) : String(v)}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                  <div className={`text-[10px] text-muted-foreground px-1 ${msg.role === "user" ? "text-right" : "text-left"}`}>
                    {msg.timestamp}
                  </div>
                </div>
                {msg.role === "user" && (
                  <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center shrink-0 text-xs text-muted-foreground border">
                    <UserIcon className="h-4 w-4" />
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="flex items-center gap-2 text-muted-foreground text-xs p-3">
                <Loader2 className="h-4 w-4 animate-spin text-indigo-600" />
                <span>DataPilot is querying dataset and computing aggregations...</span>
              </div>
            )}
            <div ref={scrollRef} />
          </div>
        )}
      </ScrollArea>

      <div className="p-3.5 border-t bg-background">
        <form onSubmit={(e) => { e.preventDefault(); handleSend(input); }} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question (e.g. 'What was the total revenue by region?')..."
            disabled={isLoading}
            className="flex-1 text-sm h-11"
          />
          <Button type="submit" disabled={isLoading || !input.trim()} className="bg-indigo-600 hover:bg-indigo-700 text-white h-11 px-5">
            <Send className="h-4 w-4 mr-1.5" /> Send
          </Button>
        </form>
      </div>
    </div>
  );
}
