"""
SQLAlchemy ORM モデル定義

from __future__ import annotations

データベーステーブルに対応するORMモデルを定義します。
ドメインモデルとのマッピングはリポジトリ層で行います。
"""

import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class CategoryORM(Base):
    """
    カテゴリテーブルのORMモデル
    """

    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # リレーション: このカテゴリに属するLLM応答
    llm_responses = relationship(
        "LLMResponseORM", back_populates="category", cascade="all, delete-orphan"
    )


class LLMResponseORM(Base):
    """
    LLM応答テーブルのORMモデル
    """

    __tablename__ = "llm_responses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    content_md = Column(Text, nullable=False)
    model = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    tags = Column(JSON, default=list, nullable=False)  # タグのリストをJSON形式で保存
    summary = Column(Text, nullable=True)
    storage_location = Column(String(50), default="file", nullable=False)
    storage_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # リレーション: 所属カテゴリ
    category = relationship("CategoryORM", back_populates="llm_responses")
