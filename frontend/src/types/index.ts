export interface User {
  id: string;
  name: string;
  email: string;
  role?: string;
  avatar_url?: string;
  avatarUrl?: string;
  is_active?: boolean;
  created_at?: string;
}

export interface Workspace {
  id: string;
  name: string;
  owner_id?: string;
  logo_url?: string;
  logoUrl?: string;
  brand_color?: string;
  role?: string;
  created_at?: string;
}

export interface WorkspaceMember {
  id: string;
  userId?: string;
  user_id?: string;
  workspaceId?: string;
  workspace_id?: string;
  role: "owner" | "admin" | "analyst" | "member" | "viewer" | string;
  name?: string;
  email?: string;
  user?: User;
  created_at?: string;
}

export interface Dataset {
  id: string;
  name: string;
  original_filename?: string;
  file_type?: string;
  file_size?: number;
  workspaceId?: string;
  workspace_id?: string;
  rowCount?: number;
  row_count?: number;
  colCount?: number;
  column_count?: number;
  dataset_type?: string;
  quality_score?: number;
  qualityScore?: number;
  status: "uploaded" | "processing" | "ready" | "failed" | "deleted" | string;
  profile?: any;
  profile_json?: any;
  cleaning_summary?: any;
  cleaning_summary_json?: any;
  createdAt?: string;
  created_at?: string;
}

export interface DatasetProfile {
  id?: string;
  datasetId?: string;
  dataset_id?: string;
  qualityScore?: number;
  quality_score?: number;
  dataset_type?: string;
  cleaning_summary?: any;
  profile?: any;
}

export interface DatasetPreview {
  columns: Array<{ key: string; label: string; type: string } | string>;
  rows: Record<string, any>[];
  total_rows?: number;
  page?: number;
  page_size?: number;
  total_pages?: number;
}

export interface Analysis {
  id: string;
  datasetId?: string;
  dataset_id?: string;
  workspace_id?: string;
  status: string;
  kpis?: any[];
  kpis_json?: any;
  charts?: any[];
  charts_json?: any;
  summary?: any;
  summary_json?: any;
  metadata?: any;
  created_at?: string;
}

export interface KPI {
  name: string;
  value: number | string;
  formatted_value?: string;
  description?: string;
  icon?: string;
  color?: string;
}

export interface ChartConfig {
  type: string;
  title: string;
  x_column?: string;
  y_column?: string;
  data: any[];
}

export interface Insight {
  id: string;
  title: string;
  category: string;
  severity: "info" | "warning" | "critical" | string;
  description: string;
  recommendation?: string;
  supporting_metrics?: any;
  created_at?: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  context?: any;
  timestamp?: string;
}

export interface ChatSession {
  id: string;
  datasetId?: string;
  dataset_id?: string;
  created_at?: string;
}

export interface Forecast {
  id?: string;
  model?: string;
  metric?: string;
  predictions: Array<{ date: string; predicted_value: number; lower_bound: number; upper_bound: number }>;
  confidence_intervals?: any[];
  historical?: any[];
  metrics?: { mae: number; rmse: number; mape: number };
}

export interface Anomaly {
  id: string;
  column: string;
  row_reference: string;
  value: string;
  score: number;
  explanation: string;
}

export interface Report {
  id: string;
  title: string;
  dataset_id: string;
  dataset_name?: string;
  format: string;
  created_at: string;
}

export interface Subscription {
  plan: string;
  status: string;
  current_period_start?: string;
  current_period_end?: string;
}

export interface Usage {
  plan: string;
  analyses: { used: number; limit: number };
  ai_requests: { used: number; limit: number };
  uploads: { used: number; limit: number };
  storage_mb: { used: number; limit: number };
}

export interface Plan {
  name: string;
  limits: Record<string, any>;
}

export interface ApiError {
  message: string;
  code?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
}
