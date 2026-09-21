"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Database, FileText, Activity, Brain, ArrowUpRight, Upload, Sparkles } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { useDatasets } from "@/hooks/use-datasets";
import { StatusBadge } from "@/components/common/status-badge";
import { LoadingSkeleton } from "@/components/common/loading-skeleton";
import { api } from "@/lib/api";

export default function DashboardPage() {
  const { data: datasets, isLoading: datasetsLoading } = useDatasets();
  
  const { data: usageData } = useQuery({
    queryKey: ["billing-usage"],
    queryFn: () => api.get<any>("/api/v1/billing/usage").catch(() => null)
  });

  const { data: reportsData } = useQuery({
    queryKey: ["reports-list"],
    queryFn: () => api.get<any[]>("/api/v1/reports").catch(() => [])
  });

  const datasetList = datasets || [];
  const totalDatasets = datasetList.length;
  const readyDatasets = datasetList.filter((d: any) => d.status === "ready");
  const totalRows = readyDatasets.reduce((acc: number, d: any) => acc + (d.row_count || 0), 0);
  const avgQuality = readyDatasets.length > 0 
    ? (readyDatasets.reduce((acc: number, d: any) => acc + (d.quality_score || 0), 0) / readyDatasets.length).toFixed(1)
    : "100.0";

  const totalReports = reportsData?.length || 0;
  const analysesRun = usageData?.analyses?.used || 0;

  if (datasetsLoading) {
    return <LoadingSkeleton />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Intelligence Dashboard</h1>
          <p className="text-muted-foreground">Real-time overview of your datasets, automated insights, and analyses.</p>
        </div>
        <Link href="/datasets/upload">
          <Button className="bg-indigo-600 hover:bg-indigo-700 text-white">
            <Upload className="mr-2 h-4 w-4" /> Upload Dataset
          </Button>
        </Link>
      </div>

      {/* Dynamic Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard 
          title="Total Datasets" 
          value={totalDatasets} 
          icon={Database} 
          trend={`${readyDatasets.length} ready for analysis`} 
          highlight="blue"
        />
        <StatCard 
          title="Analyses Run" 
          value={analysesRun} 
          icon={Activity} 
          trend={`${usageData?.plan ? `${usageData.plan.toUpperCase()} plan` : "Active"}`} 
          highlight="indigo"
        />
        <StatCard 
          title="Avg Data Quality" 
          value={`${avgQuality}%`} 
          icon={Brain} 
          trend={`${totalRows.toLocaleString()} rows profiled`} 
          highlight="emerald"
        />
        <StatCard 
          title="Reports Generated" 
          value={totalReports} 
          icon={FileText} 
          trend={`${totalReports} PDF exports`} 
          highlight="purple"
        />
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
        {/* Recent Datasets Table */}
        <Card className="col-span-4">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Recent Datasets</CardTitle>
              <CardDescription>Your recently uploaded CSV and Excel workbooks</CardDescription>
            </div>
            <Link href="/datasets" className="text-xs font-semibold text-indigo-600 hover:underline">
              View All
            </Link>
          </CardHeader>
          <CardContent>
            {datasetList.length === 0 ? (
              <div className="text-sm text-center py-10 text-muted-foreground border-2 border-dashed rounded-lg">
                <Database className="h-8 w-8 mx-auto text-muted-foreground mb-2" />
                <p className="font-medium">No datasets uploaded yet.</p>
                <Link href="/datasets/upload" className="text-indigo-600 hover:underline text-xs mt-1 inline-block">
                  Upload your first dataset
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {datasetList.slice(0, 5).map((d: any) => (
                  <div key={d.id} className="flex items-center justify-between p-3 rounded-lg border bg-card hover:bg-muted/40 transition-colors">
                    <div className="flex items-center gap-3">
                      <div className="h-9 w-9 rounded-md bg-indigo-50 dark:bg-indigo-950 flex items-center justify-center text-indigo-600 font-bold text-xs">
                        CSV
                      </div>
                      <div>
                        <Link href={`/datasets/${d.id}`} className="text-sm font-semibold hover:underline text-foreground">
                          {d.name}
                        </Link>
                        <p className="text-xs text-muted-foreground">
                          {d.dataset_type || "General"} • {d.row_count ? `${d.row_count} rows` : "Processing"}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <StatusBadge status={d.status} />
                      <Link href={`/datasets/${d.id}`}>
                        <Button variant="ghost" size="sm">
                          <ArrowUpRight className="h-4 w-4" />
                        </Button>
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick Actions & AI Shortcuts */}
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Fast shortcuts for your analytics workflows</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Link href="/datasets/upload" className="block">
              <Button className="w-full justify-start h-12 text-sm font-medium" variant="outline">
                <Upload className="mr-3 h-4 w-4 text-indigo-600" /> Upload Excel or CSV
              </Button>
            </Link>
            <Link href="/chat" className="block">
              <Button className="w-full justify-start h-12 text-sm font-medium" variant="outline">
                <Sparkles className="mr-3 h-4 w-4 text-indigo-600" /> Ask DataPilot AI
              </Button>
            </Link>
            <Link href="/reports" className="block">
              <Button className="w-full justify-start h-12 text-sm font-medium" variant="outline">
                <FileText className="mr-3 h-4 w-4 text-indigo-600" /> Generate Executive PDF Report
              </Button>
            </Link>
            <Link href="/settings" className="block">
              <Button className="w-full justify-start h-12 text-sm font-medium" variant="outline">
                <Brain className="mr-3 h-4 w-4 text-indigo-600" /> Workspace & Billing Limits
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, trend }: any) {
  return (
    <Card className="hover:shadow-sm transition-shadow">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        <div className="h-8 w-8 rounded-lg bg-muted flex items-center justify-center text-muted-foreground">
          <Icon className="h-4 w-4" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold tracking-tight">{value}</div>
        <p className="text-xs text-muted-foreground mt-1">{trend}</p>
      </CardContent>
    </Card>
  );
}
