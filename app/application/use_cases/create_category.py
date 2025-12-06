"""
カテゴリ作成ユースケース

from __future__ import annotations
"""

from app.domain.models.category import Category
from app.domain.repositories.category_repository import CategoryRepository


class CreateCategoryUseCase:
    """
    カテゴリ作成ユースケース

    新しいカテゴリを作成します。
    """

    def __init__(self, category_repository: CategoryRepository):
        """
        Args:
            category_repository: カテゴリリポジトリ
        """
        self.category_repository = category_repository

    def execute(self, name: str, description: str | None = None) -> Category:
        """
        カテゴリを作成します。

        Args:
            name: カテゴリ名
            description: カテゴリの説明

        Returns:
            作成されたカテゴリエンティティ
        """
        # 新しいカテゴリエンティティを作成
        category = Category(name=name, description=description)

        # リポジトリに永続化
        created_category = self.category_repository.create(category)

        return created_category
