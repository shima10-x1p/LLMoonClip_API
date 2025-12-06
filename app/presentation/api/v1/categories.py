"""
カテゴリ API エンドポイント

from __future__ import annotations

カテゴリ関連のCRUD操作を提供するAPIエンドポイントを定義します。
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.create_category import CreateCategoryUseCase
from app.application.use_cases.list_categories import ListCategoriesUseCase
from app.domain.repositories.category_repository import CategoryRepository
from app.presentation.api.deps import get_category_repository
from app.presentation.schemas.category import (
    CategoryCreate,
    CategoryListResponse,
    CategoryRead,
    CategoryUpdate,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="カテゴリを作成",
)
def create_category(
    category_data: CategoryCreate,
    repository: CategoryRepository = Depends(get_category_repository),
):
    """
    新しいカテゴリを作成します。
    """
    use_case = CreateCategoryUseCase(repository)
    category = use_case.execute(
        name=category_data.name, description=category_data.description
    )
    return category


@router.get("", response_model=CategoryListResponse, summary="カテゴリ一覧を取得")
def list_categories(
    skip: int = 0,
    limit: int = 100,
    repository: CategoryRepository = Depends(get_category_repository),
):
    """
    カテゴリの一覧を取得します。
    """
    use_case = ListCategoriesUseCase(repository)
    categories = use_case.execute(skip=skip, limit=limit)
    return CategoryListResponse(
        items=categories, total=len(categories), skip=skip, limit=limit
    )


@router.get("/{category_id}", response_model=CategoryRead, summary="カテゴリを取得")
def get_category(
    category_id: UUID,
    repository: CategoryRepository = Depends(get_category_repository),
):
    """
    IDでカテゴリを取得します。
    """
    category = repository.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="カテゴリが見つかりません"
        )
    return category


@router.put("/{category_id}", response_model=CategoryRead, summary="カテゴリを更新")
def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    repository: CategoryRepository = Depends(get_category_repository),
):
    """
    カテゴリを更新します。
    """
    category = repository.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="カテゴリが見つかりません"
        )

    category.update(name=category_data.name, description=category_data.description)
    updated_category = repository.update(category)
    return updated_category


@router.delete(
    "/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="カテゴリを削除"
)
def delete_category(
    category_id: UUID,
    repository: CategoryRepository = Depends(get_category_repository),
):
    """
    カテゴリを削除します。
    """
    success = repository.delete(category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="カテゴリが見つかりません"
        )
