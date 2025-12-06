"""
FastAPI アプリケーション

from __future__ import annotations

LLM応答管理バックエンドのメインアプリケーション。
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging import setup_logging
from app.infrastructure.db.base import init_db
from app.presentation.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    アプリケーションのライフサイクルイベント

    起動時と終了時の処理を定義します。
    """
    # 起動時の処理
    setup_logging()
    init_db()  # データベースの初期化（テーブル作成）
    yield
    # 終了時の処理（必要であればここに記述）


# FastAPIアプリケーションの作成
app = FastAPI(
    title="LLMoonClip API",
    description="LLM応答を管理するバックエンドAPI",
    version="0.1.0",
    lifespan=lifespan,
)

# CORSミドルウェアの設定（開発用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 ルーターの登録
app.include_router(api_v1_router)


@app.get("/", tags=["root"])
def root():
    """
    ルートエンドポイント

    APIの基本情報を返します。
    """
    return {
        "message": "LLMoonClip API",
        "version": "0.1.0",
        "docs": "/docs",
    }


# 開発用: uvicorn で直接起動する場合
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
