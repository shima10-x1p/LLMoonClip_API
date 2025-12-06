"""
LLM応答更新ユースケース

from __future__ import annotations
"""

from uuid import UUID

from app.domain.models.llm_response import LLMProvider, LLMResponse
from app.domain.repositories.llm_response_repository import LLMResponseRepository


class UpdateResponseUseCase:
    """
    LLM応答更新ユースケース

    既存のLLM応答を更新します。
    """

    def __init__(self, llm_response_repository: LLMResponseRepository):
        """
        Args:
            llm_response_repository: LLM応答リポジトリ
        """
        self.llm_response_repository = llm_response_repository

    def execute(
        self,
        response_id: UUID,
        title: str | None = None,
        prompt: str | None = None,
        content_md: str | None = None,
        model: str | None = None,
        provider: LLMProvider | None = None,
        category_id: UUID | None = None,
        tags: list[str] | None = None,
        summary: str | None = None,
    ) -> LLMResponse | None:
        """
        LLM応答を更新します。

        Args:
            response_id: 更新するLLM応答のID
            title: 新しいタイトル
            prompt: 新しいプロンプト
            content_md: 新しい応答内容
            model: 新しいモデル名
            provider: 新しいプロバイダー
            category_id: 新しいカテゴリID
            tags: 新しいタグリスト
            summary: 新しい要約

        Returns:
            更新されたLLM応答エンティティ。存在しない場合はNone
        """
        # 既存のLLM応答を取得
        existing_response = self.llm_response_repository.get_by_id(response_id)
        if not existing_response:
            return None

        # 応答を更新
        existing_response.update(
            title=title,
            prompt=prompt,
            content_md=content_md,
            model=model,
            provider=provider,
            category_id=category_id,
            tags=tags,
            summary=summary,
        )

        # リポジトリに永続化
        updated_response = self.llm_response_repository.update(existing_response)

        return updated_response
