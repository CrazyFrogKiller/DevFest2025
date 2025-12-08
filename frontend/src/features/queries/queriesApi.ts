import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const queriesApi = createApi({
  reducerPath: "queriesApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://127.0.0.1:8001",
  }),
  endpoints: (builder) => ({
    submitQuery: builder.mutation({
      query: (payload: { query: string; top_k?: number }) => ({
        url: "/api/queries/ask",
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Ensure backend receives JSON and provide a default top_k = 5
        body: JSON.stringify({ query: payload.query, top_k: payload.top_k ?? 5 }),
      }),
    }),
  }),
});

export const { useSubmitQueryMutation } = queriesApi;
