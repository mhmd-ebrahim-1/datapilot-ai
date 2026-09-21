"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { PageHeader } from "@/components/common/page-header";
import { EmptyState } from "@/components/common/empty-state";
import { FileText, Download, Trash2, Plus, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useDatasets } from "@/hooks/use-datasets";
import { useToast } from "@/components/ui/use-toast";
import { api } from "@/lib/api";

export default function ReportsPage() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedDataset, setSelectedDataset] = useState("");
  const [reportTitle, setReportTitle] = useState("");

  const { data: datasets } = useDatasets();
  const readyDatasets = (datasets || []).filter((d: any) => d.status === "ready");

  const { data: reports, isLoading } = useQuery({
    queryKey: ["reports-list"],
    queryFn: () => api.get<any[]>("/api/v1/reports")
  });

  const createReportMutation = useMutation({
    mutationFn: (body: { dataset_id: string; title: string }) => api.post<any>("/api/v1/reports/", body),
    onSuccess: (newReport) => {
      queryClient.invalidateQueries({ queryKey: ["reports-list"] });
      setIsDialogOpen(false);
      setReportTitle("");
      setSelectedDataset("");
      toast({
        title: "Report Generated",
        description: "Your PDF report is ready for download."
      });
      // Download right away
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      window.open(`${baseUrl}/api/v1/reports/${newReport.id}/download`, "_blank");
    },
    onError: (err: any) => {
      toast({
        title: "Failed to generate report",
        description: err.message || "An error occurred.",
        variant: "destructive"
      });
    }
  });

  const deleteReportMutation = useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/reports/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reports-list"] });
      toast({ title: "Report deleted" });
    }
  });

  const handleDownload = (reportId: string) => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    window.open(`${baseUrl}/api/v1/reports/${reportId}/download`, "_blank");
  };

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedDataset) {
      toast({ title: "Please select a dataset", variant: "destructive" });
      return;
    }
    createReportMutation.mutate({
      dataset_id: selectedDataset,
      title: reportTitle.trim() || "Executive Dataset Report"
    });
  };

  const reportList = reports || [];

  return (
    <div className="space-y-6">
      <PageHeader title="Executive Reports" description="Generated executive summaries, KPI audits, and PDF exports">
        <Button onClick={() => setIsDialogOpen(true)} className="bg-indigo-600 hover:bg-indigo-700 text-white">
          <Plus className="h-4 w-4 mr-2" /> Generate Report
        </Button>
      </PageHeader>

      {isLoading ? (
        <div className="py-16 text-center text-muted-foreground text-sm flex items-center justify-center gap-2">
          <Loader2 className="h-4 w-4 animate-spin text-indigo-600" />
          <span>Loading reports...</span>
        </div>
      ) : reportList.length === 0 ? (
        <EmptyState
          icon={FileText}
          title="No reports generated"
          description="Create your first executive report to share data-driven conclusions with leadership."
          actionLabel="Generate Report"
          onAction={() => setIsDialogOpen(true)}
        />
      ) : (
        <div className="border rounded-lg bg-card overflow-hidden">
          <Table>
            <TableHeader className="bg-muted/50">
              <TableRow>
                <TableHead>Report Title</TableHead>
                <TableHead>Dataset</TableHead>
                <TableHead>Format</TableHead>
                <TableHead>Generated At</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {reportList.map((report) => (
                <TableRow key={report.id} className="hover:bg-muted/30">
                  <TableCell className="font-semibold text-foreground flex items-center gap-2">
                    <FileText className="h-4 w-4 text-indigo-600" />
                    {report.title}
                  </TableCell>
                  <TableCell className="text-muted-foreground">{report.dataset_name || "Dataset"}</TableCell>
                  <TableCell>
                    <span className="px-2 py-0.5 text-[10px] font-bold uppercase rounded bg-indigo-50 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300">
                      {report.format || "PDF"}
                    </span>
                  </TableCell>
                  <TableCell className="text-muted-foreground text-xs">
                    {new Date(report.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </TableCell>
                  <TableCell className="text-right space-x-1">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      onClick={() => handleDownload(report.id)}
                      className="text-xs"
                    >
                      <Download className="h-3.5 w-3.5 mr-1" /> Download
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      onClick={() => deleteReportMutation.mutate(report.id)}
                      className="text-destructive hover:bg-destructive/10"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}

      {/* Generate Report Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Generate Executive PDF Report</DialogTitle>
            <DialogDescription>
              Select a dataset to compile an executive briefing with KPIs, distribution charts, and AI insights.
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleCreate} className="space-y-4 py-2">
            <div className="space-y-2">
              <Label>Select Target Dataset</Label>
              <Select value={selectedDataset} onValueChange={setSelectedDataset}>
                <SelectTrigger>
                  <SelectValue placeholder="Choose a ready dataset..." />
                </SelectTrigger>
                <SelectContent>
                  {readyDatasets.map((d: any) => (
                    <SelectItem key={d.id} value={d.id}>{d.name} ({d.dataset_type || "General"})</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Report Title (Optional)</Label>
              <Input
                placeholder="e.g. Q3 Sales & Performance Review"
                value={reportTitle}
                onChange={(e) => setReportTitle(e.target.value)}
              />
            </div>
            <DialogFooter className="pt-4">
              <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" disabled={createReportMutation.isPending || !selectedDataset} className="bg-indigo-600 hover:bg-indigo-700 text-white">
                {createReportMutation.isPending ? "Generating PDF..." : "Generate & Download"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
