"""
ドメインモデル: LLMResponse

from __future__ import annotations

LLM応答を表すドメインエンティティ。
フレームワークに依存しない純粋なPythonクラスとして実装。
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class LLMProvider(str, Enum):
    """
    LLMプロバイダーの列挙型
    """

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OTHER = "other"


@dataclass
class LLMResponse:
    """
    LLM応答エンティティ

    LLM（ChatGPT, Gemini等）からの応答とそのメタデータを表します。

    Attributes:
        id: 応答の一意識別子
        title: 応答のタイトル
        prompt: LLMへの入力プロンプト
        content_md: 応答内容（Markdown形式）
        model: 使用したモデル名
        provider: LLMプロバイダー
        category_id: 所属カテゴリのID
        tags: タグのリスト
        summary: 応答の要約
        storage_location: ストレージの種類（file, s3等）
        storage_path: 実際のストレージパス
        created_at: 作成日時
        updated_at: 更新日時
    """

    title: str
    prompt: str
    content_md: str
    model: str
    provider: LLMProvider
    category_id: UUID | None = None
    tags: list[str] = field(default_factory=list)
    summary: str | None = None
    storage_location: str = "file"
    storage_path: str | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update(
        self,
        title: str | None = None,
        prompt: str | None = None,
        content_md: str | None = None,
        model: str | None = None,
        provider: LLMProvider | None = None,
        category_id: UUID | None = None,
        tags: list[str] | None = None,
        summary: str | None = None,
    ) -> None:
        """
        LLM応答情報を更新します。

        Args:
            title: 新しいタイトル
            prompt: 新しいプロンプト
            content_md: 新しい応答内容
            model: 新しいモデル名
            provider: 新しいプロバイダー
            category_id: 新しいカテゴリID
            tags: 新しいタグリスト
            summary: 新しい要約
        """
        if title is not None:
            self.title = title
        if prompt is not None:
            self.prompt = prompt
        if content_md is not None:
            self.content_md = content_md
        if model is not None:
            self.model = model
        if provider is not None:
            self.provider = provider
        if category_id is not None:
            self.category_id = category_id
        if tags is not None:
            self.tags = tags
        if summary is not None:
            self.summary = summary
        self.updated_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        """
        タグを追加します。

        Args:
            tag: 追加するタグ
        """
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        """
        タグを削除します。

        Args:
            tag: 削除するタグ
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

    def __str__(self) -> str:
        """文字列表現"""
        return f"LLMResponse(id={self.id}, title={self.title})"
