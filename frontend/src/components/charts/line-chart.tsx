"use client"
import { ResponsiveContainer, LineChart as RechartsLine, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface LineChartProps {
  data: Record<string, any>[]
  xKey: string
  yKeys: { key: string; color: string; name?: string }[]
  title?: string
  height?: number
}

export function LineChartComponent({ data, xKey, yKeys, title, height = 300 }: LineChartProps) {
  if (!data?.length) return <div className="flex items-center justify-center h-64 text-muted-foreground">No data available</div>
  
  return (
    <Card>
      {title && <CardHeader className="pb-2"><CardTitle className="text-base">{title}</CardTitle></CardHeader>}
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <RechartsLine data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey={xKey} tick={{ fontSize: 12 }} className="text-muted-foreground" />
            <YAxis tick={{ fontSize: 12 }} className="text-muted-foreground" />
            <Tooltip contentStyle={{ borderRadius: "8px", border: "1px solid hsl(var(--border))" }} />
            <Legend />
            {yKeys.map(({ key, color, name }) => (
              <Line key={key} type="monotone" dataKey={key} stroke={color} name={name || key} strokeWidth={2} dot={false} />
            ))}
          </RechartsLine>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
