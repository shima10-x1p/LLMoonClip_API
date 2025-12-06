"""
データベース基盤モジュール

from __future__ import annotations

SQLAlchemyのエンジン、セッション、ベースクラスを定義します。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config.settings import settings

# SQLAlchemy エンジンの作成
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.APP_ENV == "development",  # 開発環境ではSQLをログ出力
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.DATABASE_URL
    else {},
)

# セッションファクトリの作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """
    SQLAlchemy ORM モデルのベースクラス

    すべてのORMモデルはこのクラスを継承します。
    """

    pass


def get_db():
    """
    データベースセッションを取得するジェネレータ

    FastAPIの依存関数として使用します。

    Yields:
        Session: データベースセッション
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    データベースを初期化します。

    すべてのテーブルを作成します。
    本番環境ではAlembicマイグレーションを使用することを推奨します。
    """
    Base.metadata.create_all(bind=engine)
