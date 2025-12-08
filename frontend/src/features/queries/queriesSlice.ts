import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { QueryResponse } from '../../types';

interface QueriesState {
  currentQuery: string;
  currentResponse: QueryResponse | null;
  isLoading: boolean;
  history: QueryResponse[];
  settings: {
    topK: number;
    minSimilarity: number;
  };
}

const initialState: QueriesState = {
  currentQuery: '',
  currentResponse: null,
  isLoading: false,
  history: [],
  settings: {
    topK: 5,
    minSimilarity: 0.7,
  },
};

const queriesSlice = createSlice({
  name: 'queries',
  initialState,
  reducers: {
    setCurrentQuery: (state, action: PayloadAction<string>) => {
      state.currentQuery = action.payload;
    },
    setCurrentResponse: (state, action: PayloadAction<QueryResponse | null>) => {
      state.currentResponse = action.payload;
      if (action.payload) {
        state.history.unshift(action.payload);
        // Keep only last 10 queries
        state.history = state.history.slice(0, 10);
      }
    },
    setIsLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    clearCurrentResponse: (state) => {
      state.currentResponse = null;
      state.currentQuery = '';
    },
    updateSettings: (state, action: PayloadAction<Partial<QueriesState['settings']>>) => {
      state.settings = { ...state.settings, ...action.payload };
    },
    clearHistory: (state) => {
      state.history = [];
    },
  },
});

export const {
  setCurrentQuery,
  setCurrentResponse,
  setIsLoading,
  clearCurrentResponse,
  updateSettings,
  clearHistory,
} = queriesSlice.actions;

export default queriesSlice.reducer;