"""
Synthesis service for generating answers using Gemini
"""
import google.generativeai as genai
from typing import List, Tuple
from app.models.chunk import Chunk
from app.config import get_settings


class SynthesisService:
    """Service for generating answers from retrieved chunks"""
    
    settings = get_settings()
    
    def __init__(self):
        """Initialize Gemini API"""
        if not self.settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not set in environment")
        
        genai.configure(api_key=self.settings.GOOGLE_API_KEY)
    
    @staticmethod
    def generate_answer(
        query: str,
        chunks: List[Tuple[Chunk, float]],
        language: str = "Russian"
    ) -> str:
        """
        Generate answer based on query and retrieved chunks
        
        Args:
            query: User query
            chunks: List of (Chunk, score) tuples
            language: Language for response
            
        Returns:
            Generated answer
        """
        if not chunks:
            return f"I don't have enough information to answer your question about '{query}'."
        
        # Prepare context
        context_parts = []
        for idx, (chunk, score) in enumerate(chunks, 1):
            context_parts.append(
                f"[Source {idx} (relevance: {score:.2%})]\n{chunk.content}"
            )
        
        context = "\n\n".join(context_parts)
        
        # Create prompt
        prompt = f"""You are a helpful assistant answering questions based on provided documents.
        
Answer the following question in {language} based ONLY on the provided context.
If the context doesn't contain the answer, say so explicitly.
Always cite which source(s) you're using.

Question: {query}

Context from documents:
{context}

Please provide a comprehensive answer citing the relevant sources."""
        
        try:
            service = SynthesisService()

            model_name = service.settings.GENERATION_MODEL

            # Try common genai generation entrypoints with fallbacks to support
            # different genai client versions and model availability.
            # Preferred: genai.generate_text (newer clients), fallback to
            # genai.generate or genai.GenerativeModel usage.
            try:
                # genai.generate_text -> returns object with .text or dict
                resp = genai.generate_text(model=model_name, prompt=prompt, temperature=0)
                # try common attributes
                if hasattr(resp, 'text') and resp.text:
                    return resp.text
                if isinstance(resp, dict):
                    # try to find content in known shapes
                    if 'candidates' in resp and resp['candidates']:
                        return resp['candidates'][0].get('content') or resp['candidates'][0].get('output')
                    if 'output' in resp:
                        return resp['output']

            except Exception:
                # Try alternative API shape
                pass

            try:
                # Older or alternate API
                resp = genai.generate(model=model_name, prompt=prompt, temperature=0)
                if hasattr(resp, 'text') and resp.text:
                    return resp.text
                if isinstance(resp, dict) and 'candidates' in resp and resp['candidates']:
                    return resp['candidates'][0].get('content') or resp['candidates'][0].get('output')
            except Exception:
                pass

            try:
                # Last resort: GenerativeModel interface used previously in codebase
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                # response may have .text or .candidates
                if hasattr(response, 'text') and response.text:
                    return response.text
                if isinstance(response, dict) and 'candidates' in response and response['candidates']:
                    return response['candidates'][0].get('content') or response['candidates'][0].get('output')
            except Exception as e:
                raise ValueError(f"Failed to generate answer: {str(e)}")

            # If none of the above returned text, raise explicit error
            raise ValueError("Failed to generate answer: generation returned no text from model")
        except Exception as e:
            raise ValueError(f"Failed to generate answer: {str(e)}")
    
    @staticmethod
    def format_sources(chunks: List[Tuple[Chunk, float]]) -> List[dict]:
        """
        Format chunks into source references
        
        Args:
            chunks: List of (Chunk, score) tuples
            
        Returns:
            List of source information dicts
        """
        sources = []
        for chunk, score in chunks:
            sources.append({
                "document": chunk.chunk_metadata.get("document_filename") if chunk.chunk_metadata else "Unknown",
                "category": chunk.chunk_metadata.get("category") if chunk.chunk_metadata else None,
                "chunk_index": chunk.chunk_index,
                "relevance_score": round(score, 4),
                "content_preview": chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
            })
        
        return sources
