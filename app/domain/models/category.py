"""
ドメインモデル: Category

from __future__ import annotations

カテゴリを表すドメインエンティティ。
フレームワークに依存しない純粋なPythonクラスとして実装。
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Category:
    """
    カテゴリエンティティ

    LLM応答を分類するためのカテゴリを表します。

    Attributes:
        id: カテゴリの一意識別子
        name: カテゴリ名
        description: カテゴリの説明
        created_at: 作成日時
        updated_at: 更新日時
    """

    name: str
    description: str | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update(self, name: str | None = None, description: str | None = None) -> None:
        """
        カテゴリ情報を更新します。

        Args:
            name: 新しいカテゴリ名（Noneの場合は更新しない）
            description: 新しい説明（Noneの場合は更新しない）
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        """文字列表現"""
        return f"Category(id={self.id}, name={self.name})"
