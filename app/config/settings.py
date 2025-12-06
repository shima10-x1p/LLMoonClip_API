"""
アプリケーション設定モジュール

from __future__ import annotations

pydantic-settingsを使用して環境変数から設定を読み込みます。
"""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    アプリケーション設定クラス

    環境変数または .env ファイルから設定値を読み込みます。
    """

    # データベース設定
    DATABASE_URL: str = "sqlite:///./llmoonclip.db"

    # アプリケーション環境
    APP_ENV: Literal["development", "staging", "production"] = "development"

    # ログレベル
    LOG_LEVEL: str = "INFO"

    # ストレージパス（Markdownファイル保存先）
    STORAGE_PATH: Path = Path("./storage/markdown")

    # pydantic-settings 設定
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# グローバル設定インスタンス
settings = Settings()
