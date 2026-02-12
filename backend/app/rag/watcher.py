"""
Document Watcher Agent for FactFlow.

Monitors document content for changes using SHA256 hashing
and timestamp-based freshness detection. Does not perform
any vector DB operations or trigger refresh — it only detects
and reports staleness.
"""
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any


class DocumentWatcherAgent:
    """
    Background-style agent that checks documents for staleness.

    Detection methods:
    1. Hash-based: SHA256 of content vs stored hash in metadata.
    2. Timestamp-based: published_at older than 180 days → outdated.
    """

    FRESHNESS_THRESHOLD_DAYS = 180

    def check_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check a list of documents for staleness.

        Args:
            documents: List of dicts, each with:
                - "content": str — the document text
                - "metadata": dict — must include:
                    - "content_hash": str (previously stored SHA256)
                    - "published_at": str (ISO 8601 date, e.g. "2025-06-15")

        Returns:
            {
                "stale": bool,
                "changed_documents": int,
                "reason": "hash_mismatch" | "outdated" | "no_change"
            }
        """
        if not documents:
            return {
                "stale": False,
                "changed_documents": 0,
                "reason": "no_change"
            }

        hash_mismatches = 0
        outdated_count = 0

        for doc in documents:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})

            # 1. Hash-based change detection
            current_hash = self._compute_hash(content)
            stored_hash = metadata.get("content_hash", "")
            if stored_hash and current_hash != stored_hash:
                hash_mismatches += 1

            # 2. Timestamp freshness detection
            published_at = metadata.get("published_at", "")
            if published_at and self._is_outdated(published_at):
                outdated_count += 1

        # 3. Final decision
        if hash_mismatches > 0:
            return {
                "stale": True,
                "changed_documents": hash_mismatches,
                "reason": "hash_mismatch"
            }
        elif outdated_count > 0:
            return {
                "stale": True,
                "changed_documents": outdated_count,
                "reason": "outdated"
            }
        else:
            return {
                "stale": False,
                "changed_documents": 0,
                "reason": "no_change"
            }

    @staticmethod
    def _compute_hash(content: str) -> str:
        """Compute SHA256 hash of document content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _is_outdated(self, published_at: str) -> bool:
        """
        Check if a document is older than the freshness threshold.

        Args:
            published_at: ISO 8601 date string (e.g. "2025-06-15")

        Returns:
            True if the document is older than FRESHNESS_THRESHOLD_DAYS.
        """
        try:
            pub_date = datetime.fromisoformat(published_at)
            if pub_date.tzinfo is None:
                pub_date = pub_date.replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - pub_date).days
            return age_days > self.FRESHNESS_THRESHOLD_DAYS
        except (ValueError, TypeError):
            return False
