/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import { useState, useEffect, useCallback, useRef } from 'react';

type AsyncState<T> = {
  data: T | null;
  loading: boolean;
  error: string | null;
  isFromApi: boolean;
};

/**
 * Hook to fetch data from the API with automatic fallback to mock data.
 *
 * @param fetcher - async function that calls the API
 * @param fallback - mock data to use if the API call fails
 * @param deps - dependency array (re-fetches when these change)
 */
export function useApiData<T>(
  fetcher: () => Promise<T>,
  fallback: T,
  deps: unknown[] = []
): AsyncState<T> & { refetch: () => void } {
  const [state, setState] = useState<AsyncState<T>>({
    data: fallback,
    loading: true,
    error: null,
    isFromApi: false,
  });

  const fetcherRef = useRef(fetcher);
  fetcherRef.current = fetcher;

  const doFetch = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const data = await fetcherRef.current();
      setState({ data, loading: false, error: null, isFromApi: true });
    } catch (err) {
      console.warn('[SalesBrain] API unavailable, using mock data:', (err as Error).message);
      setState({
        data: fallback,
        loading: false,
        error: (err as Error).message || 'Backend unavailable',
        isFromApi: false,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    doFetch();
  }, [doFetch]);

  return { ...state, refetch: doFetch };
}
