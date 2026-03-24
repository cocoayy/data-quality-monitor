# data-quality-monitor

オープンデータ向けのデータ品質監視ツール

## 概要
データ品質を以下の観点で評価・監視する:
- Completeness
- Freshness
- Accessibility
- Format Quality

## 技術スタック
- Frontend: Next.js
- Backend: FastAPI
- Database: PostgreSQL
- Batch: Python
- Infra: Docker Compose

## ディレクトリ構成

```text
backend/   # API
frontend/  # UI
batch/     # スコア計算バッチ
infra/     # インフラ関連
docs/      # 設計資料