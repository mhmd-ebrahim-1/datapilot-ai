"use client"
import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { CloudUpload, File as FileIcon, X } from 'lucide-react'
import { CloudUpload, File as FileIcon, X, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface UploadZoneProps {
  onUpload: (file: File) => void
  isUploading: boolean
  progress?: number
  statusText?: string
}

export function UploadZone({ onUpload, isUploading }: UploadZoneProps) {
export function UploadZone({ onUpload, isUploading, progress = 0, statusText = "" }: UploadZoneProps) {
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  
  const onDrop = useCallback((acceptedFiles: File[]) => {
  const onDrop = useCallback((acceptedFiles: File[], fileRejections: any[]) => {
    setError(null)
    if (fileRejections.length > 0) {
      const rej = fileRejections[0]
      if (rej.file.size > 50 * 1024 * 1024) {
        setError(`File exceeds maximum allowed size of 50 MB (${(rej.file.size / (1024 * 1024)).toFixed(1)} MB).`)
      } else {
        setError("Invalid file format. Only CSV (.csv) and Excel (.xlsx, .xls) files are supported.")
      }
      return
    }
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
      const selected = acceptedFiles[0]
      if (selected.size > 50 * 1024 * 1024) {
        setError(`File exceeds maximum allowed size of 50 MB (${(selected.size / (1024 * 1024)).toFixed(1)} MB).`)
        return
      }
      setFile(selected)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    maxFiles: 1,
    maxSize: 50 * 1024 * 1024,
    disabled: isUploading
  })

  return (
    <div className="w-full">
    <div className="w-full space-y-4">
      {error && (
        <div className="p-3 bg-destructive/10 border border-destructive/20 text-destructive text-sm rounded-lg flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {!file ? (
        <div
          {...getRootProps()}
          className={cn(
            "flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer transition-colors",
            isDragActive ? "border-primary bg-primary/5" : "border-muted-foreground/25 hover:bg-muted/50",
            isDragReject && "border-destructive bg-destructive/5"
            (isDragReject || error) && "border-destructive bg-destructive/5"
          )}
        >
          <input {...getInputProps()} />
          <CloudUpload className={cn("w-10 h-10 mb-4", isDragActive ? "text-primary" : "text-muted-foreground")} />
          <p className="mb-2 text-sm font-semibold">
            {isDragActive ? "Drop the file here" : "Drag & drop your file here"}
          </p>
          <p className="text-xs text-muted-foreground">or click to browse</p>
          <div className="mt-4 flex gap-2">
            <span className="text-xs bg-muted px-2 py-1 rounded">.csv</span>
            <span className="text-xs bg-muted px-2 py-1 rounded">.xlsx</span>
            <span className="text-xs bg-muted px-2 py-1 rounded">.xls</span>
          <p className="text-xs text-muted-foreground">or click to browse from your device</p>
          <div className="mt-4 flex items-center gap-2">
            <span className="text-xs font-mono bg-muted px-2 py-1 rounded">.csv</span>
            <span className="text-xs font-mono bg-muted px-2 py-1 rounded">.xlsx</span>
            <span className="text-xs font-mono bg-muted px-2 py-1 rounded">.xls (Legacy Excel)</span>
          </div>
          <p className="mt-3 text-[11px] text-muted-foreground">Direct cloud upload supported up to 50 MB</p>
        </div>
      ) : (
        <div className="flex items-center justify-between p-4 border rounded-lg">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-primary/10 rounded-lg text-primary">
              <FileIcon className="w-6 h-6" />
        <div className="p-5 border rounded-xl bg-card shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3.5">
              <div className="p-2.5 bg-primary/10 rounded-lg text-primary">
                <FileIcon className="w-6 h-6" />
              </div>
              <div>
                <p className="font-medium text-sm text-foreground">{file.name}</p>
                <p className="text-xs text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            </div>
            <div>
              <p className="font-medium text-sm">{file.name}</p>
              <p className="text-xs text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            
            <div className="flex items-center space-x-2">
              {!isUploading && (
                <Button variant="ghost" size="icon" onClick={() => { setFile(null); setError(null); }}>
                  <X className="w-4 h-4" />
                </Button>
              )}
              <Button 
                onClick={() => onUpload(file)} 
                disabled={isUploading}
                className="gap-2"
              >
                {isUploading && <Loader2 className="w-4 h-4 animate-spin" />}
                {isUploading ? "Uploading & Analyzing..." : "Start Analysis"}
              </Button>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {!isUploading && (
              <Button variant="ghost" size="icon" onClick={() => setFile(null)}>
                <X className="w-4 h-4" />
              </Button>
            )}
            <Button onClick={() => onUpload(file)} disabled={isUploading}>
              {isUploading ? "Uploading..." : "Upload File"}
            </Button>
          </div>

          {isUploading && (
            <div className="space-y-2 pt-2 border-t">
              <div className="flex justify-between items-center text-xs font-medium">
                <span className="text-muted-foreground">{statusText || "Processing dataset..."}</span>
                <span className="text-primary">{progress}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
