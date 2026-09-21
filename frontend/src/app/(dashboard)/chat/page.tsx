"use client"
import { useState } from "react"
import { MessageSquare } from "lucide-react"
import { PageHeader } from "@/components/common/page-header"
import { ChatInterface } from "@/components/ai/chat-interface"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useDatasets } from "@/hooks/use-datasets"

export default function ChatPage() {
  const [selectedDataset, setSelectedDataset] = useState<string>("")
  const { data: datasets } = useDatasets()
  const readyDatasets = (datasets || []).filter((d: any) => d.status === "ready")

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      <div className="p-6 pb-0">
        <PageHeader title="Ask DataPilot" description="Chat with your data using natural language">
          <Select value={selectedDataset} onValueChange={setSelectedDataset}>
            <SelectTrigger className="w-64"><SelectValue placeholder="Select a dataset" /></SelectTrigger>
            <SelectContent>
              {readyDatasets.map((d: any) => (<SelectItem key={d.id} value={d.id}>{d.name}</SelectItem>))}
            </SelectContent>
          </Select>
        </PageHeader>
      </div>
      <div className="flex-1 p-6 pt-4">
        {selectedDataset ? (
          <ChatInterface datasetId={selectedDataset} />
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-muted-foreground border-2 border-dashed rounded-lg">
            <MessageSquare className="h-12 w-12 mb-4 text-muted-foreground/50" />
            <p className="text-lg font-medium">Select a dataset to start chatting</p>
            <p className="text-sm">Choose a dataset from the dropdown above</p>
          </div>
        )}
      </div>
    </div>
  )
}
