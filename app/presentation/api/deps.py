"""
FastAPI 共通依存関数

from __future__ import annotations

エンドポイントで使用する共通の依存関数を定義します。
"""

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.base import get_db
from app.infrastructure.repositories.category_repository_impl import (
    CategoryRepositoryImpl,
)
from app.infrastructure.repositories.llm_response_repository_impl import (
    LLMResponseRepositoryImpl,
)


# データベースセッション依存
def get_database() -> Generator[Session]:
    """
    データベースセッションを取得します。

    Yields:
        Session: SQLAlchemyセッション
    """
    yield from get_db()


# リポジトリ依存
def get_category_repository(
    db: Session = Depends(get_database),
) -> CategoryRepositoryImpl:
    """
    カテゴリリポジトリを取得します。

    Args:
        db: データベースセッション

    Returns:
        CategoryRepositoryImpl: カテゴリリポジトリ実装
    """
    return CategoryRepositoryImpl(db)


def get_llm_response_repository(
    db: Session = Depends(get_database),
) -> LLMResponseRepositoryImpl:
    """
    LLM応答リポジトリを取得します。

    Args:
        db: データベースセッション

    Returns:
        LLMResponseRepositoryImpl: LLM応答リポジトリ実装
    """
    return LLMResponseRepositoryImpl(db)
