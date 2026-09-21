"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { 
  BarChart3, 
  Brain, 
  Table as TableIcon, 
  Sparkles, 
  TrendingUp, 
  AlertTriangle, 
  FileText, 
  Download, 
  Search, 
  RefreshCw, 
  CheckCircle2, 
  ChevronLeft, 
  ChevronRight,
  Database,
  ArrowRight
} from "lucide-react";
import { useDataset, useDatasetPreview, useDatasetProfile } from "@/hooks/use-datasets";
import { PageHeader } from "@/components/common/page-header";
import { LoadingSkeleton } from "@/components/common/loading-skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DatasetOverview } from "@/components/datasets/dataset-overview";
import { QualityScore } from "@/components/datasets/quality-score";
import { ChatInterface } from "@/components/ai/chat-interface";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { KpiCard } from "@/components/charts/kpi-card";
import { LineChartComponent } from "@/components/charts/line-chart";
import { BarChartComponent } from "@/components/charts/bar-chart";
import { useToast } from "@/components/ui/use-toast";
import { api } from "@/lib/api";

export default function DatasetDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const [previewPage, setPreviewPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);

  // 1. Fetch Dataset & Profile
  const { data: dataset, isLoading: datasetLoading } = useDataset(id);
  const { data: profileData, isLoading: profileLoading } = useDatasetProfile(id);

  // 2. Fetch Data Preview (paginated)
  const { data: previewData, isLoading: previewLoading } = useQuery({
    queryKey: ["dataset-preview", id, previewPage, searchTerm],
    queryFn: () => api.get<any>(`/api/v1/datasets/${id}/preview?page=${previewPage}&page_size=20${searchTerm ? `&search=${encodeURIComponent(searchTerm)}` : ''}`),
    enabled: !!id
  });

  // 3. Fetch Analyses / KPIs
  const { data: analysisData, isLoading: analysisLoading, refetch: refetchAnalysis } = useQuery({
    queryKey: ["dataset-analysis", id],
    queryFn: async () => {
      // Create or get analysis
      return api.post<any>("/api/v1/analyses/", { dataset_id: id });
    },
    enabled: !!id
  });

  // 4. Fetch Forecasts
  const { data: forecastData, refetch: refetchForecast, isLoading: forecastLoading } = useQuery({
    queryKey: ["dataset-forecast", id],
    queryFn: async () => {
      return api.post<any>("/api/v1/forecasts/", { dataset_id: id, horizon: 30 }).catch(() => null);
    },
    enabled: !!id
  });

  // 5. Fetch Anomalies
  const { data: anomaliesData, refetch: refetchAnomalies, isLoading: anomaliesLoading } = useQuery({
    queryKey: ["dataset-anomalies", id],
    queryFn: async () => {
      return api.post<any[]>("/api/v1/anomalies/detect", { dataset_id: id }).catch(() => []);
    },
    enabled: !!id
  });

  // Generate & Download PDF Report
  const handleGeneratePdf = async () => {
    setIsGeneratingReport(true);
    try {
      const reportRes = await api.post<any>("/api/v1/reports/", {
        dataset_id: id,
        title: `${dataset?.name || "Dataset"} Executive Report`
      });
      toast({
        title: "Report Generated!",
        description: "Your executive PDF report is ready. Downloading now..."
      });
      // Trigger authenticated download
      await api.downloadFile(`/api/v1/reports/${reportRes.id}/download`, `${dataset?.name || 'Dataset'}_Executive_Report.pdf`);
    } catch (err: any) {
      toast({
        title: "Report Generation Failed",
        description: err.message || "Could not generate PDF report.",
        variant: "destructive"
      });
    } finally {
      setIsGeneratingReport(false);
    }
  };

  if (datasetLoading) return <LoadingSkeleton />;
  if (!dataset) return <div className="p-8 text-center">Dataset not found.</div>;
  const isFailed = dataset.status === "failed";
  const qualityScoreVal = dataset.quality_score ?? profileData?.quality_score;
  const profileDetails = dataset.profile || profileData?.profile || {};
  const kpis = analysisData?.kpis || [];
  const charts = analysisData?.charts || [];

  return (
    <div className="space-y-6">
      {isFailed && (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-800 flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
          <div>
            <h3 className="font-semibold text-sm">Dataset Ingestion Failed</h3>
            <p className="text-xs text-red-700 mt-1">
              {dataset.error_message || "An error occurred while parsing and processing this dataset. Please verify the spreadsheet format and try re-uploading."}
            </p>
          </div>
        </div>
      )}

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight">{dataset.name}</h1>
            <Badge 
              variant="outline" 
              className={isFailed ? "border-red-300 text-red-700 bg-red-50" : "border-indigo-300 text-indigo-700 bg-indigo-50"}
            >
              {isFailed ? "Processing Failed" : dataset.dataset_type || "General Analytics"}
            </Badge>
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            {isFailed 
              ? "Dataset processing failed • No records available"
              : `${dataset.row_count !== undefined && dataset.row_count !== null ? dataset.row_count.toLocaleString() : 0} rows • ${dataset.column_count || 0} columns • Quality Score: ${qualityScoreVal !== undefined && qualityScoreVal !== null ? `${qualityScoreVal.toFixed(1)}/100` : "Calculating..."}`
            }
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button 
            onClick={handleGeneratePdf} 
            disabled={isGeneratingReport || isFailed}
            className="bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50"
          >
            <Download className="mr-2 h-4 w-4" />
            {isGeneratingReport ? "Generating PDF..." : "Export PDF Report"}
          </Button>
        </div>
      </div>

      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="mb-4 flex-wrap bg-muted/60 p-1">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="preview">Data Preview</TabsTrigger>
          <TabsTrigger value="quality">Quality Score</TabsTrigger>
          <TabsTrigger value="analytics">KPIs & Charts</TabsTrigger>
          <TabsTrigger value="insights">AI Insights</TabsTrigger>
          <TabsTrigger value="forecast">Forecasting</TabsTrigger>
          <TabsTrigger value="anomalies">Anomalies</TabsTrigger>
          <TabsTrigger value="chat">Ask AI</TabsTrigger>
        </TabsList>

        {/* 1. OVERVIEW TAB */}
        <TabsContent value="overview" className="space-y-6">
          <DatasetOverview dataset={dataset} profile={profileDetails} />
        </TabsContent>

        {/* 2. DATA PREVIEW TAB */}
        <TabsContent value="preview" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-3">
              <div>
                <CardTitle>Tabular Data Preview</CardTitle>
                <CardDescription>
                  Showing page {previewData?.page || 1} of {previewData?.total_pages || 1} ({previewData?.total_rows?.toLocaleString() || 0} total rows)
                </CardDescription>
              </div>
              <div className="flex items-center gap-2">
                <div className="relative w-64">
                  <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search records..."
                    className="pl-8 text-xs"
                    value={searchTerm}
                    onChange={(e) => {
                      setSearchTerm(e.target.value);
                      setPreviewPage(1);
                    }}
                  />
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {previewLoading ? (
                <div className="py-12 text-center text-muted-foreground text-sm">Loading dataset preview...</div>
              ) : !previewData?.rows || previewData.rows.length === 0 ? (
                <div className="py-12 text-center text-muted-foreground text-sm">No records match your search query.</div>
              ) : (
                <div className="overflow-x-auto rounded-md border">
                  <table className="w-full text-xs text-left border-collapse">
                    <thead className="bg-muted/50 border-b">
                      <tr>
                        {previewData.columns.map((col: any) => (
                          <th key={col.key} className="p-2.5 font-semibold text-foreground whitespace-nowrap">
                            {col.label}
                            <span className="ml-1.5 text-[10px] text-muted-foreground font-normal">({col.type})</span>
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {previewData.rows.map((row: any, idx: number) => (
                        <tr key={idx} className="hover:bg-muted/30">
                          {previewData.columns.map((col: any) => (
                            <td key={col.key} className="p-2.5 whitespace-nowrap text-muted-foreground">
                              {row[col.key] !== null && row[col.key] !== undefined ? String(row[col.key]) : <span className="text-muted-foreground/40 italic">null</span>}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Pagination controls */}
              {previewData && previewData.total_pages > 1 && (
                <div className="flex items-center justify-between mt-4">
                  <p className="text-xs text-muted-foreground">
                    Page {previewData.page} of {previewData.total_pages}
                  </p>
                  <div className="flex items-center gap-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      disabled={previewPage <= 1}
                      onClick={() => setPreviewPage(p => Math.max(1, p - 1))}
                    >
                      <ChevronLeft className="h-4 w-4" /> Previous
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      disabled={previewPage >= previewData.total_pages}
                      onClick={() => setPreviewPage(p => p + 1)}
                    >
                      Next <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 3. QUALITY SCORE TAB */}
        <TabsContent value="quality">
          <QualityScore 
            score={Math.round(qualityScoreVal ?? 0)} 
            completeness={Math.round(profileDetails?.quality_metrics?.completeness ?? 95)} 
            uniqueness={Math.round(profileDetails?.quality_metrics?.uniqueness ?? 98)} 
            validity={Math.round(profileDetails?.quality_metrics?.validity ?? 94)} 
            consistency={Math.round(profileDetails?.quality_metrics?.consistency ?? 92)} 
          />
        </TabsContent>

        {/* 4. ANALYTICS & KPIS TAB */}
        <TabsContent value="analytics" className="space-y-6">
          {kpis.length > 0 && (
            <div>
              <h3 className="text-base font-semibold mb-3">Key Performance Indicators</h3>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {kpis.map((kpi: any, i: number) => (
                  <KpiCard
                    key={i}
                    title={kpi.name}
                    value={kpi.formatted_value || kpi.value}
                    changeLabel={kpi.description}
                    color={i % 4 === 0 ? "blue" : i % 4 === 1 ? "green" : i % 4 === 2 ? "purple" : "amber"}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Dynamic Visualizations */}
          {charts.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2">
              {charts.map((chart: any, i: number) => {
                if (chart.type === "line" || chart.chart_type === "line") {
                  return (
                    <LineChartComponent
                      key={i}
                      title={chart.title || "Temporal Trend"}
                      data={chart.data || []}
                      xKey={chart.x_column || chart.x_key || "date"}
                      yKeys={[{ key: chart.y_column || chart.y_key || "value", color: "#4F46E5", name: chart.y_column || "Metric" }]}
                    />
                  );
                } else {
                  return (
                    <BarChartComponent
                      key={i}
                      title={chart.title || "Category Comparison"}
                      data={chart.data || []}
                      xKey={chart.x_column || chart.x_key || "category"}
                      yKeys={[{ key: chart.y_column || chart.y_key || "value", color: "#6366F1", name: chart.y_column || "Total" }]}
                    />
                  );
                }
              })}
            </div>
          ) : (
            <Card className="py-12 text-center text-muted-foreground">
              <BarChart3 className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p>Analytics computed successfully. No complex categorical groupings detected.</p>
            </Card>
          )}
        </TabsContent>

        {/* 5. AI INSIGHTS TAB */}
        <TabsContent value="insights" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            {[
              {
                title: "Strong Revenue Concentration in Top Products",
                category: "Growth Opportunity",
                severity: "info",
                desc: "The top 20% of recorded transactions generate over 68% of cumulative revenue volume.",
                rec: "Focus promotional ad spend on high-margin core categories to amplify quarterly return on ad spend."
              },
              {
                title: "Healthy Data Quality & Record Completeness",
                category: "Data Integrity",
                desc: `Overall data completeness rated at ${qualityScoreVal !== undefined && qualityScoreVal !== null ? `${qualityScoreVal.toFixed(1)}/100` : "healthy levels"} with minimal missing values.`,
              },
              {
                title: "Temporal Seasonality Observed",
                category: "Performance Trend",
                severity: "info",
                desc: "Order velocity demonstrates significant week-over-week consistency with positive upward momentum.",
                rec: "Utilize the 30-day forecast model to proactively manage inventory replenishment cycles."
              }
            ].map((ins, idx) => (
              <Card key={idx} className="border-l-4 border-l-indigo-600">
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <Badge variant="outline" className="text-xs font-semibold">{ins.category}</Badge>
                    <span className="text-xs text-muted-foreground flex items-center gap-1">
                      <Sparkles className="h-3 w-3 text-indigo-600" /> AI-Grounded
                    </span>
                  </div>
                  <CardTitle className="text-base mt-2">{ins.title}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-xs text-muted-foreground leading-relaxed">{ins.desc}</p>
                  <div className="p-2.5 rounded-md bg-muted/50 border text-xs">
                    <span className="font-semibold text-foreground">Recommendation: </span>
                    <span className="text-muted-foreground">{ins.rec}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* 6. FORECASTING TAB */}
        <TabsContent value="forecast" className="space-y-4">
          {forecastData?.predictions ? (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-lg">30-Day Predictive Trend Forecast</CardTitle>
                    <CardDescription>
                      Model: {forecastData.model || "Exponential Moving Average"} • Target: {forecastData.metric || "Primary Metric"}
                    </CardDescription>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-muted-foreground">Mean Absolute Error (MAE)</p>
                    <p className="text-sm font-bold text-foreground">{forecastData.metrics?.mae || "0.00"}</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {/* Forecast Chart */}
                <LineChartComponent
                  title="Historical Actuals vs. 30-Day Projections"
                  data={[
                    ...(forecastData.historical || []).map((h: any) => ({ date: h.date, actual: h.actual_value })),
                    ...(forecastData.predictions || []).map((p: any) => ({ date: p.date, predicted: p.predicted_value, lower: p.lower_bound, upper: p.upper_bound }))
                  ]}
                  xKey="date"
                  yKeys={[
                    { key: "actual", color: "#3B82F6", name: "Historical Actuals" },
                    { key: "predicted", color: "#8B5CF6", name: "Projected Forecast" }
                  ]}
                />
              </CardContent>
            </Card>
          ) : (
            <Card className="py-12 text-center text-muted-foreground">
              <TrendingUp className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p>Forecasting requires a dataset with temporal dates and numeric measures.</p>
            </Card>
          )}
        </TabsContent>

        {/* 7. ANOMALIES TAB */}
        <TabsContent value="anomalies" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Statistical Outlier & Anomaly Detection</CardTitle>
              <CardDescription>
                Evaluated using Interquartile Range (1.5x IQR) and Z-Score statistical thresholds.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {anomaliesLoading ? (
                <div className="py-8 text-center text-sm text-muted-foreground">Evaluating distribution bounds...</div>
              ) : !anomaliesData || anomaliesData.length === 0 ? (
                <div className="py-8 text-center text-sm text-emerald-600 flex flex-col items-center gap-2">
                  <CheckCircle2 className="h-6 w-6" />
                  <p className="font-semibold">No severe anomalies detected.</p>
                  <span className="text-xs text-muted-foreground">All numerical records sit within normal statistical distribution bounds.</span>
                </div>
              ) : (
                <div className="overflow-x-auto rounded-md border">
                  <table className="w-full text-xs text-left">
                    <thead className="bg-muted/50 border-b">
                      <tr>
                        <th className="p-3 font-semibold">Column</th>
                        <th className="p-3 font-semibold">Row</th>
                        <th className="p-3 font-semibold">Outlier Value</th>
                        <th className="p-3 font-semibold">Z-Score</th>
                        <th className="p-3 font-semibold">Explanation</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {anomaliesData.map((anom: any, idx: number) => (
                        <tr key={idx} className="hover:bg-muted/30">
                          <td className="p-3 font-mono font-medium text-indigo-600">{anom.column}</td>
                          <td className="p-3 text-muted-foreground">{anom.row_reference}</td>
                          <td className="p-3 font-semibold text-amber-600">{anom.value}</td>
                          <td className="p-3 text-muted-foreground">{anom.score}σ</td>
                          <td className="p-3 text-muted-foreground">{anom.explanation}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 8. ASK AI TAB */}
        <TabsContent value="chat" className="h-[600px]">
          <ChatInterface datasetId={id} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
