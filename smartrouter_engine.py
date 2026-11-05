"""
Local SmartRouter engine for SmartRouter Analytics.

Uses TF-IDF + cosine similarity for lightweight semantic-style caching.
This is a local similarity baseline, not a neural embedding model or an LLM.
"""

from __future__ import annotations

import re
import time
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SmartRouterEngine:
    """Route questions locally and reuse answers for sufficiently similar queries."""

    def __init__(self, similarity_threshold: float = 0.72):
        self.similarity_threshold = float(similarity_threshold)
        self.cache: list[dict[str, Any]] = []

    @staticmethod
    def _clean(text: str) -> str:
        text = str(text or "").strip().lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    COMPLEX_KEYWORDS = {
        "compare", "analyze", "analysis", "evaluate", "architecture",
        "strategy", "comprehensive", "relationship", "multiple",
        "optimize", "recommend", "forecast", "design", "detailed",
        "tradeoff", "trade-offs", "implementation", "prioritize",
        "investigate", "experiment", "predict", "interpret",
    }

    MEDIUM_KEYWORDS = {
        "explain", "describe", "calculate", "summarize", "why",
        "how", "difference", "identify", "classify", "debug",
        "convert", "outline", "example",
    }

    @classmethod
    def classify_request(cls, query: str) -> dict[str, Any]:
        """Score a request with transparent rules; this is not a trained ML model."""
        cleaned = cls._clean(query)
        words = cleaned.split()
        word_count = len(words)
        complex_matches = sorted(set(words) & cls.COMPLEX_KEYWORDS)
        medium_matches = sorted(set(words) & cls.MEDIUM_KEYWORDS)
        score = 0
        reasons: list[str] = []

        if word_count >= 25:
            score += 3
            reasons.append("long request (25+ words)")
        elif word_count >= 13:
            score += 2
            reasons.append("multi-step length (13+ words)")
        elif word_count >= 7:
            score += 1
            reasons.append("moderate request length")

        if complex_matches:
            score += min(4, len(complex_matches) * 2)
            reasons.append("complex task terms: " + ", ".join(complex_matches))
        if medium_matches:
            score += 2 if medium_matches else 0
            reasons.append("instruction terms: " + ", ".join(medium_matches))
        if any(term in cleaned for term in [" and ", " versus ", " vs "]):
            score += 1
            reasons.append("multiple aspects or comparison")

        if score >= 5:
            complexity, route, profile = "Complex", "Local deep-analysis route", "High-capability profile"
            explanation = "The request has several signals of multi-step reasoning."
        elif score >= 2:
            complexity, route, profile = "Medium", "Local balanced route", "Balanced profile"
            explanation = "The request needs explanation or moderate processing."
        else:
            complexity, route, profile = "Simple", "Local fast route", "Lightweight profile"
            explanation = "The request appears short and straightforward."

        if not reasons:
            reasons.append("short request with no strong complexity keywords")
        return {
            "complexity": complexity, "complexity_score": score,
            "route": route, "route_profile": profile,
            "routing_reason": explanation + " Signals: " + "; ".join(reasons) + ".",
            "classification_signals": reasons,
        }

    @classmethod
    def classify_complexity(cls, query: str) -> str:
        """Compatibility helper returning only the complexity label."""
        return cls.classify_request(query)["complexity"]

    @staticmethod
    def _local_answer(query: str, complexity: str) -> str:
        """
        Small deterministic local response generator.
        It demonstrates routing/caching without claiming to be an LLM.
        """
        cleaned = query.strip().rstrip("?!.")
        lower = cleaned.lower()

        if any(term in lower for term in ["hello", "hi", "hey"]):
            return (
                "Hello! I'm the local SmartRouter prototype. "
                "I can demonstrate query routing and caching without an API key."
            )

        if "machine learning" in lower or re.search(r"\bml\b", lower):
            return (
                "Machine learning is a branch of artificial intelligence in which "
                "computer systems learn patterns from data and use those patterns "
                "to make predictions or decisions. Common approaches include "
                "supervised, unsupervised, and reinforcement learning."
            )

        if "semantic cach" in lower or "cache" in lower:
            return (
                "A semantic cache stores a response with its original query. "
                "When a new query arrives, the system compares it with cached "
                "queries and reuses a response when similarity exceeds a chosen "
                "threshold. This can reduce repeated processing and response time."
            )

        if any(term in lower for term in ["python", "error", "bug", "code"]):
            return (
                f"I received your programming-related request: “{cleaned}”. "
                "For a precise solution, include the relevant code, full error "
                "message, and expected output. This prototype uses a local "
                "rule-based responder rather than executing code."
            )

        if any(term in lower for term in ["data", "dataset", "csv", "sales"]):
            return (
                f"For the data-related request “{cleaned}”, a useful analysis "
                "workflow is to inspect column types and missing values, validate "
                "the data, calculate descriptive statistics, and then examine "
                "patterns with suitable visualizations. Uploading a dataset and "
                "connecting a real analysis tool would be needed for actual results."
            )

        if complexity == "Complex":
            return (
                f"Local analysis outline for: “{cleaned}”\n\n"
                "1. Define the objective and expected outcome.\n"
                "2. Identify the inputs, constraints, and assumptions.\n"
                "3. Break the task into smaller steps.\n"
                "4. Evaluate the results against the objective.\n\n"
                "This is a local demonstration response, not an LLM-generated "
                "research answer."
            )

        return (
            f"Your request was received: “{cleaned}”. "
            "This local prototype demonstrates request routing and semantic-style "
            "cache behavior. Connect a language model later if you want "
            "open-ended AI-generated answers."
        )

    def _find_cache_match(self, query: str) -> tuple[dict[str, Any] | None, float]:
        if not self.cache:
            return None, 0.0

        cached_queries = [item["query"] for item in self.cache]
        documents = cached_queries + [query]

        try:
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
            matrix = vectorizer.fit_transform(documents)
            scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
            best_index = int(np.argmax(scores))
            best_score = float(scores[best_index])
        except ValueError:
            return None, 0.0

        if best_score >= self.similarity_threshold:
            return self.cache[best_index], best_score
        return None, best_score

    def process(self, query: str) -> dict[str, Any]:
        query = str(query or "").strip()
        if not query:
            raise ValueError("Please enter a question before submitting.")

        started = time.perf_counter()
        routing = self.classify_request(query)
        complexity = routing["complexity"]
        match, similarity = self._find_cache_match(query)

        if match is not None:
            answer = match["answer"]
            route = "Semantic cache"
            route_profile = "Cached response"
            routing_reason = (
                f"Reused a stored response because similarity ({similarity:.1%}) "
                f"met the {self.similarity_threshold:.1%} threshold."
            )
            cache_hit = True
            model = "Local cache"
        else:
            answer = self._local_answer(query, complexity)
            route = routing["route"]
            route_profile = routing["route_profile"]
            routing_reason = routing["routing_reason"]
            cache_hit = False
            model = "Local rule-based responder"
            self.cache.append({
                "query": query, "answer": answer, "complexity": complexity,
                "route": route, "route_profile": route_profile,
            })

        latency_ms = (time.perf_counter() - started) * 1000
        return {
            "query": query,
            "answer": answer,
            "cache_hit": cache_hit,
            "similarity": similarity,
            "complexity": complexity,
            "complexity_score": routing["complexity_score"],
            "route": route,
            "route_profile": route_profile,
            "routing_reason": routing_reason,
            "classification_signals": routing["classification_signals"],
            "model": model,
            "latency_ms": latency_ms,
            "cache_size": len(self.cache),
        }

    def clear_cache(self) -> None:
        self.cache.clear()
