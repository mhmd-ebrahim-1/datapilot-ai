"use client"
import { Button } from "@/components/ui/button"

const questions = [
  "What was our total revenue?",
  "Which product sold the most?",
  "What are the main trends?",
  "Show me unusual values",
  "Which region performed best?",
  "What should we investigate?"
]

export function SuggestedQuestions({ onSelect }: { onSelect: (q: string) => void }) {
  return (
    <div className="flex flex-wrap justify-center gap-2 max-w-2xl">
      {questions.map((q, i) => (
        <Button 
          key={i} 
          variant="outline" 
          className="rounded-full bg-background"
          onClick={() => onSelect(q)}
        >
          {q}
        </Button>
      ))}
    </div>
  )
}
