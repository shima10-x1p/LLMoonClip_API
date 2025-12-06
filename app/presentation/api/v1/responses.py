"""
LLM応答 API エンドポイント

from __future__ import annotations

LLM応答関連のCRUD・検索操作を提供するAPIエンドポイントを定義します。
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.use_cases.create_response import CreateResponseUseCase
from app.application.use_cases.list_responses import ListResponsesUseCase
from app.application.use_cases.search_responses import SearchResponsesUseCase
from app.application.use_cases.update_response import UpdateResponseUseCase
from app.domain.repositories.llm_response_repository import LLMResponseRepository
from app.presentation.api.deps import get_llm_response_repository
from app.presentation.schemas.llm_response import (
    LLMResponseCreate,
    LLMResponseListResponse,
    LLMResponseRead,
    LLMResponseUpdate,
)

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post(
    "",
    response_model=LLMResponseRead,
    status_code=status.HTTP_201_CREATED,
    summary="LLM応答を作成",
)
def create_response(
    response_data: LLMResponseCreate,
    repository: LLMResponseRepository = Depends(get_llm_response_repository),
):
    """
    新しいLLM応答を作成します。
    """
    use_case = CreateResponseUseCase(repository)
    llm_response = use_case.execute(
        title=response_data.title,
        prompt=response_data.prompt,
        content_md=response_data.content_md,
        model=response_data.model,
        provider=response_data.provider,
        category_id=response_data.category_id,
        tags=response_data.tags,
        summary=response_data.summary,
    )
    return llm_response


@router.get("", response_model=LLMResponseListResponse, summary="LLM応答一覧を取得")
def list_responses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repository: LLMResponseRepository = Depends(get_llm_response_repository),
):
    """
    LLM応答の一覧を取得します。
    """
    use_case = ListResponsesUseCase(repository)
    responses = use_case.execute(skip=skip, limit=limit)
    return LLMResponseListResponse(
        items=responses, total=len(responses), skip=skip, limit=limit
    )


@router.get("/search", response_model=LLMResponseListResponse, summary="LLM応答を検索")
def search_responses(
    query: str | None = Query(None, description="検索文字列"),
    category_id: UUID | None = Query(None, description="カテゴリID"),
    tags: list[str] | None = Query(None, description="タグ"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repository: LLMResponseRepository = Depends(get_llm_response_repository),
):
    """
    LLM応答を検索します。
    """
    use_case = SearchResponsesUseCase(repository)
    responses = use_case.execute(
        query=query, category_id=category_id, tags=tags, skip=skip, limit=limit
    )
    return LLMResponseListResponse(
        items=responses, total=len(responses), skip=skip, limit=limit
    )


@router.get("/{response_id}", response_model=LLMResponseRead, summary="LLM応答を取得")
def get_response(
    response_id: UUID,
    repository: LLMResponseRepository = Depends(get_llm_response_repository),
):
    """
    IDでLLM応答を取得します。
    """
    llm_response = repository.get_by_id(response_id)
    if not llm_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="LLM応答が見つかりません"
        )
    return llm_response


@router.put("/{response_id}", response_model=LLMResponseRead, summary="LLM応答を更新")
def update_response(
    response_id: UUID,
    response_data: LLMResponseUpdate,
    repository: LLMResponseRepository = Depends(get_llm_response_repository),
):
    """
    LLM応答を更新します。
    """
    use_case = UpdateResponseUseCase(repository)
    updated_response = use_case.execute(
        response_id=response_id,
        title=response_data.title,
        prompt=response_data.prompt,
        content_md=response_data.content_md,
        model=response_data.model,
        provider=response_data.provider,
        category_id=response_data.category_id,
        tags=response_data.tags,
        summary=response_data.summary,
    )
    if not updated_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="LLM応答が見つかりません"
        )
    return updated_response


@router.delete(
    "/{response_id}", status_code=status.HTTP_204_NO_CONTENT, summary="LLM応答を削除"
)
def delete_response(
    response_id: UUID,
    repository: LLMResponseRepository = Depends(get_llm_response_repository),
):
    """
    LLM応答を削除します。
    """
    success = repository.delete(response_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="LLM応答が見つかりません"
        )
