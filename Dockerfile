# ========================================
# ビルダーステージ
# ========================================
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定（Pythonのバイトコード生成を無効化）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# プロジェクトファイルをコピー
COPY pyproject.toml uv.lock ./

# 依存関係を同期（本番用のみ、開発用依存関係は除外）
RUN uv sync --frozen --no-dev

# アプリケーションコードをコピー
COPY app ./app

# ========================================
# 実行ステージ
# ========================================
FROM python:3.13-slim-bookworm AS runtime

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# 非rootユーザーを作成
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin appuser && \
    chown -R appuser:appuser /app

# ビルダーステージから仮想環境とアプリケーションコードをコピー
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /app/app /app/app

# 非rootユーザーに切り替え
USER appuser

# ポート8000を公開
EXPOSE 8000

# ヘルスチェックを設定
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')"

# FastAPIアプリケーションを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
