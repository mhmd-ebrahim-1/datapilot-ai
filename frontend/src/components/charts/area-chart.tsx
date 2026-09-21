"use client"
import { ResponsiveContainer, AreaChart as RechartsArea, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface AreaChartProps {
  data: Record<string, any>[]
  xKey: string
  yKeys: { key: string; color: string; name?: string }[]
  title?: string
  height?: number
}

export function AreaChartComponent({ data, xKey, yKeys, title, height = 300 }: AreaChartProps) {
  if (!data?.length) return <div className="flex items-center justify-center h-64 text-muted-foreground">No data available</div>
  
  return (
    <Card>
      {title && <CardHeader className="pb-2"><CardTitle className="text-base">{title}</CardTitle></CardHeader>}
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <RechartsArea data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <defs>
              {yKeys.map(({ key, color }) => (
                <linearGradient key={`color${key}`} id={`color${key}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={color} stopOpacity={0.3}/>
                  <stop offset="95%" stopColor={color} stopOpacity={0}/>
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey={xKey} tick={{ fontSize: 12 }} className="text-muted-foreground" />
            <YAxis tick={{ fontSize: 12 }} className="text-muted-foreground" />
            <Tooltip contentStyle={{ borderRadius: "8px", border: "1px solid hsl(var(--border))" }} />
            <Legend />
            {yKeys.map(({ key, color, name }) => (
              <Area key={key} type="monotone" dataKey={key} stroke={color} fillOpacity={1} fill={`url(#color${key})`} name={name || key} />
            ))}
          </RechartsArea>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
