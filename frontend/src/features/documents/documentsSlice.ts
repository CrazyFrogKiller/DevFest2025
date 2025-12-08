import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { Document } from '../../types';

type DocumentsState = {
  items: Document[];
};

const initialState: DocumentsState = { items: [] };

const documentsSlice = createSlice({
  name: 'documents',
  initialState,
  reducers: {
    setDocuments(state, action: PayloadAction<Document[]>) {
      state.items = action.payload;
    },
    addDocument(state, action: PayloadAction<Document>) {
      state.items.push(action.payload);
    },
    removeDocument(state, action: PayloadAction<string>) {
      state.items = state.items.filter((d) => d.id !== action.payload);
    },
    clearDocuments(state) {
      state.items = [];
    },
  },
});

export const { setDocuments, addDocument, removeDocument, clearDocuments } = documentsSlice.actions;
export default documentsSlice.reducer;