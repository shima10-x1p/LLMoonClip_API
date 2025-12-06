"""
LLM応答作成ユースケース

from __future__ import annotations
"""

from uuid import UUID

from app.domain.models.llm_response import LLMProvider, LLMResponse
from app.domain.repositories.llm_response_repository import LLMResponseRepository


class CreateResponseUseCase:
    """
    LLM応答作成ユースケース

    新しいLLM応答を作成します。
    """

    def __init__(self, llm_response_repository: LLMResponseRepository):
        """
        Args:
            llm_response_repository: LLM応答リポジトリ
        """
        self.llm_response_repository = llm_response_repository

    def execute(
        self,
        title: str,
        prompt: str,
        content_md: str,
        model: str,
        provider: LLMProvider,
        category_id: UUID | None = None,
        tags: list[str] | None = None,
        summary: str | None = None,
    ) -> LLMResponse:
        """
        LLM応答を作成します。

        Args:
            title: 応答のタイトル
            prompt: LLMへの入力プロンプト
            content_md: 応答内容（Markdown形式）
            model: 使用したモデル名
            provider: LLMプロバイダー
            category_id: 所属カテゴリのID
            tags: タグのリスト
            summary: 応答の要約

        Returns:
            作成されたLLM応答エンティティ
        """
        # 新しいLLM応答エンティティを作成
        llm_response = LLMResponse(
            title=title,
            prompt=prompt,
            content_md=content_md,
            model=model,
            provider=provider,
            category_id=category_id,
            tags=tags if tags else [],
            summary=summary,
        )

        # リポジトリに永続化
        created_response = self.llm_response_repository.create(llm_response)

        return created_response
