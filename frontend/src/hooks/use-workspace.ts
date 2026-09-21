import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { Workspace } from "@/types"
import { create } from "zustand"

interface WorkspaceState {
  currentWorkspaceId: string | null
  setCurrentWorkspaceId: (id: string) => void
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  currentWorkspaceId: typeof window !== "undefined" ? localStorage.getItem("currentWorkspaceId") : null,
  setCurrentWorkspaceId: (id) => {
    localStorage.setItem("currentWorkspaceId", id)
    set({ currentWorkspaceId: id })
  }
}))

export function useWorkspaces() {
  return useQuery({
    queryKey: ["workspaces"],
    queryFn: () => api.get<Workspace[]>("/api/v1/workspaces")
  })
}

export function useCurrentWorkspace() {
  const { currentWorkspaceId, setCurrentWorkspaceId } = useWorkspaceStore()
  const { data: workspaces, isLoading } = useWorkspaces()
  
  if (workspaces && workspaces.length > 0 && !currentWorkspaceId) {
    setCurrentWorkspaceId(workspaces[0].id)
  }
  
  const currentWorkspace = workspaces?.find(w => w.id === currentWorkspaceId) || workspaces?.[0]
  
  return { currentWorkspace, currentWorkspaceId, setCurrentWorkspaceId, workspaces, isLoading }
}
