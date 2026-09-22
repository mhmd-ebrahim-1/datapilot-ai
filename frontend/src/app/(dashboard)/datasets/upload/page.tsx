"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { PageHeader } from "@/components/common/page-header"
import { UploadZone } from "@/components/datasets/upload-zone"
import { useUploadDataset } from "@/hooks/use-datasets"
import { useDirectUploadDataset } from "@/hooks/use-datasets"
import { useToast } from "@/components/ui/use-toast"
import { Card, CardContent } from "@/components/ui/card"
import { ShieldCheck, Zap, Database, ArrowRight } from "lucide-react"

export default function UploadDatasetPage() {
  const router = useRouter()
  const { toast } = useToast()
  const uploadMutation = useUploadDataset()
  const uploadMutation = useDirectUploadDataset()
  const [progress, setProgress] = useState(0)
  const [statusText, setStatusText] = useState("")

  const handleUpload = async (file: File) => {
    try {
      const result = await uploadMutation.mutateAsync(file)
      const result = await uploadMutation.mutateAsync({
        file,
        onProgress: (pct, msg) => {
          setProgress(pct)
          setStatusText(msg)
        }
      })
      toast({
        title: "Upload successful",
        description: "Your dataset has been uploaded and is processing."
        title: "Dataset Ready",
        description: `Successfully analyzed ${result.name || "dataset"}.`
      })
      router.push(`/datasets/${(result as any).id || "new"}`)
    } catch (err) {
      router.push(`/datasets/${result.id || "new"}`)
    } catch (err: any) {
      toast({
        title: "Upload failed",
        description: "There was an error uploading your file.",
        description: err.message || "There was an error uploading and analyzing your file.",
        variant: "destructive"
      })
      setProgress(0)
      setStatusText("")
    }
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <PageHeader title="Upload Dataset" description="Upload a new CSV or Excel file for analysis." />
      <PageHeader 
        title="Upload Dataset" 
        description="Upload CSV, XLSX, or XLS files up to 50 MB for instant automated profiling and analysis." 
      />
      
      <Card>
        <CardContent className="pt-6">
          <UploadZone onUpload={handleUpload} isUploading={uploadMutation.isPending} />
          <UploadZone 
            onUpload={handleUpload} 
            isUploading={uploadMutation.isPending}
            progress={progress}
            statusText={statusText}
          />
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
        <div className="p-4 rounded-lg bg-card border flex items-start gap-3">
          <ShieldCheck className="w-5 h-5 text-indigo-600 mt-0.5 shrink-0" />
          <div className="text-xs">
            <p className="font-semibold text-foreground">Secure Direct Upload</p>
            <p className="text-muted-foreground mt-0.5">Encrypted short-lived signed tokens directly to isolated cloud storage.</p>
          </div>
        </div>

        <div className="p-4 rounded-lg bg-card border flex items-start gap-3">
          <Zap className="w-5 h-5 text-indigo-600 mt-0.5 shrink-0" />
          <div className="text-xs">
            <p className="font-semibold text-foreground">Deterministic Analytics</p>
            <p className="text-muted-foreground mt-0.5">Automated 4-pillar data quality scoring, KPIs, and anomaly detection.</p>
          </div>
        </div>

        <div className="p-4 rounded-lg bg-card border flex items-start gap-3">
          <Database className="w-5 h-5 text-indigo-600 mt-0.5 shrink-0" />
          <div className="text-xs">
            <p className="font-semibold text-foreground">Multi-Format Engine</p>
            <p className="text-muted-foreground mt-0.5">Native parsing support for CSV, modern XLSX, and legacy Excel (.XLS).</p>
          </div>
        </div>
      </div>
    </div>
  )
}
