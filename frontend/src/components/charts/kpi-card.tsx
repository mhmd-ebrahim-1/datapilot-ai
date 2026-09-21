"use client"
import { Card, CardContent } from "@/components/ui/card"
import { LucideIcon, TrendingUp, TrendingDown } from "lucide-react"
import { cn } from "@/lib/utils"

interface KpiCardProps {
  title: string
  value: string | number
  change?: number
  changeLabel?: string
  icon?: LucideIcon
  color?: "blue" | "green" | "purple" | "amber" | "red"
}

const colorMap = {
  blue: "bg-blue-50 text-blue-600",
  green: "bg-emerald-50 text-emerald-600",
  purple: "bg-purple-50 text-purple-600",
  amber: "bg-amber-50 text-amber-600",
  red: "bg-red-50 text-red-600",
}

export function KpiCard({ title, value, change, changeLabel, icon: Icon, color = "blue" }: KpiCardProps) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          {Icon && <div className={cn("rounded-lg p-2", colorMap[color])}><Icon className="h-4 w-4" /></div>}
        </div>
        <div className="mt-2">
          <p className="text-2xl font-bold">{typeof value === 'number' ? value.toLocaleString() : value}</p>
          {change !== undefined && (
            <div className="flex items-center mt-1 text-xs">
              {change >= 0 ? <TrendingUp className="h-3 w-3 text-emerald-500 mr-1" /> : <TrendingDown className="h-3 w-3 text-red-500 mr-1" />}
              <span className={change >= 0 ? "text-emerald-500" : "text-red-500"}>{change >= 0 ? "+" : ""}{change.toFixed(1)}%</span>
              {changeLabel && <span className="text-muted-foreground ml-1">{changeLabel}</span>}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
