"use client"
import { useRouter } from "next/navigation"
import { PageHeader } from "@/components/common/page-header"
import { UploadZone } from "@/components/datasets/upload-zone"
import { useUploadDataset } from "@/hooks/use-datasets"
import { useToast } from "@/components/ui/use-toast"
import { Card, CardContent } from "@/components/ui/card"

export default function UploadDatasetPage() {
  const router = useRouter()
  const { toast } = useToast()
  const uploadMutation = useUploadDataset()

  const handleUpload = async (file: File) => {
    try {
      const result = await uploadMutation.mutateAsync(file)
      toast({
        title: "Upload successful",
        description: "Your dataset has been uploaded and is processing."
      })
      router.push(`/datasets/${(result as any).id || "new"}`)
    } catch (err) {
      toast({
        title: "Upload failed",
        description: "There was an error uploading your file.",
        variant: "destructive"
      })
    }
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <PageHeader title="Upload Dataset" description="Upload a new CSV or Excel file for analysis." />
      
      <Card>
        <CardContent className="pt-6">
          <UploadZone onUpload={handleUpload} isUploading={uploadMutation.isPending} />
        </CardContent>
      </Card>
    </div>
  )
}
