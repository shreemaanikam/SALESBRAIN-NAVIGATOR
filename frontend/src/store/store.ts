import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface FilterState {
  searchQuery: string;
  category: string;
  region: string;
  segment: string;
  dateRange: string;
  setSearchQuery: (query: string) => void;
  setCategory: (category: string) => void;
  setRegion: (region: string) => void;
  setSegment: (segment: string) => void;
  setDateRange: (range: string) => void;
  clearFilters: () => void;
}

export const useFilterStore = create<FilterState>((set) => ({
  searchQuery: '',
  category: 'All',
  region: 'All',
  segment: 'All',
  dateRange: 'Last 12 Months',
  setSearchQuery: (query) => set({ searchQuery: query }),
  setCategory: (category) => set({ category }),
  setRegion: (region) => set({ region }),
  setSegment: (segment) => set({ segment }),
  setDateRange: (range) => set({ dateRange: range }),
  clearFilters: () => set({ 
    searchQuery: '', 
    category: 'All', 
    region: 'All', 
    segment: 'All', 
    dateRange: 'Last 12 Months' 
  }),
}));

export interface UIState {
  isMobileMenuOpen: boolean;
  toggleMobileMenu: () => void;
  setMobileMenuOpen: (isOpen: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  isMobileMenuOpen: false,
  toggleMobileMenu: () => set((state) => ({ isMobileMenuOpen: !state.isMobileMenuOpen })),
  setMobileMenuOpen: (isOpen) => set({ isMobileMenuOpen: isOpen }),
}));

// ── Workspace (My Data) State ──────────────────────────────────────────────

export interface WorkspaceInfo {
  datasetId: string;
  filename: string;
  rowCount: number;
  columnCount: number;
  mapping: Record<string, string>;
  status: string;
  createdAt: string;
}

export interface WorkspaceState {
  activeWorkspace: WorkspaceInfo | null;
  workspaces: WorkspaceInfo[];
  setActiveWorkspace: (ws: WorkspaceInfo | null) => void;
  addWorkspace: (ws: WorkspaceInfo) => void;
  removeWorkspace: (datasetId: string) => void;
  clearWorkspaces: () => void;
}

export const useWorkspaceStore = create<WorkspaceState>()(
  persist(
    (set) => ({
      activeWorkspace: null,
      workspaces: [],
      setActiveWorkspace: (ws) => set({ activeWorkspace: ws }),
      addWorkspace: (ws) =>
        set((state) => ({
          workspaces: [...state.workspaces.filter((w) => w.datasetId !== ws.datasetId), ws],
          activeWorkspace: ws,
        })),
      removeWorkspace: (datasetId) =>
        set((state) => ({
          workspaces: state.workspaces.filter((w) => w.datasetId !== datasetId),
          activeWorkspace:
            state.activeWorkspace?.datasetId === datasetId ? null : state.activeWorkspace,
        })),
      clearWorkspaces: () => set({ workspaces: [], activeWorkspace: null }),
    }),
    {
      name: 'salesbrain-workspaces',
      partialize: (s) => ({ workspaces: s.workspaces, activeWorkspace: s.activeWorkspace }),
    }
  )
);
