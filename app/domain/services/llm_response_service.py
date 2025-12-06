"""
ドメインサービス: LLMResponseService

from __future__ import annotations

複数のリポジトリにまたがるドメインロジックを実装します。
現段階では薄い実装とし、必要に応じて拡張します。
"""

from app.domain.models.llm_response import LLMResponse
from app.domain.repositories.category_repository import CategoryRepository
from app.domain.repositories.llm_response_repository import LLMResponseRepository


class LLMResponseService:
    """
    LLM応答に関するドメインサービス

    複数のリポジトリやエンティティにまたがるビジネスロジックを実装します。
    """

    def __init__(
        self,
        response_repository: LLMResponseRepository,
        category_repository: CategoryRepository,
    ):
        """
        サービスを初期化します。

        Args:
            response_repository: LLM応答リポジトリ
            category_repository: カテゴリリポジトリ
        """
        self.response_repository = response_repository
        self.category_repository = category_repository

    def validate_category_exists(self, response: LLMResponse) -> bool:
        """
        LLM応答に紐づくカテゴリが存在するか検証します。

        Args:
            response: 検証するLLM応答エンティティ

        Returns:
            カテゴリが存在する場合True、存在しない場合False
        """
        if response.category_id is None:
            return True  # カテゴリIDがNoneの場合は検証不要

        category = self.category_repository.get_by_id(response.category_id)
        return category is not None

    # 将来的に追加する可能性のあるメソッド:
    # - タグの正規化
    # - 応答の重複チェック
    # - カテゴリの移動
    # など
