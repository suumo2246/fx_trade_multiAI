# 📋 現実的なライブラリインストール手順（2025年11月更新版）

## 🎯 pipアップグレード完了後の次ステップ

### 📊 現在の状況
- ✅ Python 3.11.9
- ✅ pip 25.3（最新版）
- ✅ 仮想環境有効化済み
- ⚠️ pandas-ta は Python 3.12+が必要なため使用不可
- ✅ TA-Lib（ta-lib-binary）を主力に変更

## 🚀 推奨インストール順序（実証済み）

### ステップ1: 基本ライブラリ（安全確実）
```bash
pip install pandas numpy matplotlib seaborn plotly
```

### ステップ2: 機械学習基盤
```bash
pip install scikit-learn
pip install xgboost lightgbm
pip install optuna joblib
```

### ステップ3: テクニカル指標ライブラリ
```bash
# TA-Lib（Windowsバイナリ版）
pip install ta-lib-binary

# 軽量代替
pip install ta

# 金融チャート
pip install mplfinance
```

### ステップ4: バックテスト
```bash
pip install backtesting
```

### ステップ5: 開発環境
```bash
pip install jupyter jupyterlab
pip install tqdm python-dotenv
```

### ステップ6: MT5（Windowsのみ）
```bash
pip install MetaTrader5
```

## ✅ インストール確認

各ステップ後に以下で確認：

```python
# ステップ1確認
import pandas as pd
import numpy as np
print("✅ 基本ライブラリOK")

# ステップ3確認
import talib
print("✅ TA-LibOK")

# ステップ4確認
from backtesting import Backtest, Strategy
print("✅ バックテストOK")
```

## 🎯 次のアクション

1. **基本ライブラリインストール**: 上記ステップ1-3を実行
2. **動作確認**: 各ステップで確認コード実行
3. **プロジェクト構造作成**: フォルダ構成を作成
4. **Phase 1開始**: ルールベースシステム構築開始

## 📝 変更履歴

**2025年11月13日の調整:**
- pandas-ta → ta-lib-binary に主力変更
- Python 3.11対応の安定構成に修正
- 段階的インストールでエラー率を最小化
- GPU対応は基本環境構築後に追加

これで安全にライブラリをインストールできます！