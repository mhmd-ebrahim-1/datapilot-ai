"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Sparkles, Bot } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { SuggestedQuestions } from "@/components/ai/suggested-questions";
import { ChatMessageItem, ChatMessageData } from "@/components/ai/chat-message";
import { api } from "@/lib/api";
import { useToast } from "@/components/ui/use-toast";

export function ChatInterface({ datasetId }: { datasetId: string }) {
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
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

    const userMessage: ChatMessageData = {
      id: Date.now().toString(),
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await api.post<{ 
        message: string; 
        session_id: string; 
        analysis?: any; 
        context?: any;
        methodology?: string;
      }>("/api/v1/chat/", {
        dataset_id: datasetId,
        message: text,
        session_id: sessionId
      });

      if (res.session_id) {
        setSessionId(res.session_id);
      }

      const assistantMessage: ChatMessageData = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: res.message || "I've analyzed the dataset for your query.",
        analysis: res.analysis || res.context?.analysis,
        methodology: res.methodology,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error: any) {
      toast({
        title: "Analytics Query Failed",
        description: error.message || "Failed to communicate with deterministic query engine.",
        variant: "destructive"
      });
      const errorMessage: ChatMessageData = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I encountered an issue computing the requested metrics for this query. Please check if the requested column exists in your dataset.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full border rounded-xl overflow-hidden bg-card shadow-sm">
      <div className="p-3.5 border-b bg-muted/20 flex items-center justify-between text-xs font-medium">
        <div className="flex items-center gap-2">
          <div className="h-6 w-6 rounded-md bg-indigo-600/10 text-indigo-600 flex items-center justify-center">
            <Sparkles className="h-3.5 w-3.5" />
          </div>
          <div>
            <span className="font-bold text-foreground">Ask DataPilot AI</span>
            <span className="text-muted-foreground ml-2 text-[11px] hidden sm:inline">100% Grounded Deterministic Analytics</span>
          </div>
        </div>
        <span className="text-[11px] text-muted-foreground font-mono bg-muted/60 px-2 py-0.5 rounded border">
          Dataset: {datasetId.slice(0, 8)}...
        </span>
      </div>

      <ScrollArea className="flex-1 p-4 sm:p-6">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full py-12 text-center max-w-lg mx-auto">
            <div className="h-14 w-14 rounded-2xl bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-100 dark:border-indigo-900 flex items-center justify-center text-indigo-600 mb-4 shadow-sm">
              <Bot className="h-7 w-7" />
            </div>
            <h3 className="font-bold text-lg mb-1.5 text-foreground">Ask anything about your dataset</h3>
            <p className="text-xs text-muted-foreground mb-6 leading-relaxed">
              Every answer is calculated directly from your actual records using deterministic Pandas algorithms. The LLM never invents numbers.
            </p>
            <SuggestedQuestions onSelect={handleSend} />
          </div>
        ) : (
          <div className="space-y-6 pb-4">
            {messages.map((msg) => (
              <ChatMessageItem key={msg.id} message={msg} />
            ))}
            {isLoading && (
              <div className="flex items-center gap-2.5 text-muted-foreground text-xs p-3.5 rounded-xl bg-muted/30 border animate-pulse">
                <Loader2 className="h-4 w-4 animate-spin text-indigo-600" />
                <span className="font-medium">DataPilot is querying dataset and computing verified aggregations...</span>
              </div>
            )}
            <div ref={scrollRef} />
          </div>
        )}
      </ScrollArea>

      <div className="p-3.5 border-t bg-background/80 backdrop-blur-sm">
        <form onSubmit={(e) => { e.preventDefault(); handleSend(input); }} className="flex gap-2 max-w-4xl mx-auto">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question (e.g. 'What are the top 5 products by sales?')..."
            disabled={isLoading}
            className="flex-1 text-sm h-11 bg-card border-border/80 focus-visible:ring-indigo-500"
          />
          <Button 
            type="submit" 
            disabled={isLoading || !input.trim()} 
            className="bg-indigo-600 hover:bg-indigo-700 text-white h-11 px-5 font-semibold shadow-sm"
          >
            <Send className="h-4 w-4 mr-1.5" /> Send
          </Button>
        </form>
      </div>
    </div>
  );
}
