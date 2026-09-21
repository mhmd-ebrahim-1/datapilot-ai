import { Badge } from "@/components/ui/badge"

const statusConfig: Record<string, { label: string; variant: "default" | "secondary" | "destructive" | "outline"; className: string }> = {
  uploaded: { label: "Uploaded", variant: "outline", className: "border-blue-200 bg-blue-50 text-blue-700" },
  processing: { label: "Processing", variant: "outline", className: "border-yellow-200 bg-yellow-50 text-yellow-700" },
  ready: { label: "Ready", variant: "outline", className: "border-green-200 bg-green-50 text-green-700" },
  failed: { label: "Failed", variant: "destructive", className: "" },
  deleted: { label: "Deleted", variant: "secondary", className: "" },
}

export function StatusBadge({ status }: { status: string }) {
  const config = statusConfig[status] || { label: status, variant: "outline" as const, className: "" }
  return <Badge variant={config.variant} className={config.className}>{config.label}</Badge>
}
