"""
LLM応答検索ユースケース

from __future__ import annotations
"""

from uuid import UUID

from app.domain.models.llm_response import LLMResponse
from app.domain.repositories.llm_response_repository import LLMResponseRepository


class SearchResponsesUseCase:
    """
    LLM応答検索ユースケース

    検索条件に基づいてLLM応答を検索します。
    """

    def __init__(self, llm_response_repository: LLMResponseRepository):
        """
        Args:
            llm_response_repository: LLM応答リポジトリ
        """
        self.llm_response_repository = llm_response_repository

    def execute(
        self,
        query: str | None = None,
        category_id: UUID | None = None,
        tags: list[str] | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[LLMResponse]:
        """
        LLM応答を検索します。

        Args:
            query: 検索クエリ（タイトル・プロンプト・内容で検索）
            category_id: カテゴリIDでフィルタ
            tags: タグでフィルタ
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            検索条件に合致するLLM応答エンティティのリスト
        """
        return self.llm_response_repository.search(
            query=query,
            category_id=category_id,
            tags=tags,
            skip=skip,
            limit=limit,
        )
