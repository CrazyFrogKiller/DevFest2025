export interface Document {
  id: string;
  filename: string;
  title?: string;
  content_type: string;
  file_size: number;
  uploaded_at: string;
  metadata?: Record<string, any>;
}

export interface Chunk {
  id: string;
  document_id: string;
  content: string;
  chunk_index: number;
  similarity: number;
  document: {
    id: string;
    filename: string;
    title?: string;
  };
}

export interface QueryRequest {
  query: string;
  top_k?: number;
  min_similarity?: number;
}

export interface QueryResponse {
  query?: string;
  answer?: string;
  chunks?: Chunk[];
  has_sufficient_data?: boolean;
  processing_time?: number;
  sources?: string[];
  total_tokens?: number;
  detail?: string; // Error response field
}
