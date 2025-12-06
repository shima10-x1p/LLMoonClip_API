"""
LLMResponseRepository の実装

SQLAlchemyを使用したLLM応答リポジトリの実装。
ORMモデルとドメインエンティティ間のマッピングを行います。
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.models.llm_response import LLMProvider, LLMResponse
from app.domain.repositories.llm_response_repository import LLMResponseRepository
from app.infrastructure.db.models import LLMResponseORM


class LLMResponseRepositoryImpl(LLMResponseRepository):
    """
    SQLAlchemy を使用したLLM応答リポジトリの実装
    """

    def __init__(self, db: Session):
        """
        リポジトリを初期化します。

        Args:
            db: SQLAlchemyセッション
        """
        self.db = db

    def _to_domain(self, orm_model: LLMResponseORM) -> LLMResponse:
        """
        ORMモデルをドメインエンティティに変換します。

        Args:
            orm_model: LLMResponseORM インスタンス

        Returns:
            LLMResponse ドメインエンティティ
        """
        return LLMResponse(
            id=UUID(orm_model.id),
            title=orm_model.title,
            prompt=orm_model.prompt,
            content_md=orm_model.content_md,
            model=orm_model.model,
            provider=LLMProvider(orm_model.provider),
            category_id=UUID(orm_model.category_id) if orm_model.category_id else None,
            tags=orm_model.tags if orm_model.tags else [],
            summary=orm_model.summary,
            storage_location=orm_model.storage_location,
            storage_path=orm_model.storage_path,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
        )

    def _to_orm(self, domain_model: LLMResponse) -> LLMResponseORM:
        """
        ドメインエンティティをORMモデルに変換します。

        Args:
            domain_model: LLMResponse ドメインエンティティ

        Returns:
            LLMResponseORM インスタンス
        """
        return LLMResponseORM(
            id=str(domain_model.id),
            title=domain_model.title,
            prompt=domain_model.prompt,
            content_md=domain_model.content_md,
            model=domain_model.model,
            provider=domain_model.provider.value,
            category_id=str(domain_model.category_id)
            if domain_model.category_id
            else None,
            tags=domain_model.tags,
            summary=domain_model.summary,
            storage_location=domain_model.storage_location,
            storage_path=domain_model.storage_path,
            created_at=domain_model.created_at,
            updated_at=domain_model.updated_at,
        )

    def get_by_id(self, response_id: UUID) -> LLMResponse | None:
        """IDでLLM応答を取得します"""
        orm_model = (
            self.db.query(LLMResponseORM)
            .filter(LLMResponseORM.id == str(response_id))
            .first()
        )
        return self._to_domain(orm_model) if orm_model else None

    def list(self, skip: int = 0, limit: int = 100) -> list[LLMResponse]:
        """LLM応答のリストを取得します"""
        orm_models = (
            self.db.query(LLMResponseORM)
            .order_by(LLMResponseORM.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain(orm_model) for orm_model in orm_models]

    def search(
        self,
        query: str | None = None,
        category_id: UUID | None = None,
        tags: list[str] | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[LLMResponse]:
        """LLM応答を検索します"""
        db_query = self.db.query(LLMResponseORM)

        # テキスト検索（タイトル、プロンプト、内容）
        if query:
            search_pattern = f"%{query}%"
            db_query = db_query.filter(
                (LLMResponseORM.title.like(search_pattern))
                | (LLMResponseORM.prompt.like(search_pattern))
                | (LLMResponseORM.content_md.like(search_pattern))
            )

        # カテゴリでフィルタ
        if category_id:
            db_query = db_query.filter(LLMResponseORM.category_id == str(category_id))

        # タグでフィルタ（JSON配列内の要素を検索）
        # 注: SQLiteでは簡易的な実装、PostgreSQLではより高度な検索が可能
        if tags:
            for tag in tags:
                db_query = db_query.filter(LLMResponseORM.tags.contains(tag))

        orm_models = (
            db_query.order_by(LLMResponseORM.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain(orm_model) for orm_model in orm_models]

    def create(self, response: LLMResponse) -> LLMResponse:
        """LLM応答を作成します"""
        orm_model = self._to_orm(response)
        self.db.add(orm_model)
        self.db.commit()
        self.db.refresh(orm_model)
        return self._to_domain(orm_model)

    def update(self, response: LLMResponse) -> LLMResponse:
        """LLM応答を更新します"""
        orm_model = (
            self.db.query(LLMResponseORM)
            .filter(LLMResponseORM.id == str(response.id))
            .first()
        )
        if orm_model:
            orm_model.title = response.title
            orm_model.prompt = response.prompt
            orm_model.content_md = response.content_md
            orm_model.model = response.model
            orm_model.provider = response.provider.value
            orm_model.category_id = (
                str(response.category_id) if response.category_id else None
            )
            orm_model.tags = response.tags
            orm_model.summary = response.summary
            orm_model.updated_at = response.updated_at
            self.db.commit()
            self.db.refresh(orm_model)
            return self._to_domain(orm_model)
        return response

    def delete(self, response_id: UUID) -> bool:
        """LLM応答を削除します"""
        result = (
            self.db.query(LLMResponseORM)
            .filter(LLMResponseORM.id == str(response_id))
            .delete()
        )
        self.db.commit()
        return result > 0
