import { create } from 'zustand';

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
