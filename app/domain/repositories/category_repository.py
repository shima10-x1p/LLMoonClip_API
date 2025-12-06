"""
ドメインリポジトリインターフェイス: CategoryRepository

カテゴリの永続化を担当するリポジトリのインターフェイス（ポート）。
実装はインフラストラクチャ層で行います。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.category import Category


class CategoryRepository(ABC):
    """
    カテゴリリポジトリのインターフェイス

    カテゴリの永続化操作を定義します。
    具体的な実装はインフラストラクチャ層で行います。
    """

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Category | None:
        """
        IDでカテゴリを取得します。

        Args:
            category_id: 取得するカテゴリのID

        Returns:
            カテゴリエンティティ。存在しない場合はNone
        """
        pass

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> list[Category]:
        """
        カテゴリのリストを取得します。

        Args:
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            カテゴリエンティティのリスト
        """
        pass

    @abstractmethod
    def create(self, category: Category) -> Category:
        """
        カテゴリを作成します。

        Args:
            category: 作成するカテゴリエンティティ

        Returns:
            作成されたカテゴリエンティティ
        """
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        """
        カテゴリを更新します。

        Args:
            category: 更新するカテゴリエンティティ

        Returns:
            更新されたカテゴリエンティティ
        """
        pass

    @abstractmethod
    def delete(self, category_id: UUID) -> bool:
        """
        カテゴリを削除します。

        Args:
            category_id: 削除するカテゴリのID

        Returns:
            削除が成功した場合True、失敗した場合False
        """
        pass
