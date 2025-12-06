"""
ロギング設定モジュール

from __future__ import annotations

アプリケーション全体で使用するロギングの設定と、
関数の開始・終了ログを自動的に出力するデコレータを提供します。
"""

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar

from app.config.settings import settings

# 型変数定義
F = TypeVar("F", bound=Callable[..., Any])


def setup_logging() -> None:
    """
    ロギングの初期設定を行います。

    フォーマット: %(asctime)s - %(name)s - %(levelname)s - %(message)s
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # ルートロガーの設定
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # アプリケーションロガーの取得
    logger = logging.getLogger("app")
    logger.setLevel(log_level)

    logger.info(f"ロギング設定完了: レベル={settings.LOG_LEVEL}")


def log_function_call(logger: logging.Logger | None = None) -> Callable[[F], F]:
    """
    関数の開始と終了時にログを出力するデコレータ

    Args:
        logger: 使用するロガー。Noneの場合は関数のモジュール名からロガーを取得します。

    Returns:
        デコレートされた関数

    使用例:
        @log_function_call()
        def my_function(arg1: str, arg2: int) -> str:
            return f"{arg1}_{arg2}"
    """

    def decorator(func: F) -> F:
        # ロガーが指定されていない場合、関数のモジュール名から取得
        nonlocal logger
        if logger is None:
            logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 関数名とパラメータをログ出力
            func_name = func.__name__
            logger.info(f"関数開始: {func_name}")
            logger.debug(f"引数: args={args}, kwargs={kwargs}")

            try:
                # 関数実行
                result = func(*args, **kwargs)
                logger.info(f"関数終了: {func_name}")
                logger.debug(f"戻り値: {result}")
                return result
            except Exception as e:
                # エラー発生時のログ
                logger.error(f"関数エラー: {func_name} - {type(e).__name__}: {e}")
                raise

        return wrapper  # type: ignore

    return decorator
