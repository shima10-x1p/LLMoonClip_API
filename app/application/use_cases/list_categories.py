"""
カテゴリ一覧取得ユースケース

from __future__ import annotations
"""

from app.domain.models.category import Category
from app.domain.repositories.category_repository import CategoryRepository


class ListCategoriesUseCase:
    """
    カテゴリ一覧取得ユースケース

    カテゴリの一覧をページネーション付きで取得します。
    """

    def __init__(self, category_repository: CategoryRepository):
        """
        Args:
            category_repository: カテゴリリポジトリ
        """
        self.category_repository = category_repository

    def execute(self, skip: int = 0, limit: int = 100) -> list[Category]:
        """
        カテゴリ一覧を取得します。

        Args:
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            カテゴリエンティティのリスト
        """
        return self.category_repository.list(skip=skip, limit=limit)
