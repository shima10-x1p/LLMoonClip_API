"""
CategoryRepository の実装

from __future__ import annotations

SQLAlchemyを使用したカテゴリリポジトリの実装。
ORMモデルとドメインエンティティ間のマッピングを行います。
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.models.category import Category
from app.domain.repositories.category_repository import CategoryRepository
from app.infrastructure.db.models import CategoryORM


class CategoryRepositoryImpl(CategoryRepository):
    """
    SQLAlchemy を使用したカテゴリリポジトリの実装
    """

    def __init__(self, db: Session):
        """
        リポジトリを初期化します。

        Args:
            db: SQLAlchemyセッション
        """
        self.db = db

    def _to_domain(self, orm_model: CategoryORM) -> Category:
        """
        ORMモデルをドメインエンティティに変換します。

        Args:
            orm_model: CategoryORM インスタンス

        Returns:
            Category ドメインエンティティ
        """
        return Category(
            id=UUID(orm_model.id),
            name=orm_model.name,
            description=orm_model.description,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
        )

    def _to_orm(self, domain_model: Category) -> CategoryORM:
        """
        ドメインエンティティをORMモデルに変換します。

        Args:
            domain_model: Category ドメインエンティティ

        Returns:
            CategoryORM インスタンス
        """
        return CategoryORM(
            id=str(domain_model.id),
            name=domain_model.name,
            description=domain_model.description,
            created_at=domain_model.created_at,
            updated_at=domain_model.updated_at,
        )

    def get_by_id(self, category_id: UUID) -> Category | None:
        """IDでカテゴリを取得します"""
        orm_model = (
            self.db.query(CategoryORM)
            .filter(CategoryORM.id == str(category_id))
            .first()
        )
        return self._to_domain(orm_model) if orm_model else None

    def list(self, skip: int = 0, limit: int = 100) -> list[Category]:
        """カテゴリのリストを取得します"""
        orm_models = self.db.query(CategoryORM).offset(skip).limit(limit).all()
        return [self._to_domain(orm_model) for orm_model in orm_models]

    def create(self, category: Category) -> Category:
        """カテゴリを作成します"""
        orm_model = self._to_orm(category)
        self.db.add(orm_model)
        self.db.commit()
        self.db.refresh(orm_model)
        return self._to_domain(orm_model)

    def update(self, category: Category) -> Category:
        """カテゴリを更新します"""
        orm_model = (
            self.db.query(CategoryORM)
            .filter(CategoryORM.id == str(category.id))
            .first()
        )
        if orm_model:
            orm_model.name = category.name
            orm_model.description = category.description
            orm_model.updated_at = category.updated_at
            self.db.commit()
            self.db.refresh(orm_model)
            return self._to_domain(orm_model)
        return category

    def delete(self, category_id: UUID) -> bool:
        """カテゴリを削除します"""
        result = (
            self.db.query(CategoryORM)
            .filter(CategoryORM.id == str(category_id))
            .delete()
        )
        self.db.commit()
        return result > 0
