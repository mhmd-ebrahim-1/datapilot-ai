import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Dataset, DatasetProfile, DatasetPreview } from "@/types";

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
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (file: File) => api.upload<Dataset>("/api/v1/datasets/upload", file),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["datasets"] })
  });
}

export function useDeleteDataset() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/datasets/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["datasets"] })
  });
}
