import { configureStore } from '@reduxjs/toolkit';
import queriesReducer from '../features/queries/queriesSlice';
import documentsReducer from '../features/documents/documentsSlice';

export const store = configureStore({
  reducer: {
    queries: queriesReducer,
    documents: documentsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
