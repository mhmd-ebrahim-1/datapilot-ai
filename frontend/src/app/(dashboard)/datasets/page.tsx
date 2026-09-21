"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQueryClient, useMutation } from "@tanstack/react-query";
import { useDatasets } from "@/hooks/use-datasets";
import { PageHeader } from "@/components/common/page-header";
import { LoadingSkeleton } from "@/components/common/loading-skeleton";
import { EmptyState } from "@/components/common/empty-state";
import { StatusBadge } from "@/components/common/status-badge";
import { Database, Plus, Search, Trash2, Eye, ArrowUpRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { useToast } from "@/components/ui/use-toast";
import { api } from "@/lib/api";

export default function DatasetsPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { toast } = useToast();
  const { data: datasets, isLoading } = useDatasets();
  const [search, setSearch] = useState("");

  const deleteDatasetMutation = useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/datasets/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["datasets"] });
      toast({ title: "Dataset deleted successfully" });
    },
    onError: (err: any) => {
      toast({ title: "Failed to delete dataset", description: err.message, variant: "destructive" });
    }
  });

  if (isLoading) return <LoadingSkeleton />;

  const datasetList = datasets || [];
  const filteredDatasets = datasetList.filter(d => 
    d.name.toLowerCase().includes(search.toLowerCase()) ||
    (d.dataset_type && d.dataset_type.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      <PageHeader title="Datasets" description="Manage, explore, and analyze your uploaded CSV and Excel workbooks.">
        <Link href="/datasets/upload">
          <Button className="bg-indigo-600 hover:bg-indigo-700 text-white">
            <Plus className="mr-2 h-4 w-4" /> Upload Dataset
          </Button>
        </Link>
      </PageHeader>

      {datasetList.length === 0 ? (
        <EmptyState
          icon={Database}
          title="No datasets uploaded yet"
          description="Upload your first CSV or Excel file to start generating automated AI insights and interactive dashboards."
          actionLabel="Upload Dataset"
          onAction={() => router.push("/datasets/upload")}
        />
      ) : (
        <div className="space-y-4">
          <div className="flex items-center">
            <div className="relative w-full max-w-sm">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search datasets by name or type..."
                className="pl-8"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
          </div>
          
          <div className="border rounded-lg bg-card overflow-hidden">
            <Table>
              <TableHeader className="bg-muted/50">
                <TableRow>
                  <TableHead>Dataset Name</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Rows</TableHead>
                  <TableHead>Quality Score</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredDatasets.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} className="h-24 text-center text-muted-foreground text-sm">
                      No datasets found matching your search.
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredDatasets.map((dataset) => {
                    const rows = dataset.row_count ?? dataset.rowCount ?? 0;
                    const qScore = dataset.quality_score ?? dataset.qualityScore ?? 100;
                    const dateStr = dataset.created_at || dataset.createdAt || new Date().toISOString();

                    return (
                      <TableRow key={dataset.id} className="hover:bg-muted/30">
                        <TableCell className="font-semibold text-foreground">
                          <Link href={`/datasets/${dataset.id}`} className="hover:underline flex items-center gap-2">
                            <Database className="h-4 w-4 text-indigo-600" />
                            {dataset.name}
                          </Link>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline" className="text-xs">
                            {dataset.dataset_type || "General"}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-muted-foreground">{rows.toLocaleString()}</TableCell>
                        <TableCell>
                          <span className="font-bold text-xs text-indigo-600 dark:text-indigo-400">
                            {qScore.toFixed(1)} / 100
                          </span>
                        </TableCell>
                        <TableCell><StatusBadge status={dataset.status} /></TableCell>
                        <TableCell className="text-xs text-muted-foreground">{formatDate(dateStr)}</TableCell>
                        <TableCell className="text-right space-x-1">
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            onClick={() => router.push(`/datasets/${dataset.id}`)}
                          >
                            <Eye className="h-4 w-4 mr-1" /> View
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            onClick={() => deleteDatasetMutation.mutate(dataset.id)}
                            className="text-destructive hover:bg-destructive/10"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </TableCell>
                      </TableRow>
                    );
                  })
                )}
              </TableBody>
            </Table>
          </div>
        </div>
      )}
    </div>
  );
}
