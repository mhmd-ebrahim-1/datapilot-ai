"use client"

import { cn, formatDate } from "@/lib/utils"

interface ChatMessageProps {
  message: {
    role: "user" | "assistant"
    content: string
    timestamp: string
  }
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user"

  return (
    <div className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}>
      <div className={cn(
        "max-w-[80%] rounded-2xl px-4 py-3 shadow-sm",
        isUser 
          ? "bg-primary text-primary-foreground rounded-br-sm" 
          : "bg-muted text-foreground border rounded-bl-sm"
      )}>
        <p className="text-sm whitespace-pre-wrap leading-relaxed">{message.content}</p>
        <div className={cn(
          "flex items-center text-[10px] mt-2 opacity-70",
          isUser ? "justify-end" : "justify-start"
        )}>
          {!isUser && <span className="mr-2 font-medium">AI-generated</span>}
          <span>{formatDate(message.timestamp)}</span>
        </div>
      </div>
    </div>
  )
}
