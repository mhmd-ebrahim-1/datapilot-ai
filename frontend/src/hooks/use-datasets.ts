import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Dataset, DatasetProfile, DatasetPreview } from "@/types";
import { Dataset, DatasetProfile, DatasetPreview, PresignedUploadResponse } from "@/types";

export function useDatasets() {
  return useQuery({
    queryKey: ["datasets"],
    queryFn: () => api.get<Dataset[]>("/api/v1/datasets")
  });
}

export function useDataset(id: string) {
  return useQuery({
    queryKey: ["datasets", id],
    queryFn: () => api.get<Dataset>(`/api/v1/datasets/${id}`),
    enabled: !!id
  });
}

export function useDatasetPreview(id: string, page = 1) {
  return useQuery({
    queryKey: ["datasets", id, "preview", page],
    queryFn: () => api.get<DatasetPreview>(`/api/v1/datasets/${id}/preview?page=${page}`),
    enabled: !!id
  });
}

export function useDatasetProfile(id: string) {
  return useQuery({
    queryKey: ["datasets", id, "profile"],
    queryFn: () => api.get<DatasetProfile>(`/api/v1/datasets/${id}/profile`),
    enabled: !!id
  });
}

export function useUploadDataset() {
export interface DirectUploadParams {
  file: File;
  workspaceId?: string;
  onProgress?: (percent: number, statusText: string) => void;
}

export function useDirectUploadDataset() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (file: File) => api.upload<Dataset>("/api/v1/datasets/upload", file),
    mutationFn: async ({ file, workspaceId, onProgress }: DirectUploadParams): Promise<Dataset> => {
      // Step 1: Request presigned upload authorization
      if (onProgress) onProgress(5, "Requesting secure storage upload authorization...");
      const presigned = await api.post<PresignedUploadResponse>("/api/v1/datasets/presigned-upload", {
        filename: file.name,
        file_size: file.size,
        content_type: file.type || "application/octet-stream",
        workspace_id: workspaceId || undefined
      });

      // Step 2: Stream file directly to Supabase S3 Storage (bypasses Vercel 4.5MB limit)
      if (onProgress) onProgress(15, `Uploading directly to Cloud Storage (${(file.size / (1024 * 1024)).toFixed(1)} MB)...`);
      await api.uploadDirect(
        presigned.upload_url,
        file,
        presigned.headers?.["Content-Type"] || file.type,
        (uploadPercent) => {
          // Map upload progress from 15% to 85%
          const mapped = Math.round(15 + (uploadPercent * 0.70));
          if (onProgress) onProgress(mapped, `Uploading directly to Cloud Storage (${uploadPercent}%)...`);
        }
      );

      // Step 3: Trigger server-side deterministic analytics pipeline
      if (onProgress) onProgress(88, "Executing deterministic data profiling and analytics...");
      const processed = await api.post<Dataset>(`/api/v1/datasets/${presigned.dataset_id}/process`, {});
      
      if (onProgress) onProgress(100, "Dataset analytics ready!");
      return processed;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["datasets"] })
  });
}

export function useUploadDataset() {
  return useDirectUploadDataset();
}

export function useDeleteDataset() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/datasets/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["datasets"] })
  });
}
