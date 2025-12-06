"""
LLM応答一覧取得ユースケース

from __future__ import annotations
"""

from app.domain.models.llm_response import LLMResponse
from app.domain.repositories.llm_response_repository import LLMResponseRepository


class ListResponsesUseCase:
    """
    LLM応答一覧取得ユースケース

    LLM応答の一覧をページネーション付きで取得します。
    """

    def __init__(self, llm_response_repository: LLMResponseRepository):
        """
        Args:
            llm_response_repository: LLM応答リポジトリ
        """
        self.llm_response_repository = llm_response_repository

    def execute(self, skip: int = 0, limit: int = 100) -> list[LLMResponse]:
        """
        LLM応答一覧を取得します。

        Args:
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            LLM応答エンティティのリスト
        """
        return self.llm_response_repository.list(skip=skip, limit=limit)
