"""
ドメインリポジトリインターフェイス: LLMResponseRepository

LLM応答の永続化を担当するリポジトリのインターフェイス（ポート）。
実装はインフラストラクチャ層で行います。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.llm_response import LLMResponse


class LLMResponseRepository(ABC):
    """
    LLM応答リポジトリのインターフェイス

    LLM応答の永続化操作を定義します。
    具体的な実装はインフラストラクチャ層で行います。
    """

    @abstractmethod
    def get_by_id(self, response_id: UUID) -> LLMResponse | None:
        """
        IDでLLM応答を取得します。

        Args:
            response_id: 取得するLLM応答のID

        Returns:
            LLM応答エンティティ。存在しない場合はNone
        """
        pass

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> list[LLMResponse]:
        """
        LLM応答のリストを取得します。

        Args:
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            LLM応答エンティティのリスト
        """
        pass

    @abstractmethod
    def search(
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
        pass

    @abstractmethod
    def create(self, response: LLMResponse) -> LLMResponse:
        """
        LLM応答を作成します。

        Args:
            response: 作成するLLM応答エンティティ

        Returns:
            作成されたLLM応答エンティティ
        """
        pass

    @abstractmethod
    def update(self, response: LLMResponse) -> LLMResponse:
        """
        LLM応答を更新します。

        Args:
            response: 更新するLLM応答エンティティ

        Returns:
            更新されたLLM応答エンティティ
        """
        pass

    @abstractmethod
    def delete(self, response_id: UUID) -> bool:
        """
        LLM応答を削除します。

        Args:
            response_id: 削除するLLM応答のID

        Returns:
            削除が成功した場合True、失敗した場合False
        """
        pass
