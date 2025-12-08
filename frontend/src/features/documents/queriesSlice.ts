import { createSlice } from "@reduxjs/toolkit";
import { ragApi } from "../documents/documentsApi";
import type { AskQueryResponse } from "../documents/documentsApi";


type QueryState = {
  response: AskQueryResponse | null;
};

const initialState: QueryState = {
  response: null,
};

const queriesSlice = createSlice({
  name: "queries",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addMatcher(
      ragApi.endpoints.askQuery.matchFulfilled,
      (state, { payload }) => {
        state.response = payload;
      }
    );
  },
});

export default queriesSlice.reducer;
