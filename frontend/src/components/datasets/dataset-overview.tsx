"use client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Database, FileDigit, FileType, HardDrive, Hash, ShieldCheck } from "lucide-react"

interface DatasetOverviewProps {
  dataset: any
  profile: any
}

export function DatasetOverview({ dataset, profile }: DatasetOverviewProps) {
  if (!dataset) return null

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <InfoCard icon={FileType} title="File Name" value={dataset.name} />
      <InfoCard icon={Database} title="Dataset Type" value={dataset.name.endsWith('.csv') ? 'CSV' : 'Excel'} />
      <InfoCard icon={Hash} title="Rows" value={dataset.rowCount?.toLocaleString() || '0'} />
      <InfoCard icon={FileDigit} title="Columns" value={dataset.colCount?.toLocaleString() || '0'} />
      <InfoCard icon={HardDrive} title="Size" value="12 MB" />
      <InfoCard icon={ShieldCheck} title="Quality Score" value={`${profile?.qualityScore || 0}%`} />
    </div>
  )
}

function InfoCard({ icon: Icon, title, value }: { icon: any, title: string, value: string | number }) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold truncate">{value}</div>
      </CardContent>
    </Card>
  )
}
