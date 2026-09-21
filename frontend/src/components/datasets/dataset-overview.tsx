"use client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Database, FileDigit, FileType, HardDrive, Hash, ShieldCheck, AlertCircle } from "lucide-react"

interface DatasetOverviewProps {
  dataset: any
  profile: any
}

function formatBytes(bytes?: number): string {
  if (!bytes || bytes === 0) return "0 KB"
  const k = 1024
  const sizes = ["Bytes", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i]
}

export function DatasetOverview({ dataset, profile }: DatasetOverviewProps) {
  if (!dataset) return null

  const rowCount = dataset.row_count ?? dataset.rowCount
  const colCount = dataset.column_count ?? dataset.colCount
  const qualityScore = dataset.quality_score ?? profile?.quality_score ?? profile?.qualityScore
  const isFailed = dataset.status === "failed"

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <InfoCard icon={FileType} title="File Name" value={dataset.original_filename || dataset.name} />
      <InfoCard icon={Database} title="Dataset Domain" value={dataset.dataset_type || "General"} />
      <InfoCard 
        icon={Hash} 
        title="Rows" 
        value={isFailed ? "Failed" : rowCount !== undefined && rowCount !== null ? Number(rowCount).toLocaleString() : "Processing..."} 
      />
      <InfoCard 
        icon={FileDigit} 
        title="Columns" 
        value={isFailed ? "Failed" : colCount !== undefined && colCount !== null ? Number(colCount).toLocaleString() : "Processing..."} 
      />
      <InfoCard icon={HardDrive} title="File Size" value={formatBytes(dataset.file_size)} />
      <InfoCard 
        icon={isFailed ? AlertCircle : ShieldCheck} 
        title="Quality Score" 
        value={isFailed ? "N/A" : qualityScore !== undefined && qualityScore !== null ? `${Number(qualityScore).toFixed(1)}/100` : "Calculating..."} 
      />
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
