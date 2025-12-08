const BASE_URL = "http://127.0.0.1:8001/api";

export type AskQueryRequest = {
  query: string;
  top_k?: number;
};

export type AskQueryResponse = {
  answer?: string;
  chunks?: {
    id: string;
    content: string;
    score: number;
    source: string;
  }[];
  sources?: {
    filename: string;
    chunk_index: number;
    lines?: string;
  }[];
  detail?: string; // Error response field
  query?: string;
  total_tokens?: number;
};

// Upload document
export async function uploadDocument(formData: FormData): Promise<{ id: string }> {
  const response = await fetch(`${BASE_URL}/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Upload failed");
  }

  return response.json();
}

// Ask query
export async function askQuery(payload: AskQueryRequest): Promise<AskQueryResponse> {
  const response = await fetch(`${BASE_URL}/queries/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: payload.query,
      top_k: payload.top_k ?? 5,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Query failed");
  }


    console.log("REQUEST URL:", `${BASE_URL}/queries/ask`);
    console.log("PAYLOAD:", payload);

  return data;
}
