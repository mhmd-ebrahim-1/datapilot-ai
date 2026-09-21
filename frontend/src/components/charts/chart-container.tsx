"use client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { AlertCircle } from "lucide-react"

interface ChartContainerProps {
  title?: string
  isLoading?: boolean
  error?: Error | null
  isEmpty?: boolean
  children: React.ReactNode
}

export function ChartContainer({ title, isLoading, error, isEmpty, children }: ChartContainerProps) {
  return (
    <Card>
      {title && (
        <CardHeader className="pb-2">
          <CardTitle className="text-base">{title}</CardTitle>
        </CardHeader>
      )}
      <CardContent>
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <Skeleton className="w-full h-full" />
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center h-64 text-destructive">
            <AlertCircle className="h-8 w-8 mb-2" />
            <p>Failed to load chart data</p>
          </div>
        ) : isEmpty ? (
          <div className="flex items-center justify-center h-64 text-muted-foreground">
            <p>No data available</p>
          </div>
        ) : (
          <div className="h-64">
            {children}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
