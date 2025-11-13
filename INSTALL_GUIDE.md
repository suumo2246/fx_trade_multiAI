# 📚 FX自動トレードシステム - ライブラリインストール手順

## 🎯 Phase 0: 環境構築 - ライブラリインストール

### 1. 基本インストール（必須）　（完了）

```bash
# 仮想環境を有効化
venv\Scripts\activate

# requirements.txt から一括インストール
pip install -r requirements.txt
```

### 2. 段階的インストール（推奨）

トラブル回避のため、用途別に段階的にインストールすることを推奨します。

#### ステップ1: 基本ライブラリ　（完了）
```bash
# データ処理・可視化
pip install pandas numpy matplotlib seaborn plotly mplfinance
```

#### ステップ2: 機械学習ライブラリ　（完了）
```bash
# 機械学習・最適化
pip install scikit-learn xgboost lightgbm optuna
pip install imbalanced-learn umap-learn scikit-optimize
```

#### ステップ3: 金融・テクニカル分析　（完了）
```bash
# テクニカル指標（TA-Libメイン）
pip install ta-lib-binary  # Windowsの場合
pip install ta             # 軽量代替ライブラリ

# pandas-taは現在Python 3.12+が必要なためスキップ
# pip install pandas-ta    # Python 3.11以下では使用不可

# バックテスト
pip install backtesting vectorbt
```

#### ステップ4: MT5接続（Windows のみ）
```bash
# MT5 API
pip install MetaTrader5
```

#### ステップ5: 強化学習（オプション）
```bash
# 強化学習関連
pip install stable-baselines3 gymnasium torch tensorboard
```

#### ステップ6: 開発環境
```bash
# Jupyter・開発ツール
pip install jupyter jupyterlab ipykernel
pip install pytest black flake8 mypy
```

### 3. OS別の注意事項

#### Windows ユーザー
- ✅ `ta-lib-binary` を使用（バイナリ版でインストール簡単）
- ✅ `MetaTrader5` が利用可能
- ✅ すべてのライブラリが利用可能

#### Mac/Linux ユーザー
```bash
# TA-Lib のインストール（事前準備が必要）
# Mac の場合
brew install ta-lib

# Ubuntu/Debian の場合
sudo apt-get install libta-lib-dev

# その後
pip install ta-lib
```
- ❌ `MetaTrader5` は利用不可（代替手段を検討）
- ✅ その他のライブラリは利用可能

### 4. インストール確認

以下のスクリプトで正常にインストールされているか確認：

```python
# test_installation.py
import sys

def check_installation():
    print("🔍 ライブラリインストール確認")
    print("=" * 50)
    
    # 必須ライブラリ
    essential_libs = [
        ('pandas', 'データ処理'),
        ('numpy', '数値計算'),
        ('matplotlib', 'グラフ描画'),
        ('sklearn', '機械学習'),
        ('xgboost', 'XGBoost'),
        ('talib', 'TA-Lib'), # pandas-taから変更
        ('backtesting', 'バックテスト'),
    ]
    
    # Windows専用ライブラリ
    windows_libs = [
        ('MetaTrader5', 'MT5接続'),
    ]
    
    # オプションライブラリ
    optional_libs = [
        ('stable_baselines3', '強化学習'),
        ('torch', 'PyTorch'),
    ]
    
    all_good = True
    
    print("\n📦 必須ライブラリ:")
    for lib, desc in essential_libs:
        try:
            __import__(lib)
            print(f"✅ {lib} ({desc})")
        except ImportError:
            print(f"❌ {lib} ({desc}) - インストールしてください")
            all_good = False
    
    print(f"\n🪟 Windows専用ライブラリ:")
    if sys.platform == "win32":
        for lib, desc in windows_libs:
            try:
                __import__(lib)
                print(f"✅ {lib} ({desc})")
            except ImportError:
                print(f"❌ {lib} ({desc}) - インストールしてください")
    else:
        print("ℹ️  非Windows環境のため、MT5関連ライブラリはスキップ")
    
    print(f"\n🎯 オプションライブラリ:")
    for lib, desc in optional_libs:
        try:
            __import__(lib)
            print(f"✅ {lib} ({desc})")
        except ImportError:
            print(f"⚠️  {lib} ({desc}) - オプション（後でインストール可能）")
    
    if all_good:
        print("\n🎉 必須ライブラリのインストール完了！")
        print("Phase 1（ルールベースシステム構築）に進めます。")
    else:
        print("\n⚠️  必須ライブラリに不足があります。上記の❌項目をインストールしてください。")

if __name__ == "__main__":
    check_installation()
```

### 5. トラブルシューティング

#### よくあるエラーと解決法

**1. TA-Lib インストールエラー（Windows）**
```bash
# エラーが出た場合
pip install ta-lib-binary

# または軽量代替
pip install ta

# pandas-taはPython 3.12+が必要なため現在は使用不可
```

**2. PyTorch CUDA対応（GPU使用時）**
```bash
# CUDA対応版をインストール
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**3. メモリ不足エラー**
```bash
# 一つずつインストール
pip install --no-cache-dir pandas
pip install --no-cache-dir numpy
# ... 続ける
```

**4. 権限エラー（Windows）**
```bash
# 管理者として実行するか、ユーザーディレクトリにインストール
pip install --user -r requirements.txt
```

### 6. 次のステップ

ライブラリインストール完了後：

1. ✅ `test_installation.py` を実行して確認
2. ✅ MT5接続テスト（Windowsの場合）
3. ✅ プロジェクト構造の作成
4. ✅ Phase 1: ルールベースシステム構築開始

---

**💡 Tips:**
- インストールは段階的に行う（エラー特定が容易）
- 仮想環境を必ず使用する
- 定期的に `pip list` でインストール状況を確認
- エラーが出たら、エラーメッセージをよく読んで対応