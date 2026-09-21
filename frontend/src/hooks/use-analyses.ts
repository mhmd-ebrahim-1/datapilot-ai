import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { Analysis, Insight } from "@/types"

export function useAnalyses(datasetId?: string) {
  return useQuery({
    queryKey: ["analyses", datasetId],
    queryFn: () => {
      const url = datasetId ? `/api/v1/analyses?datasetId=${datasetId}` : "/api/v1/analyses"
      return api.get<Analysis[]>(url)
    }
  })
}

export function useAnalysis(id: string) {
  return useQuery({
    queryKey: ["analyses", id],
    queryFn: () => api.get<Analysis>(`/api/v1/analyses/${id}`),
    enabled: !!id
  })
}

export function useCreateAnalysis() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: { datasetId: string, name: string }) => api.post("/api/v1/analyses", data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["analyses"] })
  })
}

export function useInsights(datasetId: string) {
  return useQuery({
    queryKey: ["insights", datasetId],
    queryFn: () => api.get<Insight[]>(`/api/v1/datasets/${datasetId}/insights`),
    enabled: !!datasetId
  })
}
