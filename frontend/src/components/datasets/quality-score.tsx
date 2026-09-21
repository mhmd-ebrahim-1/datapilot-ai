"use client"
import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { cn } from "@/lib/utils"

interface QualityScoreProps {
  score: number
  completeness: number
  uniqueness: number
  validity: number
  consistency: number
}

function getScoreColor(score: number) {
  if (score >= 90) return "text-emerald-500"
  if (score >= 70) return "text-blue-500"
  if (score >= 50) return "text-amber-500"
  return "text-red-500"
}

export function QualityScore({ score, completeness, uniqueness, validity, consistency }: QualityScoreProps) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex flex-col md:flex-row gap-8 items-center">
          <div className="flex flex-col items-center justify-center p-6 border-4 border-muted rounded-full w-48 h-48 relative">
            <span className={cn("text-5xl font-bold", getScoreColor(score))}>{score}</span>
            <span className="text-sm text-muted-foreground mt-2">Overall Score</span>
          </div>
          
          <div className="flex-1 w-full space-y-6">
            <ScoreBar label="Completeness" value={completeness} />
            <ScoreBar label="Uniqueness" value={uniqueness} />
            <ScoreBar label="Validity" value={validity} />
            <ScoreBar label="Consistency" value={consistency} />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function ScoreBar({ label, value }: { label: string, value: number }) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="font-medium">{label}</span>
        <span className="text-muted-foreground">{value}%</span>
      </div>
      <Progress value={value} className="h-2" />
    </div>
  )
}
