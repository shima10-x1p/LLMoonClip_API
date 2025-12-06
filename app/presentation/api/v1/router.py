"""
API v1 ルーター

from __future__ import annotations

API バージョン 1 のすべてのエンドポイントを統合します。
"""

from fastapi import APIRouter

from app.presentation.api.v1 import categories, responses

# v1 APIルーターの作成
api_v1_router = APIRouter(prefix="/api/v1")

# 各リソースのルーターを登録
api_v1_router.include_router(categories.router)
api_v1_router.include_router(responses.router)
