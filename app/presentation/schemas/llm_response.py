"""
LLMResponse スキーマ定義

from __future__ import annotations

LLM応答関連のAPI入出力スキーマを定義します。
Pydantic v2 を使用しています。
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.presentation.schemas.category import CategoryRef


class LLMProvider(str, Enum):
    """
    LLMプロバイダーの列挙型
    """

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OTHER = "other"


class LLMResponseBase(BaseModel):
    """
    LLM応答の基本スキーマ
    """

    title: str = Field(..., description="応答のタイトル", min_length=1, max_length=255)
    prompt: str = Field(..., description="LLMへの入力プロンプト")
    content_md: str = Field(..., description="応答内容（Markdown形式）")
    model: str = Field(..., description="使用したモデル名", max_length=100)
    provider: LLMProvider = Field(..., description="LLMプロバイダー")
    category_id: UUID | None = Field(None, description="所属カテゴリのID")
    tags: list[str] = Field(default_factory=list, description="タグのリスト")
    summary: str | None = Field(None, description="応答の要約")


class LLMResponseCreate(LLMResponseBase):
    """
    LLM応答作成リクエストスキーマ
    """

    pass


class LLMResponseUpdate(BaseModel):
    """
    LLM応答更新リクエストスキーマ

    すべてのフィールドがオプショナル（部分更新に対応）
    """

    title: str | None = Field(
        None, description="応答のタイトル", min_length=1, max_length=255
    )
    prompt: str | None = Field(None, description="LLMへの入力プロンプト")
    content_md: str | None = Field(None, description="応答内容（Markdown形式）")
    model: str | None = Field(None, description="使用したモデル名", max_length=100)
    provider: LLMProvider | None = Field(None, description="LLMプロバイダー")
    category_id: UUID | None = Field(None, description="所属カテゴリのID")
    tags: list[str] | None = Field(None, description="タグのリスト")
    summary: str | None = Field(None, description="応答の要約")


class LLMResponseRead(LLMResponseBase):
    """
    LLM応答取得レスポンススキーマ
    """

    id: UUID = Field(..., description="応答ID")
    storage_location: str = Field(..., description="ストレージの種類")
    storage_path: str | None = Field(None, description="実際のストレージパス")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    category: CategoryRef | None = Field(None, description="所属カテゴリ")

    model_config = ConfigDict(from_attributes=True)


class LLMResponseListItem(BaseModel):
    """
    LLM応答一覧の項目スキーマ（詳細は含まない）
    """

    id: UUID = Field(..., description="応答ID")
    title: str = Field(..., description="応答のタイトル")
    model: str = Field(..., description="使用したモデル名")
    provider: LLMProvider = Field(..., description="LLMプロバイダー")
    category_id: UUID | None = Field(None, description="所属カテゴリのID")
    tags: list[str] = Field(..., description="タグのリスト")
    summary: str | None = Field(None, description="応答の要約")
    created_at: datetime = Field(..., description="作成日時")

    model_config = ConfigDict(from_attributes=True)


class LLMResponseListResponse(BaseModel):
    """
    LLM応答一覧取得レスポンススキーマ
    """

    items: list[LLMResponseListItem] = Field(..., description="LLM応答のリスト")
    total: int = Field(..., description="総件数")
    skip: int = Field(..., description="スキップした件数")
    limit: int = Field(..., description="取得件数の上限")


class LLMResponseSearchQuery(BaseModel):
    """
    LLM応答検索クエリスキーマ
    """

    query: str | None = Field(
        None, description="検索文字列（タイトル、プロンプト、内容で検索）"
    )
    category_id: UUID | None = Field(None, description="カテゴリIDでフィルタ")
    tags: list[str] | None = Field(None, description="タグでフィルタ")
    skip: int = Field(0, description="スキップする件数", ge=0)
    limit: int = Field(100, description="取得する最大件数", ge=1, le=1000)


class Pagination(BaseModel):
    """
    ページネーション情報スキーマ
    """

    skip: int = Field(0, description="スキップする件数", ge=0)
    limit: int = Field(100, description="取得する最大件数", ge=1, le=1000)
