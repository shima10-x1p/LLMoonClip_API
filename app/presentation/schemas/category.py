"""
Category スキーマ定義

from __future__ import annotations

カテゴリ関連のAPI入出力スキーマを定義します。
Pydantic v2 を使用しています。
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    """
    カテゴリの基本スキーマ
    """

    name: str = Field(..., description="カテゴリ名", min_length=1, max_length=255)
    description: str | None = Field(None, description="カテゴリの説明")


class CategoryCreate(CategoryBase):
    """
    カテゴリ作成リクエストスキーマ
    """

    pass


class CategoryUpdate(CategoryBase):
    """
    カテゴリ更新リクエストスキーマ

    すべてのフィールドがオプショナル（部分更新に対応）
    """

    name: str | None = Field(
        None, description="カテゴリ名", min_length=1, max_length=255
    )
    description: str | None = Field(None, description="カテゴリの説明")


class CategoryRef(BaseModel):
    """
    カテゴリ参照スキーマ（他のエンティティから参照される場合）
    """

    id: UUID = Field(..., description="カテゴリID")
    name: str = Field(..., description="カテゴリ名")

    model_config = ConfigDict(from_attributes=True)


class CategoryRead(CategoryBase):
    """
    カテゴリ取得レスポンススキーマ
    """

    id: UUID = Field(..., description="カテゴリID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")

    model_config = ConfigDict(from_attributes=True)


class CategoryListResponse(BaseModel):
    """
    カテゴリ一覧取得レスポンススキーマ
    """

    items: list[CategoryRead] = Field(..., description="カテゴリのリスト")
    total: int = Field(..., description="総件数")
    skip: int = Field(..., description="スキップした件数")
    limit: int = Field(..., description="取得件数の上限")
