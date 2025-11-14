# FX自動トレードシステム開発ロードマップ

**作成日**: 2025年11月12日  
**目的**: 環境認識とシナリオ判断を行う階層型機械学習システムの構築

---

## 📋 プロジェクト概要

### システムアーキテクチャ
```
Layer 1: 環境認識モデル（分類問題）
    ↓ シナリオ判定（1_1, 1_2, 2_1, 2_2など）
Layer 2: 戦略実行モデル（最適化問題）
    ↓ エントリー/決済タイミング決定
自動取引実行
```

### 対象トレードシナリオ
- **1_1**: トレンド連続 - 高値ブレイク
- **1_2**: トレンド連続 - 押し目狙い
- **2_1**: レンジブレイク - 押し目＋サポートライン反発
- **2_2**: レンジブレイク - サポートラインブレイク
- **3_1**: トレンドラインブレイク - 押し目＋サポートライン反転
- **3_2**: チャネル内サポート
- **3_3**: レンジ内サポート

---

## 🎯 Phase 0: 環境構築

### 0.1 開発環境のセットアップ
```bash
# Pythonのバージョン確認（3.8以上推奨）
python --version

# 仮想環境の作成
python -m venv venv
venv\Scripts\activate

# 必要なライブラリのインストール
pip install pandas numpy matplotlib
pip install ta finta  # Windowsの場合（ta-lib-binaryは利用不可）
pip install scikit-learn lightgbm xgboost
pip install optuna
pip install backtesting
pip install MetaTrader5  # MT5を使用する場合
pip install "mplfinance>=0.12.7a0"  # チャート描画用
```

### 0.2 プロジェクト構造の作成
```
fx_トレード実現/
├── data/                      # データ保存用
│   ├── raw/                   # 生データ
│   ├── processed/             # 加工済みデータ
│   └── features/              # 特徴量データ
├── models/                    # 学習済みモデル
│   ├── layer1/                # 環境認識モデル
│   │   └── best_model.pkl
│   └── layer2/                # 戦略実行モデル（シナリオ別）
│       ├── optimal_params.json          # 全シナリオの最適パラメータ
│       ├── scenario_1_1_params.json     # シナリオ1_1専用
│       ├── scenario_1_2_params.json     # シナリオ1_2専用
│       ├── scenario_2_1_params.json     # シナリオ2_1専用
│       ├── scenario_2_2_params.json     # シナリオ2_2専用
│       ├── scenario_3_1_params.json     # シナリオ3_1専用
│       ├── scenario_3_2_params.json     # シナリオ3_2専用
│       ├── scenario_3_3_params.json     # シナリオ3_3専用
│       └── rl_agents/                   # 強化学習モデル（オプション）
│           ├── rl_agent_scenario_1_1.zip
│           ├── rl_agent_scenario_1_2.zip
│           ├── rl_agent_scenario_2_1.zip
│           ├── rl_agent_scenario_2_2.zip
│           ├── rl_agent_scenario_3_1.zip
│           ├── rl_agent_scenario_3_2.zip
│           └── rl_agent_scenario_3_3.zip
├── src/
│   ├── data_collection/       # データ取得
│   ├── feature_engineering/   # 特徴量作成
│   ├── indicators/            # テクニカル指標
│   ├── backtesting/           # バックテスト
│   ├── models/                # モデル定義
│   └── trading/               # 取引実行
├── notebooks/                 # Jupyter Notebook
├── tests/                     # テストコード
├── config/                    # 設定ファイル
└── logs/                      # ログ
```

### 0.3 データソースの確立
- [ ] MT5アカウントの準備（デモ口座でOK）
- [ ] ヒストリカルデータの取得方法確認
- [ ] M15, H1, H4, Dailyの複数時間軸データの取得

---

## 🔧 Phase 1: ルールベースシステムの構築

**目標**: AIなしで、記述されたトレードルールを完全にコード化し、バックテストできる状態にする

### 1.1 データ取得・前処理システム

#### タスク
- [ ] MT5からヒストリカルデータを取得するスクリプト作成
- [ ] OHLCV（始値、高値、安値、終値、出来高）データのDataFrame化
- [ ] 複数時間軸データの同期処理
- [ ] データのクリーニング（欠損値処理、異常値検出）

#### 成果物
```python
# src/data_collection/mt5_data_collector.py
class MT5DataCollector:
    def get_historical_data(symbol, timeframe, start_date, end_date)
    def sync_multi_timeframe_data(m15_data, h1_data, h4_data, daily_data)
```

### 1.2 テクニカル指標の実装

#### 1.2.1 基本指標（TA-Lib使用）
- [ ] EMA9の計算（TA-Lib: `talib.EMA()`）
- [ ] MACD（ゴールデンクロス/デッドクロス検出）
- [ ] フィボナッチリトレースメント自動計算
- [ ] サポート/レジスタンスライン検出

#### 1.2.2 高度な指標（手動実装 + TA-Lib）
- [ ] ダウ理論の実装
  - 高値・安値の検出（ZigZagアルゴリズム）
  - トレンド判定（上昇/下降/レンジ）
  - トレンド転換シグナル（1,2,3波検出）
  
- [ ] N波動の実装
  - 波の検出とラベリング
  - N波動の比率計算（1:1, 1:1.6, 1:2, 1:2.618）
  - ターゲット価格予測

- [ ] トレンドライン・チャネル検出
  - 自動トレンドライン描画
  - チャネル（平行線）の検出
  - トレンドラインブレイク判定

- [ ] レンジ検出
  - レンジ相場の自動判定
  - レンジの上限・下限特定
  - レンジ内サポート/レジスタンスライン

- [ ] FVG（Fair Value Gap）検出
  - 価格の飛び検出
  - ギャップゾーン描画

- [ ] OB（Order Block）検出
  - 強い需給エリアの特定

#### 成果物
```python
# src/indicators/technical_indicators.py（TA-Lib版）
import talib

def calculate_ema(close, period=9):
    return talib.EMA(close, timeperiod=period)

def detect_macd_cross(close):
    macd, signal, histogram = talib.MACD(close)
    return macd, signal, histogram

def calculate_rsi(close, period=14):
    return talib.RSI(close, timeperiod=period)

def calculate_fibonacci_levels(high, low):
    # 手動実装（TA-Libにはない）
    diff = high - low
    levels = {
        '0%': low,
        '23.6%': low + diff * 0.236,
        '38.2%': low + diff * 0.382,
        '50%': low + diff * 0.5,
        '61.8%': low + diff * 0.618,
        '100%': high
    }
    return levels

# src/indicators/advanced_indicators.py（手動実装）
def detect_dow_theory_trend(data):
    # ダウ理論の実装（pandas-ta代替）
    pass

def identify_n_wave_pattern(data):
    # N波動パターン検出
    pass

def detect_support_resistance(data):
    # サポート/レジスタンス自動検出
    pass
```

### 1.3 トレードロジックの実装

#### 各シナリオのルール実装
- [ ] シナリオ1_1: トレンド連続・高値ブレイク
  - ダウ理論でトレンド確認
  - 高値ブレイクの検出
  - N波動でターゲット設定
  - EMA9との位置関係確認

- [ ] シナリオ1_2: トレンド連続・押し目狙い
  - フィボナッチで押し目予測
  - ダウ理論でトレンド維持確認
  - N波動でエントリーポイント判定

- [ ] シナリオ2_1: レンジブレイク・押し目＋サポートライン反発
  - フィボナッチとMACDの組み合わせ
  - ゴールデンクロス確認

- [ ] シナリオ2_2: レンジブレイク・サポートラインブレイク
  - MACD単独判定

- [ ] シナリオ3_1: トレンドラインブレイク・押し目＋サポートライン反転
  - トレンドラインブレイク検出
  - ダウ理論でトレンド転換確認
  - EMA9でトレンド転換確認
  - MACDでモメンタム確認
  - サポートライン反転ポイント特定

- [ ] シナリオ3_2: チャネル内サポート
  - チャネルの検出と確認
  - チャネル下限でのサポート反発
  - フィボナッチでエントリーポイント精緻化
  - ダウ理論で内部トレンド確認

- [ ] シナリオ3_3: レンジ内サポート
  - レンジ相場の判定
  - レンジ下限サポートでの反発
  - フィボナッチでエントリータイミング
  - ダウ理論でレンジ内の小波動確認

#### エントリー/決済ロジック
- [ ] エントリー条件の完全実装
- [ ] 損切り（ストップロス）ロジック
- [ ] 利確（テイクプロフィット）ロジック
- [ ] トレーリングストップ（オプション）

#### 成果物
```python
# src/trading/strategies.py
class Strategy_1_1_TrendBreakout:
    def check_entry_conditions(data, indicators)
    def calculate_position_size(account_balance, risk_percentage)
    def set_stop_loss(entry_price, atr)
    def set_take_profit(entry_price, n_wave_target)

class Strategy_1_2_TrendPullback:
    # 同様の実装

class Strategy_2_1_RangeBreakPullback:
    # 同様の実装

class Strategy_2_2_RangeBreakSupport:
    # 同様の実装

class Strategy_3_1_TrendlineBreakReversal:
    def check_trendline_break(data, indicators)
    def check_dow_reversal(data, indicators)
    def check_ema9_reversal(data, indicators)
    def check_macd_confirmation(data, indicators)
    def check_entry_conditions(data, indicators)
    def set_stop_loss(entry_price, support_level)
    def set_take_profit(entry_price, target_level)

class Strategy_3_2_ChannelSupport:
    def identify_channel(data, indicators)
    def check_channel_support(data, indicators)
    def check_fibonacci_level(data, indicators)
    def check_dow_internal_trend(data, indicators)
    def check_entry_conditions(data, indicators)
    def set_stop_loss(entry_price, channel_lower)
    def set_take_profit(entry_price, channel_upper)

class Strategy_3_3_RangeSupport:
    def identify_range(data, indicators)
    def check_range_support(data, indicators)
    def check_fibonacci_timing(data, indicators)
    def check_dow_mini_waves(data, indicators)
    def check_entry_conditions(data, indicators)
    def set_stop_loss(entry_price, range_lower)
    def set_take_profit(entry_price, range_upper)
```

### 1.4 バックテストシステムの構築

- [ ] Backtesting.pyフレームワークの統合
- [ ] 各戦略のバックテスト実行
- [ ] パフォーマンス指標の計算
  - 総損益、勝率、プロフィットファクター
  - 最大ドローダウン、シャープレシオ
  - 取引回数、平均保有期間

- [ ] バックテスト結果の可視化
  - 損益曲線
  - ドローダウンチャート
  - 取引履歴レポート

#### 成果物
```python
# src/backtesting/backtest_engine.py
class BacktestEngine:
    def run_backtest(strategy, data, initial_capital)
    def calculate_metrics(trades)
    def generate_report(results)
    def plot_equity_curve(results)
```

### 1.5 ベースライン確立

- [ ] 各シナリオの個別バックテスト実行
- [ ] 統合システムのバックテスト（全シナリオ併用）
- [ ] 問題点の洗い出し
  - 勝率が低いシナリオの特定
  - ダマシが多い条件の分析
  - 過剰最適化の確認

#### 成果物
- バックテストレポート（Phase1_baseline_report.pdf）
- 改善すべき課題リスト
- 次フェーズへの推奨事項

---

## 🤖 Phase 2: Layer 1（環境認識AI）の開発

**目標**: 教師なしクラスタリングでデータから市場パターンを自動発見し、環境認識AIを構築

**重要な方針転換**: 静的なルールベースのラベリングではなく、**データ駆動型の教師なしクラスタリング**を採用します。これにより：
- ✅ 人間のバイアスを排除
- ✅ 見落としていたパターンを発見
- ✅ 市場の変化に柔軟に対応

### 2.1 教師なしクラスタリングによるパターン発見

#### 2.1.1 特徴量の選択（あなたの作業）

**あなたがやること**: 市場状況を表現する重要な指標を選択する

```python
# config/feature_selection.py
"""
あなたのトレード知識に基づいて重要な特徴量を選択
パターン定義は不要！AIが自動的に似た市場状況をグループ化
"""

FEATURE_GROUPS = {
    # トレンド系（あなたが重視する指標）
    'trend_features': [
        'ema9',
        'ema21', 
        'ema200',
        'ema9_slope',  # EMAの傾き（トレンドの強さ）
        'ema21_slope',
        'price_ema9_distance',  # 価格とEMAの乖離率
        'price_ema21_distance',
    ],
    
    # モメンタム系
    'momentum_features': [
        'macd',
        'macd_signal',
        'macd_histogram',
        'rsi',
        'rsi_slope',  # RSIの変化率
        'adx',  # トレンド強度
        'plus_di',  # 上昇圧力
        'minus_di',  # 下降圧力
    ],
    
    # ボラティリティ系
    'volatility_features': [
        'atr',
        'atr_normalized',  # ATR / 価格（正規化）
        'bollinger_band_width',
        'bollinger_position',  # バンド内での価格位置
        'price_volatility_20',  # 20期間の価格変動率
    ],
    
    # 価格アクション系
    'price_action_features': [
        'candle_body_ratio',  # 実体の割合
        'upper_shadow_ratio',  # 上ヒゲの割合
        'lower_shadow_ratio',  # 下ヒゲの割合
        'bullish_candles_5',  # 直近5本の陽線数
        'price_range_20',  # 20期間の高値-安値範囲
    ],
    
    # マルチタイムフレーム（あなたの手法の核心）
    'multi_timeframe_features': [
        'h1_ema9_slope',  # 1時間足のトレンド
        'h4_ema9_slope',  # 4時間足のトレンド
        'daily_ema9_slope',  # 日足のトレンド
        'h1_atr_normalized',
        'h4_atr_normalized',
        'daily_trend_alignment',  # 各時間足のトレンド一致度
    ],
    
    # あなたの手法固有の特徴量
    'custom_features': [
        'fvg_exists',  # FVG（Fair Value Gap）の存在
        'fvg_distance',  # 最も近いFVGまでの距離
        'ob_strength',  # Order Blockの強さ
        'ob_distance',  # 最も近いOBまでの距離
        'support_resistance_distance',  # サポレジまでの距離
        'fibonacci_level_proximity',  # フィボナッチレベルとの近さ
    ],
    
    # 出来高・市場構造
    'volume_features': [
        'volume',
        'volume_ma_ratio',  # 出来高移動平均との比率
        'volume_trend',  # 出来高のトレンド
    ],
}

# 実際に使用する特徴量を選択
SELECTED_FEATURES = (
    FEATURE_GROUPS['trend_features'] +
    FEATURE_GROUPS['momentum_features'] +
    FEATURE_GROUPS['volatility_features'] +
    FEATURE_GROUPS['multi_timeframe_features'] +
    FEATURE_GROUPS['custom_features']
)

print(f"選択された特徴量数: {len(SELECTED_FEATURES)}")
```

**作業チェックリスト**:
- [ ] あなたのトレード手法で重視している指標を確認
- [ ] 上記リストから不要なものを削除
- [ ] 追加したい指標があれば追加
- [ ] 合計30-50個程度の特徴量を選択

#### 2.1.2 クラスタリング実装（AI自動）

```python
# src/clustering/market_regime_detector.py
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

class MarketRegimeDetector:
    """
    教師なしクラスタリングで市場パターンを自動発見
    
    使い方:
    1. 特徴量を指定
    2. fit_clusters()でクラスタリング実行
    3. analyze_clusters()で結果確認
    4. あなたが各クラスタを評価
    """
    
    def __init__(self, n_clusters=7):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = None
        self.cluster_classifier = None
        self.feature_names = None
        self.cluster_centers = None
    
    def create_features(self, data, feature_list):
        """
        指定された特徴量を抽出
        
        Args:
            data: OHLCVデータ
            feature_list: 使用する特徴量のリスト
        
        Returns:
            特徴量DataFrame
        """
        features = pd.DataFrame(index=data.index)
        
        for feature_name in feature_list:
            if feature_name in data.columns:
                features[feature_name] = data[feature_name]
            else:
                print(f"警告: {feature_name} がデータに存在しません")
        
        return features.fillna(method='ffill').fillna(0)
    
    def fit_clusters(self, data, feature_list):
        """
        クラスタリング実行
        
        Args:
            data: 履歴データ
            feature_list: 使用する特徴量リスト
        
        Returns:
            各データポイントのクラスタID
        """
        print(f"クラスタリング開始: {len(feature_list)}個の特徴量を使用")
        
        # 特徴量作成
        features = self.create_features(data, feature_list)
        self.feature_names = features.columns.tolist()
        
        # 欠損値確認
        if features.isnull().sum().sum() > 0:
            print("警告: 欠損値が存在します。0で埋めます。")
            features = features.fillna(0)
        
        # 標準化
        features_scaled = self.scaler.fit_transform(features)
        
        # K-Meansクラスタリング
        print(f"{self.n_clusters}個のクラスタに分類中...")
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,
            n_init=10,
            max_iter=300
        )
        clusters = self.kmeans.fit_predict(features_scaled)
        
        # クラスタ中心を保存
        self.cluster_centers = self.kmeans.cluster_centers_
        
        # シルエットスコアで品質評価
        silhouette = silhouette_score(features_scaled, clusters)
        print(f"シルエットスコア: {silhouette:.3f}")
        print(f"  0.7以上: 優秀")
        print(f"  0.5-0.7: 良好")
        print(f"  0.25-0.5: 普通")
        print(f"  0.25未満: 改善が必要")
        
        # XGBoost分類器を訓練（新しいデータでクラスタ予測用）
        print("クラスタ分類器を訓練中...")
        self.cluster_classifier = xgb.XGBClassifier(
            objective='multi:softmax',
            num_class=self.n_clusters,
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.cluster_classifier.fit(features, clusters)
        
        print(f"✓ クラスタリング完了")
        return clusters
    
    def predict_cluster(self, data, feature_list):
        """
        新しいデータのクラスタを予測
        """
        features = self.create_features(data, feature_list)
        return self.cluster_classifier.predict(features)
    
    def analyze_clusters(self, data, clusters):
        """
        各クラスタの特性を分析
        
        Returns:
            クラスタ分析結果の辞書
        """
        print("\n" + "="*60)
        print("クラスタ分析結果")
        print("="*60)
        
        cluster_analysis = {}
        
        for i in range(self.n_clusters):
            cluster_mask = clusters == i
            cluster_data = data[cluster_mask]
            
            if len(cluster_data) == 0:
                continue
            
            # 基本統計
            analysis = {
                'cluster_id': i,
                'size': len(cluster_data),
                'percentage': len(cluster_data) / len(data) * 100,
                'avg_volatility': cluster_data['atr'].mean() if 'atr' in cluster_data else 0,
                'avg_trend_strength': cluster_data['adx'].mean() if 'adx' in cluster_data else 0,
                'avg_return': cluster_data['close'].pct_change().mean(),
                'volatility_regime': self._classify_volatility(cluster_data),
                'trend_regime': self._classify_trend(cluster_data),
                'characteristics': self._describe_cluster(cluster_data)
            }
            
            cluster_analysis[i] = analysis
            
            # コンソール出力
            print(f"\n【クラスタ {i}】")
            print(f"  出現回数: {analysis['size']:,} ({analysis['percentage']:.1f}%)")
            print(f"  特徴: {analysis['characteristics']}")
            print(f"  トレンド: {analysis['trend_regime']}")
            print(f"  ボラティリティ: {analysis['volatility_regime']}")
            print(f"  平均リターン: {analysis['avg_return']:.4%}")
            print(f"  平均ADX: {analysis['avg_trend_strength']:.2f}")
        
        return cluster_analysis
    
    def _classify_volatility(self, data):
        """ボラティリティレジーム分類"""
        if 'atr_normalized' not in data.columns:
            return "不明"
        
        avg_atr = data['atr_normalized'].mean()
        if avg_atr > 0.015:
            return "超高ボラティリティ"
        elif avg_atr > 0.010:
            return "高ボラティリティ"
        elif avg_atr > 0.005:
            return "中ボラティリティ"
        else:
            return "低ボラティリティ"
    
    def _classify_trend(self, data):
        """トレンドレジーム分類"""
        if 'ema9_slope' not in data.columns:
            return "不明"
        
        avg_slope = data['ema9_slope'].mean()
        slope_std = data['ema9_slope'].std()
        
        if abs(avg_slope) < slope_std * 0.5:
            return "レンジ・横ばい"
        elif avg_slope > 0:
            if avg_slope > slope_std:
                return "強い上昇トレンド"
            else:
                return "弱い上昇トレンド"
        else:
            if abs(avg_slope) > slope_std:
                return "強い下降トレンド"
            else:
                return "弱い下降トレンド"
    
    def _describe_cluster(self, data):
        """クラスタの特徴を文字列で説明"""
        trend = self._classify_trend(data)
        volatility = self._classify_volatility(data)
        return f"{trend}, {volatility}"
    
    def save(self, filepath):
        """モデル保存"""
        import joblib
        joblib.dump({
            'scaler': self.scaler,
            'kmeans': self.kmeans,
            'classifier': self.cluster_classifier,
            'feature_names': self.feature_names,
            'n_clusters': self.n_clusters
        }, filepath)
        print(f"✓ モデルを保存: {filepath}")
    
    def load(self, filepath):
        """モデル読み込み"""
        import joblib
        saved = joblib.load(filepath)
        self.scaler = saved['scaler']
        self.kmeans = saved['kmeans']
        self.cluster_classifier = saved['classifier']
        self.feature_names = saved['feature_names']
        self.n_clusters = saved['n_clusters']
        print(f"✓ モデルを読み込み: {filepath}")
```

**実行方法**:
```python
# クラスタリング実行
detector = MarketRegimeDetector(n_clusters=7)
clusters = detector.fit_clusters(historical_data, SELECTED_FEATURES)

# 結果分析
analysis = detector.analyze_clusters(historical_data, clusters)

# モデル保存
detector.save('models/layer1/market_regime_detector.pkl')
```

**作業チェックリスト**:
- [ ] コードを実行
- [ ] シルエットスコアを確認（0.5以上が目標）
- [ ] 各クラスタの出現回数を確認
- [ ] 分析結果を次のステップで使用

#### 2.1.3 クラスタ数の最適化（AIによる自動評価）

```python
# src/clustering/cluster_optimization.py
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, calinski_harabasz_score

def find_optimal_clusters(data, feature_list, min_clusters=5, max_clusters=12):
    """
    最適なクラスタ数を自動的に探索
    
    Args:
        data: 履歴データ
        feature_list: 特徴量リスト
        min_clusters: 最小クラスタ数
        max_clusters: 最大クラスタ数
    
    Returns:
        各クラスタ数の評価指標
    """
    results = []
    
    for n in range(min_clusters, max_clusters + 1):
        print(f"\nクラスタ数 {n} をテスト中...")
        
        detector = MarketRegimeDetector(n_clusters=n)
        clusters = detector.fit_clusters(data, feature_list)
        
        # 標準化された特徴量
        features = detector.create_features(data, feature_list)
        features_scaled = detector.scaler.transform(features)
        
        # 評価指標計算
        silhouette = silhouette_score(features_scaled, clusters)
        calinski = calinski_harabasz_score(features_scaled, clusters)
        inertia = detector.kmeans.inertia_  # クラスタ内分散
        
        # クラスタサイズのバランスを評価
        cluster_sizes = [np.sum(clusters == i) for i in range(n)]
        size_balance = np.std(cluster_sizes) / np.mean(cluster_sizes)  # 小さいほど良い
        
        results.append({
            'n_clusters': n,
            'silhouette_score': silhouette,
            'calinski_harabasz_score': calinski,
            'inertia': inertia,
            'size_balance': size_balance,
            'min_cluster_size': min(cluster_sizes),
            'max_cluster_size': max(cluster_sizes)
        })
        
        print(f"  シルエットスコア: {silhouette:.3f}")
        print(f"  Calinski-Harabasz スコア: {calinski:.1f}")
        print(f"  クラスタサイズバランス: {size_balance:.3f}")
    
    # 結果を可視化
    plot_cluster_metrics(results)
    
    # 推奨クラスタ数
    best_n = recommend_cluster_number(results)
    print(f"\n推奨クラスタ数: {best_n}")
    
    return results

def plot_cluster_metrics(results):
    """クラスタ評価指標のグラフ表示"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    n_clusters = [r['n_clusters'] for r in results]
    
    # シルエットスコア
    axes[0, 0].plot(n_clusters, [r['silhouette_score'] for r in results], 'o-')
    axes[0, 0].set_xlabel('クラスタ数')
    axes[0, 0].set_ylabel('シルエットスコア')
    axes[0, 0].set_title('シルエットスコア（高いほど良い）')
    axes[0, 0].axhline(y=0.5, color='r', linestyle='--', label='目標値')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Calinski-Harabasz スコア
    axes[0, 1].plot(n_clusters, [r['calinski_harabasz_score'] for r in results], 'o-')
    axes[0, 1].set_xlabel('クラスタ数')
    axes[0, 1].set_ylabel('Calinski-Harabasz スコア')
    axes[0, 1].set_title('Calinski-Harabasz スコア（高いほど良い）')
    axes[0, 1].grid(True)
    
    # イナーシャ（エルボー法）
    axes[1, 0].plot(n_clusters, [r['inertia'] for r in results], 'o-')
    axes[1, 0].set_xlabel('クラスタ数')
    axes[1, 0].set_ylabel('イナーシャ')
    axes[1, 0].set_title('エルボー法（急激に減少が止まる点が最適）')
    axes[1, 0].grid(True)
    
    # クラスタサイズバランス
    axes[1, 1].plot(n_clusters, [r['size_balance'] for r in results], 'o-')
    axes[1, 1].set_xlabel('クラスタ数')
    axes[1, 1].set_ylabel('サイズバランス（標準偏差/平均）')
    axes[1, 1].set_title('クラスタサイズのバランス（低いほど良い）')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig('outputs/cluster_optimization.png')
    print("✓ グラフを保存: outputs/cluster_optimization.png")

def recommend_cluster_number(results):
    """
    複数の指標を総合して最適なクラスタ数を推奨
    """
    # 各指標を正規化してスコア化
    scores = []
    
    for r in results:
        score = 0
        
        # シルエットスコア（重視：40%）
        score += r['silhouette_score'] * 0.4
        
        # サイズバランス（重視：30%、逆数）
        score += (1 / (1 + r['size_balance'])) * 0.3
        
        # Calinski-Harabasz スコア（正規化して20%）
        max_calinski = max([res['calinski_harabasz_score'] for res in results])
        score += (r['calinski_harabasz_score'] / max_calinski) * 0.2
        
        # 最小クラスタサイズペナルティ（10%）
        if r['min_cluster_size'] < 100:  # 100データポイント未満は減点
            score += 0
        else:
            score += 0.1
        
        scores.append(score)
    
    best_idx = np.argmax(scores)
    return results[best_idx]['n_clusters']
```

**実行方法**:
```python
# 最適クラスタ数を自動探索
results = find_optimal_clusters(historical_data, SELECTED_FEATURES, min_clusters=5, max_clusters=12)

# 推奨された数でクラスタリング
best_n = recommend_cluster_number(results)
detector = MarketRegimeDetector(n_clusters=best_n)
clusters = detector.fit_clusters(historical_data, SELECTED_FEATURES)
```

**作業チェックリスト**:
- [ ] クラスタ数5-12で自動評価を実行
- [ ] グラフを確認（outputs/cluster_optimization.png）
- [ ] 推奨されたクラスタ数を確認
- [ ] 必要に応じて手動で調整

#### 2.1.4 クラスタ検証とラベリング（あなたの作業）

AIがクラスタリングした結果を検証し、各クラスタに意味のある名前を付けます。

```python
# src/clustering/cluster_validation.py
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy

def validate_clusters_with_backtest(data, clusters, detector):
    """
    各クラスタの実トレード性能を検証
    
    各クラスタで発生したトレードのパフォーマンスを確認し、
    有効なクラスタかどうかを判定
    """
    print("\n" + "="*60)
    print("クラスタ別バックテスト検証")
    print("="*60)
    
    validation_results = {}
    
    for cluster_id in range(detector.n_clusters):
        cluster_mask = clusters == cluster_id
        cluster_data = data[cluster_mask]
        
        if len(cluster_data) < 100:
            print(f"\nクラスタ {cluster_id}: データ不足（{len(cluster_data)}件）- スキップ")
            continue
        
        print(f"\n【クラスタ {cluster_id}】")
        print(f"データ数: {len(cluster_data):,}")
        
        # Phase 1のルールベース戦略でバックテスト
        bt = Backtest(cluster_data, Phase1Strategy, cash=10000, commission=.002)
        stats = bt.run()
        
        # 重要指標を抽出
        validation_results[cluster_id] = {
            'total_trades': stats['# Trades'],
            'win_rate': stats['Win Rate [%]'],
            'profit_factor': stats.get('Profit Factor', 0),
            'sharpe_ratio': stats['Sharpe Ratio'],
            'max_drawdown': stats['Max. Drawdown [%]'],
            'total_return': stats['Return [%]'],
            'avg_trade': stats['Avg. Trade [%]'],
            'is_profitable': stats['Return [%]'] > 0,
            'is_tradeable': stats['# Trades'] > 10  # 最低トレード数
        }
        
        # 結果表示
        print(f"  総トレード数: {stats['# Trades']}")
        print(f"  勝率: {stats['Win Rate [%]']:.1f}%")
        print(f"  シャープレシオ: {stats['Sharpe Ratio']:.2f}")
        print(f"  最大ドローダウン: {stats['Max. Drawdown [%]']:.1f}%")
        print(f"  総リターン: {stats['Return [%]']:.1f}%")
        
        # 判定
        if validation_results[cluster_id]['is_profitable'] and validation_results[cluster_id]['is_tradeable']:
            print(f"  ✓ トレード可能なクラスタ")
        else:
            print(f"  ✗ トレード非推奨")
    
    return validation_results

def analyze_cluster_characteristics(data, clusters, detector):
    """
    各クラスタの市場特性を詳細分析
    
    あなたがラベル付けするための情報を提供
    """
    print("\n" + "="*60)
    print("クラスタ特性の詳細分析")
    print("="*60)
    
    for cluster_id in range(detector.n_clusters):
        cluster_mask = clusters == cluster_id
        cluster_data = data[cluster_mask]
        
        if len(cluster_data) == 0:
            continue
        
        print(f"\n{'='*60}")
        print(f"【クラスタ {cluster_id}】")
        print(f"{'='*60}")
        
        # 1. トレンド分析
        print("\n■ トレンド特性:")
        if 'ema9_slope' in cluster_data.columns:
            avg_slope = cluster_data['ema9_slope'].mean()
            slope_direction = "上昇" if avg_slope > 0 else "下降"
            slope_strength = "強い" if abs(avg_slope) > cluster_data['ema9_slope'].std() else "弱い"
            print(f"  EMA9傾き: {slope_direction} {slope_strength} ({avg_slope:.6f})")
        
        if 'adx' in cluster_data.columns:
            avg_adx = cluster_data['adx'].mean()
            trend_strength = "強トレンド" if avg_adx > 25 else "レンジ" if avg_adx < 15 else "中程度"
            print(f"  ADX: {avg_adx:.1f} ({trend_strength})")
        
        # 2. ボラティリティ分析
        print("\n■ ボラティリティ:")
        if 'atr_normalized' in cluster_data.columns:
            avg_atr = cluster_data['atr_normalized'].mean()
            vol_level = "超高" if avg_atr > 0.015 else "高" if avg_atr > 0.010 else "中" if avg_atr > 0.005 else "低"
            print(f"  ATR正規化: {avg_atr:.4f} ({vol_level})")
        
        # 3. モメンタム分析
        print("\n■ モメンタム:")
        if 'rsi' in cluster_data.columns:
            avg_rsi = cluster_data['rsi'].mean()
            rsi_state = "買われ過ぎ" if avg_rsi > 70 else "売られ過ぎ" if avg_rsi < 30 else "中立"
            print(f"  RSI: {avg_rsi:.1f} ({rsi_state})")
        
        if 'macd_histogram' in cluster_data.columns:
            avg_macd_hist = cluster_data['macd_histogram'].mean()
            macd_state = "強気" if avg_macd_hist > 0 else "弱気"
            print(f"  MACDヒストグラム: {avg_macd_hist:.4f} ({macd_state})")
        
        # 4. マルチタイムフレーム分析
        print("\n■ マルチタイムフレーム:")
        for tf in ['h1', 'h4', 'daily']:
            col = f'{tf}_ema9_slope'
            if col in cluster_data.columns:
                avg = cluster_data[col].mean()
                direction = "↑上昇" if avg > 0 else "↓下降"
                print(f"  {tf.upper()}: {direction} ({avg:.6f})")
        
        # 5. 価格アクション分析
        print("\n■ 価格アクション:")
        if 'candle_body_ratio' in cluster_data.columns:
            avg_body = cluster_data['candle_body_ratio'].mean()
            print(f"  実体比率: {avg_body:.2f} ({'大きい実体' if avg_body > 0.6 else '小さい実体'})")
        
        # 6. 出現タイミング
        print("\n■ 出現パターン:")
        print(f"  出現回数: {len(cluster_data):,}")
        print(f"  全体に占める割合: {len(cluster_data) / len(data) * 100:.1f}%")
        
        # 時系列での分布
        cluster_data_with_dates = cluster_data.copy()
        if 'date' in cluster_data_with_dates.columns:
            monthly_counts = cluster_data_with_dates.groupby(cluster_data_with_dates['date'].dt.to_period('M')).size()
            print(f"  月間平均出現: {monthly_counts.mean():.0f}回")
        
        print("\n" + "-"*60)
        print("あなたの作業: 上記の特性から、このクラスタに名前を付けてください")
        print("例: '強い上昇トレンド・高ボラ', 'レンジ相場・低ボラ', '反転局面' など")

def create_cluster_labels(detector):
    """
    あなたがクラスタに名前を付けるためのテンプレート
    """
    cluster_labels = {}
    
    print("\n" + "="*60)
    print("クラスタラベリング")
    print("="*60)
    
    for i in range(detector.n_clusters):
        print(f"\nクラスタ {i} の名前を入力してください:")
        print("（上記の分析結果を参考に、わかりやすい名前を付けてください）")
        label = input(f"クラスタ {i}: ")
        cluster_labels[i] = label if label else f"クラスタ_{i}"
    
    # 保存
    import json
    with open('config/cluster_labels.json', 'w', encoding='utf-8') as f:
        json.dump(cluster_labels, f, ensure_ascii=False, indent=2)
    
    print("\n✓ クラスタラベルを保存しました")
    return cluster_labels
```

**作業フロー**:
```python
# 1. クラスタをバックテストで検証
validation_results = validate_clusters_with_backtest(
    historical_data, 
    clusters, 
    detector
)

# 2. 各クラスタの特性を詳細分析
analyze_cluster_characteristics(historical_data, clusters, detector)

# 3. あなたがラベルを付ける
cluster_labels = create_cluster_labels(detector)

# 4. トレード不可能なクラスタを除外
tradeable_clusters = [
    cid for cid, result in validation_results.items()
    if result['is_profitable'] and result['is_tradeable']
]

print(f"\nトレード可能なクラスタ: {tradeable_clusters}")
```

**作業チェックリスト**:
- [ ] 各クラスタのバックテスト結果を確認
- [ ] 各クラスタの特性分析を読む
- [ ] 各クラスタに意味のある名前を付ける
- [ ] トレード不可能なクラスタを特定
- [ ] ラベルをconfig/cluster_labels.jsonに保存

**例：ラベリング結果**:
```json
{
  "0": "強い上昇トレンド・高ボラティリティ",
  "1": "弱い上昇トレンド・低ボラティリティ",
  "2": "レンジ相場・中ボラティリティ",
  "3": "下降トレンド・高ボラティリティ",
  "4": "トレンド転換局面",
  "5": "調整局面・押し目候補",
  "6": "待機推奨・不明瞭"
}
```

---

### 2.2 教師データの作成（従来型 - 参考用）

**注意**: このセクションは従来の静的ルールベースアプローチです。教師なしクラスタリングを使う場合は不要ですが、参考として残しています。

#### 2.1.1 ラベリング戦略
- [ ] Phase 1のバックテスト結果から勝ちトレードを抽出
- [ ] 各勝ちトレードが発生した時点の相場状況を記録
- [ ] シナリオごとにラベル付け
  - Class 0: ノーエントリー（待機）
  - Class 1: シナリオ1_1（トレンド連続・高値ブレイク）
  - Class 2: シナリオ1_2（トレンド連続・押し目）
  - Class 3: シナリオ2_1（レンジブレイク・押し目＋サポート反発）
  - Class 4: シナリオ2_2（レンジブレイク・サポートブレイク）
  - Class 5: シナリオ3_1（トレンドラインブレイク・反転）
  - Class 6: シナリオ3_2（チャネル内サポート）
  - Class 7: シナリオ3_3（レンジ内サポート）

#### 2.1.2 ラベリング基準の明確化
```python
# 例: シナリオ1_1のラベリング基準
def label_scenario_1_1(data, index):
    """
    以下の条件をすべて満たす場合に1を返す：
    1. ダウ理論でアップトレンド確認
    2. 直近高値をブレイク
    3. N波動のターゲットに到達
    4. EMA9より上
    5. 実際に利益が出た
    """
```

- [ ] 各シナリオのラベリング関数作成
- [ ] 自動ラベリングスクリプト実行
- [ ] 手動検証とラベル補正

### 2.2 特徴量エンジニアリング

#### 2.2.1 基本特徴量
- [ ] 価格系: 現在価格、高値、安値、終値
- [ ] トレンド系: EMA9, EMA21, EMA200との乖離率
- [ ] モメンタム系: RSI, MACD, ADX
- [ ] ボラティリティ系: ATR, ボリンジャーバンド幅

#### 2.2.2 高度な特徴量（最重要）
- [ ] ダウ理論特徴量
  - トレンド方向（1: 上昇, 0: レンジ, -1: 下降）
  - 高値切り上げ連続回数
  - 安値切り上げ連続回数
  - 最後のトレンド転換からの経過バー数

- [ ] N波動特徴量
  - 現在の波の段階（1波, 2波, 3波）
  - 前波に対する現在波の比率
  - 理想的なN波動比率との乖離度
  - ターゲット価格までの距離（pips）

- [ ] フィボナッチ特徴量
  - 各レベル（23.6%, 38.2%, 50%, 61.8%）までの距離
  - 最も近いフィボナッチレベル
  - フィボナッチゾーン内かどうか（バイナリ）

- [ ] マルチタイムフレーム特徴量
  - H1のトレンド方向
  - H4のトレンド方向
  - Dailyのトレンド方向
  - 上位足の主要サポート/レジスタンスまでの距離

- [ ] FVG/OB特徴量
  - 直近のFVGまでの距離
  - FVGゾーン内かどうか
  - 直近のOBまでの距離
  - OBの強度（出来高ベース）

- [ ] トレンドライン・チャネル特徴量
  - トレンドラインの角度
  - トレンドラインまでの距離
  - トレンドラインブレイク判定
  - チャネル幅
  - チャネル内の位置（上部/中部/下部）

- [ ] レンジ特徴量
  - レンジ判定フラグ
  - レンジ幅
  - レンジ内の位置
  - レンジ継続期間

#### 成果物
```python
# src/feature_engineering/feature_creator.py
class FeatureCreator:
    def create_basic_features(data)
    def create_dow_theory_features(data)
    def create_n_wave_features(data)
    def create_fibonacci_features(data)
    def create_multi_timeframe_features(m15, h1, h4, daily)
    def create_fvg_ob_features(data)
    def create_trendline_channel_features(data)
    def create_range_features(data)
    def create_all_features(data)  # 統合
```

### 2.3 モデルの学習と評価

#### 2.3.1 データ分割
- [ ] 時系列を考慮した分割（TimeSeriesSplit）
- [ ] 訓練データ: 70%
- [ ] 検証データ: 15%
- [ ] テストデータ: 15%

#### 2.3.2 モデル選定と学習
- [ ] XGBoostの実装（メインモデル）
  ```python
  import xgboost as xgb
  
  model = xgb.XGBClassifier(
      objective='multi:softmax',
      num_class=8,  # シナリオ数（0: 待機 + 7シナリオ）
      n_estimators=500,
      learning_rate=0.05,
      max_depth=7,
      subsample=0.8,
      colsample_bytree=0.8,
      tree_method='hist',  # 高速化
      eval_metric='mlogloss'
  )
  ```

- [ ] ベースラインモデルの実装（比較用）
  - ランダムフォレスト（精度比較）
  - ロジスティック回帰（シンプルなベースライン）

#### 2.3.3 ハイパーパラメータチューニング
- [ ] Optunaによる自動最適化
  ```python
  def objective(trial):
      params = {
          'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
          'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
          'max_depth': trial.suggest_int('max_depth', 3, 10),
          'num_leaves': trial.suggest_int('num_leaves', 20, 100)
      }
      # モデル学習と評価
      return accuracy
  ```

#### 2.3.4 モデル評価
- [ ] 精度（Accuracy）
- [ ] 各クラスの適合率・再現率・F1スコア
- [ ] 混同行列（Confusion Matrix）
- [ ] 特徴量重要度の分析

#### 成果物
```python
# src/models/layer1_environment_classifier.py
class EnvironmentClassifier:
    def __init__(self, model_type='xgboost')
    def train(X_train, y_train, X_val, y_val)
    def predict(X)
    def predict_proba(X)  # 確率出力
    def save_model(path)
    def load_model(path)
```

### 2.4 統合とバックテスト

- [ ] Layer 1モデルをトレードシステムに統合
- [ ] フィルタリングロジックの実装
  ```python
  # 例: 予測確率が60%以上の時だけエントリー許可
  if predicted_proba > 0.6:
      execute_scenario(predicted_scenario)
  ```

- [ ] 統合システムのバックテスト実行
- [ ] Phase 1（ルールベース）との比較
  - 勝率の向上
  - ダマシトレードの減少
  - 総損益の改善

#### 成果物
- Layer1統合バックテストレポート（Phase2_layer1_report.pdf）
- モデル性能分析レポート
- 特徴量重要度レポート

---

## ⚙️ Phase 3: Layer 2（戦略実行最適化）の開発

**目標**: 各クラスタにおけるエントリー/決済判断を強化学習で動的最適化

**採用アプローチ**: **クラスタ別強化学習モデル** - Phase 2で発見した各クラスタ（市場パターン）ごとに独立した強化学習エージェントを訓練し、リアルタイムで最適な取引判断を行います。

**重要な変更点**: 
- ❌ 従来: 手動定義した7シナリオごとにRL
- ✅ 新方式: AIが発見したクラスタごとにRL

**メリット**:
- データから自動的に最適な市場分類を発見
- 人間の定義に縛られない柔軟なトレード
- 新しい市場パターンにも対応可能

### 3.1 クラスタ別強化学習の設計

#### 3.1.1 アクション空間の定義（全クラスタ共通）

```python
# src/rl/action_space.py
"""
全クラスタで共通のアクション空間
（必要に応じてクラスタごとにカスタマイズ可能）
"""

ACTION_SPACE = {
    0: 'HOLD',           # 何もしない（待機）
    1: 'BUY_SMALL',      # 小ロットでエントリー (0.01 lot)
    2: 'BUY_MEDIUM',     # 中ロットでエントリー (0.03 lot)
    3: 'BUY_LARGE',      # 大ロットでエントリー (0.05 lot)
    4: 'CLOSE_HALF',     # ポジションの半分を決済
    5: 'CLOSE_ALL',      # 全ポジション決済
    6: 'TRAILING_STOP',  # トレーリングストップ有効化
}

# クラスタごとのアクションカスタマイズ例
CLUSTER_ACTION_CUSTOMIZATION = {
    # 例: "強い上昇トレンド・高ボラ"クラスタ
    0: {
        'allowed_actions': [0, 1, 2, 3, 5, 6],  # 全アクション許可
        'lot_sizes': {'small': 0.01, 'medium': 0.03, 'large': 0.05},
        'trailing_stop_distance': 50  # pips
    },
    
    # 例: "レンジ相場・低ボラ"クラスタ
    2: {
        'allowed_actions': [0, 1, 4, 5],  # 慎重な行動のみ
        'lot_sizes': {'small': 0.01, 'medium': 0.02, 'large': 0.03},
        'trailing_stop_distance': 30
    },
    
    # 例: "待機推奨"クラスタ
    6: {
        'allowed_actions': [0, 5],  # 待機 or 既存ポジション決済のみ
        'lot_sizes': {'small': 0, 'medium': 0, 'large': 0},
        'trailing_stop_distance': 0
    }
}
```
```

**シナリオ別の拡張アクション**
- シナリオ1_1（ブレイクアウト）: ブレイク確認後の追加エントリー
- シナリオ1_2（押し目）: 複数フィボナッチレベルでの分割エントリー
- シナリオ3_2（チャネル）: チャネル上限接近時の部分利確

#### 3.1.2 観測空間の設計

**各シナリオで観測する特徴量**
```python
# シナリオごとに関連する特徴量のみを観測
observation_features = {
    'price_features': [
        'current_price',
        'high', 'low', 'close',
        'price_change_pct'
    ],
    'technical_indicators': [
        'ema9', 'ema21', 'ema200',
        'macd', 'macd_signal', 'macd_hist',
        'rsi', 'atr', 'adx'
    ],
    'scenario_specific': [
        # シナリオ1_1の場合
        'breakout_strength',
        'n_wave_ratio',
        'ema9_distance',
        # シナリオ3_2の場合
        'channel_position',  # チャネル内の位置
        'channel_width',
        'support_distance'
    ],
    'position_info': [
        'has_position',
        'position_size',
        'unrealized_pnl',
        'holding_bars'
    ]
}
```

#### 3.1.3 報酬関数の設計（最重要）

**基本報酬構造**
```python
def calculate_reward(action, state, next_state):
    """
    シナリオに応じた報酬計算
    """
    reward = 0
    
    # 1. 利益報酬（最重要）
    pnl = next_state['unrealized_pnl'] - state['unrealized_pnl']
    reward += pnl * 10  # 利益を強く評価
    
    # 2. リスク管理報酬
    if action in ['CLOSE_HALF', 'CLOSE_ALL']:
        if pnl > 0:
            reward += 5  # 利確を評価
        elif pnl < -state['max_loss']:
            reward += 3  # 適切な損切りを評価
    
    # 3. 取引効率報酬
    if action == 'HOLD' and not state['has_position']:
        if state['scenario_probability'] < 0.6:
            reward += 1  # 低確率時の待機を評価
    
    # 4. ドローダウンペナルティ
    if state['drawdown'] > 0.1:  # 10%以上のドローダウン
        reward -= 10
    
    # 5. シナリオ固有の報酬
    # 例: シナリオ1_1の場合
    if scenario == '1_1':
        if action in ['BUY_MEDIUM', 'BUY_LARGE']:
            if state['breakout_confirmed']:
                reward += 3  # ブレイク確認後のエントリーを評価
    
    # 例: シナリオ3_2の場合
    if scenario == '3_2':
        if action == 'CLOSE_HALF':
            if state['channel_position'] > 0.8:  # チャネル上限付近
                reward += 4  # 上限での部分利確を評価
    
    return reward
```

**シナリオ別報酬の調整ポイント（参考）**
- [ ] シナリオ1_1: ブレイクアウトの勢いを評価
- [ ] シナリオ1_2: フィボナッチレベルでの反発を評価
- [ ] シナリオ2_1: MACDクロスタイミングを評価
- [ ] シナリオ2_2: ブレイク後の継続性を評価
- [ ] シナリオ3_1: トレンド転換の確実性を評価
- [ ] シナリオ3_2: チャネル内の位置取りを評価
- [ ] シナリオ3_3: レンジ境界での反発を評価

---

### 3.2 【参考】シナリオ別環境実装（従来型）

以下は従来のシナリオベースのアプローチです。クラスタリング方式では不要ですが、参考として残しています。

### 3.2 【参考】シナリオ別環境実装（従来型）

#### 3.2.1 Gym環境の実装

**シナリオ1_1専用環境**
```python
import gym
import numpy as np
from gym import spaces

class TradingEnvironment_Scenario_1_1(gym.Env):
    """
    シナリオ1_1: トレンド連続・高値ブレイク専用の取引環境
    """
    def __init__(self, data, initial_balance=100000):
        super().__init__()
        
        self.data = data
        self.initial_balance = initial_balance
        self.current_step = 0
        
        # アクション空間: 0=Hold, 1=Buy_Small, 2=Buy_Medium, 3=Buy_Large, 
        #                 4=Close_Half, 5=Close_All, 6=Trailing_Stop
        self.action_space = spaces.Discrete(7)
        
        # 観測空間: シナリオ1_1に関連する特徴量
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, 
            shape=(25,),  # 特徴量の数
            dtype=np.float32
        )
        
        self.reset()
    
    def reset(self):
        """環境のリセット"""
        self.current_step = 100  # 十分な履歴を確保
        self.balance = self.initial_balance
        self.position = None
        self.total_trades = 0
        self.winning_trades = 0
        
        return self._get_observation()
    
    def _get_observation(self):
        """現在の観測を取得"""
        current_data = self.data.iloc[self.current_step]
        
        obs = np.array([
            # 価格情報
            current_data['close'],
            current_data['high'],
            current_data['low'],
            current_data['volume'],
            
            # テクニカル指標
            current_data['ema9'],
            current_data['ema21'],
            current_data['ema200'],
            current_data['macd'],
            current_data['macd_signal'],
            current_data['rsi'],
            current_data['atr'],
            current_data['adx'],
            
            # シナリオ1_1固有の特徴量
            current_data['breakout_strength'],  # ブレイクの強さ
            current_data['n_wave_ratio'],       # N波動比率
            current_data['ema9_distance'],      # EMA9との距離
            current_data['higher_high_count'],  # 高値更新回数
            current_data['dow_trend'],          # ダウ理論トレンド
            
            # ポジション情報
            1.0 if self.position else 0.0,
            self.position['size'] if self.position else 0.0,
            self.position['entry_price'] if self.position else 0.0,
            self.position['unrealized_pnl'] if self.position else 0.0,
            self.position['holding_bars'] if self.position else 0.0,
            
            # 口座情報
            self.balance,
            self.balance / self.initial_balance,  # リターン
            self.total_trades,
            self.winning_trades / max(1, self.total_trades)  # 勝率
        ], dtype=np.float32)
        
        return obs
    
    def step(self, action):
        """アクションを実行"""
        current_price = self.data.iloc[self.current_step]['close']
        atr = self.data.iloc[self.current_step]['atr']
        
        reward = 0
        done = False
        
        # アクション実行
        if action == 1:  # Buy Small
            if not self.position:
                self.position = {
                    'entry_price': current_price,
                    'size': 0.01,  # 小ロット
                    'entry_step': self.current_step,
                    'stop_loss': current_price - 2 * atr,
                    'take_profit': current_price + 4 * atr
                }
        
        elif action == 2:  # Buy Medium
            if not self.position:
                self.position = {
                    'entry_price': current_price,
                    'size': 0.02,  # 中ロット
                    'entry_step': self.current_step,
                    'stop_loss': current_price - 2 * atr,
                    'take_profit': current_price + 4 * atr
                }
        
        elif action == 3:  # Buy Large
            if not self.position:
                self.position = {
                    'entry_price': current_price,
                    'size': 0.03,  # 大ロット
                    'entry_step': self.current_step,
                    'stop_loss': current_price - 2 * atr,
                    'take_profit': current_price + 4 * atr
                }
        
        elif action == 4:  # Close Half
            if self.position:
                pnl = (current_price - self.position['entry_price']) * self.position['size'] * 0.5
                self.balance += pnl
                self.position['size'] *= 0.5
                reward += pnl * 10
        
        elif action == 5:  # Close All
            if self.position:
                pnl = (current_price - self.position['entry_price']) * self.position['size']
                self.balance += pnl
                self.total_trades += 1
                if pnl > 0:
                    self.winning_trades += 1
                    reward += pnl * 10 + 5  # 勝ちトレードボーナス
                else:
                    reward += pnl * 10  # 負けはそのまま反映
                self.position = None
        
        # ポジション管理
        if self.position:
            self.position['holding_bars'] = self.current_step - self.position['entry_step']
            self.position['unrealized_pnl'] = (current_price - self.position['entry_price']) * self.position['size']
            
            # ストップロス・テイクプロフィットのチェック
            if current_price <= self.position['stop_loss']:
                pnl = -2 * atr * self.position['size']
                self.balance += pnl
                self.total_trades += 1
                reward += pnl * 10  # 損失
                self.position = None
            
            elif current_price >= self.position['take_profit']:
                pnl = 4 * atr * self.position['size']
                self.balance += pnl
                self.total_trades += 1
                self.winning_trades += 1
                reward += pnl * 10 + 10  # 大きなボーナス
                self.position = None
        
        # 次のステップへ
        self.current_step += 1
        
        # エピソード終了判定
        if self.current_step >= len(self.data) - 1:
            done = True
        
        if self.balance < self.initial_balance * 0.5:  # 50%以上の損失
            done = True
            reward -= 100  # 大きなペナルティ
        
        obs = self._get_observation()
        info = {
            'balance': self.balance,
            'total_trades': self.total_trades,
            'win_rate': self.winning_trades / max(1, self.total_trades)
        }
        
        return obs, reward, done, info


class TradingEnvironment_Scenario_1_2(gym.Env):
    """
    シナリオ1_2: トレンド連続・押し目狙い専用の取引環境
    """
    def __init__(self, data, initial_balance=100000):
        super().__init__()
        
        self.data = data
        self.initial_balance = initial_balance
        
        # アクション空間: 押し目に特化したアクション
        # 0=Hold, 1=Buy_at_Fib_382, 2=Buy_at_Fib_500, 3=Buy_at_Fib_618,
        # 4=Close_Half, 5=Close_All
        self.action_space = spaces.Discrete(6)
        
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, 
            shape=(25,),
            dtype=np.float32
        )
        
        self.reset()
    
    def reset(self):
        self.current_step = 100
        self.balance = self.initial_balance
        self.position = None
        self.total_trades = 0
        self.winning_trades = 0
        return self._get_observation()
    
    def _get_observation(self):
        """シナリオ1_2固有の観測"""
        current_data = self.data.iloc[self.current_step]
        
        obs = np.array([
            # 基本情報
            current_data['close'],
            current_data['high'],
            current_data['low'],
            
            # テクニカル指標
            current_data['ema9'],
            current_data['ema21'],
            current_data['macd'],
            current_data['rsi'],
            current_data['atr'],
            
            # シナリオ1_2固有の特徴量
            current_data['fib_382_distance'],   # フィボナッチ38.2%までの距離
            current_data['fib_500_distance'],   # フィボナッチ50%までの距離
            current_data['fib_618_distance'],   # フィボナッチ61.8%までの距離
            current_data['pullback_depth'],     # 押し目の深さ
            current_data['n_wave_phase'],       # N波動のフェーズ
            current_data['dow_trend'],          # トレンド方向
            current_data['swing_low'],          # スイングロー
            
            # ポジション情報（省略: 前述と同様）
            # ...
        ], dtype=np.float32)
        
        return obs
    
    def step(self, action):
        """押し目エントリーに特化したステップ処理"""
        # 実装は省略（シナリオ1_1と同様の構造）
        pass


# 他のシナリオも同様に実装
class TradingEnvironment_Scenario_2_1(gym.Env):
    """シナリオ2_1: レンジブレイク専用環境"""
    pass

class TradingEnvironment_Scenario_2_2(gym.Env):
    """シナリオ2_2: サポートラインブレイク専用環境"""
    pass

class TradingEnvironment_Scenario_3_1(gym.Env):
    """シナリオ3_1: トレンドラインブレイク専用環境"""
    pass

class TradingEnvironment_Scenario_3_2(gym.Env):
    """シナリオ3_2: チャネル内サポート専用環境"""
    pass

class TradingEnvironment_Scenario_3_3(gym.Env):
    """シナリオ3_3: レンジ内サポート専用環境"""
    pass
```

**実装タスク**
- [ ] シナリオ1_1環境の完全実装とテスト
- [ ] シナリオ1_2環境の完全実装とテスト
- [ ] シナリオ2_1環境の完全実装とテスト
- [ ] シナリオ2_2環境の完全実装とテスト
- [ ] シナリオ3_1環境の完全実装とテスト
- [ ] シナリオ3_2環境の完全実装とテスト
- [ ] シナリオ3_3環境の完全実装とテスト
- [ ] 各環境の動作確認（ランダムアクションでテスト）

### 3.3 XGBoostベース強化学習エージェントの実装

**重要**: 深層学習（DQN, PPO）ではなく、**XGBoostを使った強化学習**を実装します。

#### 3.3.1 XGBoost Q-Learning実装
- [ ] ダウ理論転換の確認本数
- [ ] EMA9トレンド転換の判定基準
- [ ] MACD確認の感度
- [ ] サポートライン反転の判定条件
- [ ] ストップロス位置（トレンドライン or サポートライン）
- [ ] 利確目標（前回高値 or N波動）

**シナリオ3_2: チャネル内サポート**
- [ ] チャネル検出の信頼度閾値
- [ ] チャネル下限反発の判定基準
- [ ] フィボナッチレベルの優先度
- [ ] ダウ理論内部トレンドの重み
- [ ] エントリータイミング（反発直後 or 確認後）
- [ ] ストップロス幅（チャネル下限からの距離）
- [ ] 利確目標（チャネル上限 or 中間ライン）

**シナリオ3_3: レンジ内サポート**
- [ ] レンジ判定の最小継続期間
- [ ] レンジ下限反発の判定基準
- [ ] フィボナッチタイミングの許容誤差
- [ ] ダウ理論小波動の重要度
- [ ] エントリー位置（レンジ下限からの%）
- [ ] ストップロス幅（レンジ幅の何%？）
- [ ] 利確目標（レンジ上限 or レンジ中央）

**その他シナリオ（トレンドラインブレイク、チャネル内、レンジ内）**
- [ ] 各シナリオ固有のパラメータ定義

#### 共通パラメータ（全シナリオで調整可能）
- [ ] ポジションサイズ（資金の何%？）
- [ ] 最大保有時間
- [ ] トレーリングストップの開始条件
- [ ] 部分利確のタイミング

### 3.3 XGBoostベースQ-Learningエージェントの実装（7-10日）

**重要**: 深層学習（DQN, PPO）ではなく、**XGBoostを使った強化学習**を実装します。

**クラスタ対応**: 各クラスタごとに独立したQ-Learningエージェントを訓練します。

#### 3.3.1 クラスタ別XGBoost Q-Learning実装

```python
# src/rl/xgboost_qlearning.py
import xgboost as xgb
import numpy as np
from collections import deque
import random
import joblib

class ClusterXGBoostQLearningAgent:
    """
    XGBoostを使ったQ-Learning エージェント（クラスタ対応）
    
    各クラスタごとに独立したエージェントを作成。
    状態とアクションを入力として、Q値を予測するXGBoostモデルを学習。
    """
    def __init__(self, cluster_id, cluster_name, n_actions, n_features):
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.n_actions = n_actions
        self.n_features = n_features
        
        # ハイパーパラメータ
        self.gamma = 0.95  # 割引率
        self.epsilon = 1.0  # 探索率（初期値100%）
        self.epsilon_min = 0.05  # 最小探索率
        self.epsilon_decay = 0.995  # 探索率減衰
        self.learning_rate = 0.1
        
        # 経験リプレイバッファ
        self.memory = deque(maxlen=10000)
        self.batch_size = 64
        
        # アクション別XGBoostモデル（各アクションごとにQ値を予測）
        self.q_models = {}
        for action in range(n_actions):
            self.q_models[action] = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                objective='reg:squarederror',
                random_state=42
            )
        
        self.trained = False
        self.training_history = []
    
    def get_action(self, state, training=True):
        """
        ε-greedy法でアクションを選択
        
        Args:
            state: 現在の状態ベクトル
            training: 訓練中かどうか
        
        Returns:
            選択されたアクション
        """
        # 探索（ランダムアクション）
        if training and np.random.rand() <= self.epsilon:
            return np.random.randint(0, self.n_actions)
        
        # 活用（最善アクション）
        if self.trained:
            q_values = self.predict_q_values(state)
            return np.argmax(q_values)
        else:
            # 未訓練の場合はランダム
            return np.random.randint(0, self.n_actions)
    
    def predict_q_values(self, state):
        """
        全アクションのQ値を予測
        
        Returns:
            各アクションのQ値配列
        """
        q_values = []
        state = state.reshape(1, -1)
        
        for action in range(self.n_actions):
            if self.trained:
                q_val = self.q_models[action].predict(state)[0]
            else:
                q_val = 0.0
            q_values.append(q_val)
        
        return np.array(q_values)
    
    def remember(self, state, action, reward, next_state, done):
        """経験を記憶"""
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self):
        """
        経験リプレイによる学習
        
        メモリからランダムにバッチをサンプリングし、
        各アクションのQ値を更新
        """
        if len(self.memory) < self.batch_size:
            return
        
        # ランダムサンプリング
        minibatch = random.sample(self.memory, self.batch_size)
        
        # アクションごとにデータを分離
        action_data = {a: {'X': [], 'y': []} for a in range(self.n_actions)}
        
        for state, action, reward, next_state, done in minibatch:
            # ターゲットQ値の計算
            if done:
                target = reward
            else:
                # Bellman方程式: Q(s,a) = r + γ * max(Q(s',a'))
                next_q_values = self.predict_q_values(next_state)
                target = reward + self.gamma * np.max(next_q_values)
            
            # 学習データに追加
            action_data[action]['X'].append(state)
            action_data[action]['y'].append(target)
        
        # 各アクションのモデルを更新
        for action in range(self.n_actions):
            if len(action_data[action]['X']) > 0:
                X = np.array(action_data[action]['X'])
                y = np.array(action_data[action]['y'])
                
                # インクリメンタル学習（XGBoostのxgb_model引数を使用）
                if self.trained:
                    self.q_models[action].fit(
                        X, y,
                        xgb_model=self.q_models[action].get_booster()
                    )
                else:
                    self.q_models[action].fit(X, y)
        
        # εを減衰
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        self.trained = True
    
    def train(self, env, n_episodes=1000, verbose=True):
        """
        環境でエージェントを訓練
        
        Args:
            env: ClusterTradingEnvironment
            n_episodes: エピソード数
            verbose: 進捗表示
        
        Returns:
            訓練履歴
        """
        print(f"\n{'='*60}")
        print(f"クラスタ {self.cluster_id} ({self.cluster_name}) のエージェント訓練開始")
        print(f"{'='*60}")
        
        for episode in range(n_episodes):
            state = env.reset()
            total_reward = 0
            done = False
            step = 0
            
            while not done:
                # アクション選択
                action = self.get_action(state, training=True)
                
                # 環境でアクション実行
                next_state, reward, done, info = env.step(action)
                
                # 経験を記憶
                self.remember(state, action, reward, next_state, done)
                
                # 学習
                if len(self.memory) >= self.batch_size:
                    self.replay()
                
                state = next_state
                total_reward += reward
                step += 1
            
            self.training_history.append({
                'episode': episode,
                'total_reward': total_reward,
                'epsilon': self.epsilon,
                'balance': info['balance'],
                'trades': info['trades']
            })
            
            # 進捗表示
            if verbose and (episode + 1) % 100 == 0:
                avg_reward = np.mean([h['total_reward'] for h in self.training_history[-100:]])
                avg_balance = np.mean([h['balance'] for h in self.training_history[-100:]])
                print(f"エピソード {episode+1}/{n_episodes} - "
                      f"平均報酬: {avg_reward:.2f}, "
                      f"平均残高: {avg_balance:.2f}, "
                      f"ε: {self.epsilon:.3f}")
        
        print(f"✓ 訓練完了")
        return self.training_history
    
    def save(self, filepath):
        """エージェントを保存"""
        save_data = {
            'cluster_id': self.cluster_id,
            'cluster_name': self.cluster_name,
            'n_actions': self.n_actions,
            'n_features': self.n_features,
            'q_models': self.q_models,
            'epsilon': self.epsilon,
            'training_history': self.training_history,
            'trained': self.trained
        }
        joblib.dump(save_data, filepath)
        print(f"✓ エージェントを保存: {filepath}")
    
    @classmethod
    def load(cls, filepath):
        """エージェントを読み込み"""
        save_data = joblib.load(filepath)
        
        agent = cls(
            save_data['cluster_id'],
            save_data['cluster_name'],
            save_data['n_actions'],
            save_data['n_features']
        )
        agent.q_models = save_data['q_models']
        agent.epsilon = save_data['epsilon']
        agent.training_history = save_data['training_history']
        agent.trained = save_data['trained']
        
        print(f"✓ エージェントを読み込み: {filepath}")
        return agent
```

#### 3.3.2 全クラスタのエージェント訓練

```python
# scripts/train_cluster_agents.py
"""
全クラスタのRL エージェントを並行訓練
"""
from src.rl.xgboost_qlearning import ClusterXGBoostQLearningAgent
from src.rl.trading_environment import ClusterTradingEnvironment
from src.clustering.market_regime_detector import MarketRegimeDetector
import json

def train_all_cluster_agents(data, detector, cluster_labels, n_episodes=1000):
    """
    すべてのトレード可能クラスタでエージェントを訓練
    """
    print("\n" + "="*60)
    print("全クラスタエージェント訓練")
    print("="*60)
    
    agents = {}
    training_results = {}
    
    # トレード可能なクラスタを取得
    tradeable_clusters = [
        cid for cid in range(detector.n_clusters)
        if len(data[data['cluster'] == cid]) >= 100
    ]
    
    print(f"訓練対象クラスタ: {tradeable_clusters}")
    
    for cluster_id in tradeable_clusters:
        cluster_name = cluster_labels.get(cluster_id, f"Cluster_{cluster_id}")
        
        try:
            # 環境作成
            env = ClusterTradingEnvironment(
                data=data,
                cluster_id=cluster_id,
                cluster_labels=cluster_labels,
                initial_balance=100000,
                commission=0.002
            )
            
            # エージェント作成
            agent = ClusterXGBoostQLearningAgent(
                cluster_id=cluster_id,
                cluster_name=cluster_name,
                n_actions=7,
                n_features=STATE_SIZE
            )
            
            # 訓練
            history = agent.train(env, n_episodes=n_episodes, verbose=True)
            
            # 保存
            agent.save(f'models/layer2/agent_cluster_{cluster_id}.pkl')
            
            agents[cluster_id] = agent
            training_results[cluster_id] = history
            
        except Exception as e:
            print(f"✗ クラスタ {cluster_id} の訓練に失敗: {e}")
            continue
    
    # 結果をJSON保存
    with open('outputs/cluster_agents_training_results.json', 'w') as f:
        json.dump(training_results, f, indent=2)
    
    print(f"\n✓ {len(agents)}個のエージェント訓練完了")
    return agents, training_results

# 実行
if __name__ == "__main__":
    # データ読み込み
    data = pd.read_csv('data/processed/features_with_clusters.csv')
    
    # クラスタ検出器読み込み
    detector = MarketRegimeDetector()
    detector.load('models/layer1/market_regime_detector.pkl')
    
    # クラスタラベル読み込み
    with open('config/cluster_labels.json', 'r', encoding='utf-8') as f:
        cluster_labels = json.load(f)
    
    # 訓練実行
    agents, results = train_all_cluster_agents(
        data, 
        detector, 
        cluster_labels, 
        n_episodes=1000
    )
```

**作業チェックリスト**:
- [ ] ClusterXGBoostQLearningAgentクラスを実装
- [ ] 各クラスタの環境でエージェントを訓練
- [ ] 訓練履歴をグラフで確認
- [ ] エージェントをmodels/layer2/に保存

---

### 3.4 【参考】シナリオ別XGBoost Q-Learning（従来型）

以下は従来のシナリオベースのアプローチです。

#### 3.4.1 【参考】シナリオ別実装

```python
# 従来型（参考）
class XGBoostQLearningAgent:
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.1
        
        # 経験リプレイバッファ
        self.memory = deque(maxlen=10000)
        self.batch_size = 64
        
        # 各アクションに対するXGBoostモデル
        self.models = {}
        for action in range(n_actions):
            self.models[action] = xgb.XGBRegressor(
                objective='reg:squarederror',
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                tree_method='hist'
            )
        
        # 初期化用のダミーデータで訓練
        self._initialize_models()
    
    def _initialize_models(self):
        """モデルの初期化"""
        X_init = np.random.random((100, self.n_features))
        y_init = np.zeros(100)
        
        for action in range(self.n_actions):
            self.models[action].fit(X_init, y_init)
    
    def remember(self, state, action, reward, next_state, done):
        """経験を記憶"""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """行動選択（ε-greedy）"""
        if np.random.random() <= self.epsilon:
            return random.randrange(self.n_actions)  # ランダムアクション
        
        # 各アクションのQ値を予測
        q_values = []
        for action in range(self.n_actions):
            q_value = self.models[action].predict(state.reshape(1, -1))[0]
            q_values.append(q_value)
        
        return np.argmax(q_values)  # 最大Q値のアクション
    
    def replay(self):
        """経験リプレイで学習"""
        if len(self.memory) < self.batch_size:
            return
        
        # ミニバッチをサンプリング
        minibatch = random.sample(self.memory, self.batch_size)
        
        # アクションごとにデータを分類
        training_data = {action: {'X': [], 'y': []} for action in range(self.n_actions)}
        
        for state, action, reward, next_state, done in minibatch:
            if done:
                target = reward
            else:
                # 次状態の最大Q値を取得
                next_q_values = []
                for a in range(self.n_actions):
                    next_q = self.models[a].predict(next_state.reshape(1, -1))[0]
                    next_q_values.append(next_q)
                
                target = reward + self.gamma * np.max(next_q_values)
            
            training_data[action]['X'].append(state)
            training_data[action]['y'].append(target)
        
        # 各アクションのモデルを更新
        for action in range(self.n_actions):
            if len(training_data[action]['X']) > 0:
                X = np.array(training_data[action]['X'])
                y = np.array(training_data[action]['y'])
                
                # XGBoostモデルの増分学習（xgb_modelで継続学習）
                self.models[action].fit(
                    X, y,
                    xgb_model=self.models[action].get_booster()
                )
        
        # 探索率を減衰
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save(self, filepath):
        """モデルの保存"""
        for action in range(self.n_actions):
            self.models[action].save_model(f"{filepath}_action_{action}.json")
    
    def load(self, filepath):
        """モデルの読み込み"""
        for action in range(self.n_actions):
            self.models[action].load_model(f"{filepath}_action_{action}.json")


# シナリオごとのエージェント作成
def create_agent_for_scenario(scenario_id):
    """
    シナリオごとに適切なアクション数と特徴量数でエージェント作成
    """
    agent_configs = {
        '1_1': {'n_actions': 7, 'n_features': 25},  # ブレイクアウト
        '1_2': {'n_actions': 6, 'n_features': 25},  # 押し目
        '2_1': {'n_actions': 7, 'n_features': 25},  # レンジブレイク
        '2_2': {'n_actions': 6, 'n_features': 23},  # サポートブレイク
        '3_1': {'n_actions': 7, 'n_features': 26},  # トレンドラインブレイク
        '3_2': {'n_actions': 6, 'n_features': 24},  # チャネル
        '3_3': {'n_actions': 6, 'n_features': 24},  # レンジ内
    }
    
    config = agent_configs[scenario_id]
    return XGBoostQLearningAgent(
        scenario_id=scenario_id,
        n_actions=config['n_actions'],
        n_features=config['n_features']
    )
```

#### 3.3.2 エージェントの訓練

```python
def train_agent(agent, env, episodes=1000):
    """
    XGBoost Q-Learningエージェントの訓練
    """
    episode_rewards = []
    episode_trades = []
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        step = 0
        
        while not done:
            # アクション選択
            action = agent.act(state)
            
            # アクション実行
            next_state, reward, done, info = env.step(action)
            
            # 経験を記憶
            agent.remember(state, action, reward, next_state, done)
            
            state = next_state
            total_reward += reward
            step += 1
            
            # 経験リプレイで学習
            if step % 10 == 0:  # 10ステップごとに学習
                agent.replay()
        
        episode_rewards.append(total_reward)
        episode_trades.append(info['total_trades'])
        
        # 進捗表示
        if episode % 50 == 0:
            avg_reward = np.mean(episode_rewards[-50:])
            avg_trades = np.mean(episode_trades[-50:])
            print(f"Episode: {episode}, Avg Reward: {avg_reward:.2f}, "
                  f"Avg Trades: {avg_trades:.1f}, Epsilon: {agent.epsilon:.3f}, "
                  f"Win Rate: {info['win_rate']:.2%}")
    
    return episode_rewards

# 各シナリオのエージェントを訓練
scenarios = ['1_1', '1_2', '2_1', '2_2', '3_1', '3_2', '3_3']

for scenario_id in scenarios:
    print(f"\n========== Training Agent for Scenario {scenario_id} ==========")
    
    # 環境とエージェントの作成
    if scenario_id == '1_1':
        env = TradingEnvironment_Scenario_1_1(train_data)
    elif scenario_id == '1_2':
        env = TradingEnvironment_Scenario_1_2(train_data)
    # 他のシナリオも同様
    
    agent = create_agent_for_scenario(scenario_id)
    
    # 訓練実行
    rewards = train_agent(agent, env, episodes=1000)
    
    # モデル保存
    agent.save(f'models/layer2/rl_agents/xgboost_agent_scenario_{scenario_id}')
    
    # 学習曲線のプロット
    plt.plot(rewards)
    plt.title(f'Scenario {scenario_id} - Learning Curve')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.savefig(f'models/layer2/rl_agents/learning_curve_{scenario_id}.png')
    plt.close()
```

**実装タスク**
- [ ] XGBoost Q-Learningエージェントの完全実装
- [ ] シナリオ1_1エージェントの訓練と評価
- [ ] シナリオ1_2エージェントの訓練と評価
- [ ] シナリオ2_1エージェントの訓練と評価
- [ ] シナリオ2_2エージェントの訓練と評価
- [ ] シナリオ3_1エージェントの訓練と評価
- [ ] シナリオ3_2エージェントの訓練と評価
- [ ] シナリオ3_3エージェントの訓練と評価
- [ ] 学習曲線の分析と最適化

#### 3.3.3 ハイパーパラメータチューニング

```python
import optuna

def optimize_agent_hyperparameters(scenario_id, env, n_trials=100):
    """
    Optunaでエージェントのハイパーパラメータを最適化
    """
    def objective(trial):
        # ハイパーパラメータ提案
        gamma = trial.suggest_float('gamma', 0.9, 0.99)
        epsilon_decay = trial.suggest_float('epsilon_decay', 0.990, 0.999)
        batch_size = trial.suggest_int('batch_size', 32, 128)
        
        xgb_params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 200),
            'max_depth': trial.suggest_int('max_depth', 3, 8),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        }
        
        # エージェント作成
        agent = create_agent_for_scenario(scenario_id)
        agent.gamma = gamma
        agent.epsilon_decay = epsilon_decay
        agent.batch_size = batch_size
        
        # XGBoostパラメータ更新
        for action in range(agent.n_actions):
            agent.models[action] = xgb.XGBRegressor(**xgb_params, tree_method='hist')
            agent.models[action].fit(
                np.random.random((100, agent.n_features)),
                np.zeros(100)
            )
        
        # 短期間の訓練
        rewards = train_agent(agent, env, episodes=100)
        
        # 最後50エピソードの平均報酬を返す
        return np.mean(rewards[-50:])
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    
    return study.best_params
```

- [ ] 各シナリオのハイパーパラメータ最適化
- [ ] 最適パラメータでの再訓練

### 3.4 統合とバックテスト（3-4日）

#### 3.4.1 Layer 2（強化学習）の統合実装

**シナリオごとに独立した最適化を実行**

```python
# シナリオ1_1専用の最適化
def optimize_scenario_1_1(historical_data):
    def objective(trial):
        params = {
            'breakout_threshold': trial.suggest_float('breakout_threshold', 1, 10),
            'n_wave_ratio': trial.suggest_categorical('n_wave_ratio', [1.0, 1.6, 2.0, 2.618]),
            'ema_distance': trial.suggest_int('ema_distance', 5, 50),
            'stop_loss_atr': trial.suggest_float('stop_loss_atr', 1.0, 3.0),
            'confirmation_bars': trial.suggest_int('confirmation_bars', 1, 5)
        }
        
        # シナリオ1_1のストラテジーでバックテスト
        results = backtest_scenario_1_1(historical_data, params)
        return results['sharpe_ratio']
    
    study = optuna.create_study(direction='maximize', study_name='scenario_1_1')
    study.optimize(objective, n_trials=1000)
    return study.best_params

# シナリオ1_2専用の最適化
def optimize_scenario_1_2(historical_data):
    def objective(trial):
        params = {
            'fib_tolerance': trial.suggest_float('fib_tolerance', 1, 20),
            'max_wait_bars': trial.suggest_int('max_wait_bars', 3, 20),
            'entry_timing': trial.suggest_categorical('entry_timing', ['immediate', 'confirmation']),
            'stop_loss_type': trial.suggest_categorical('stop_loss_type', ['swing_low', 'fib_level']),
            'n_wave_weight': trial.suggest_float('n_wave_weight', 0.5, 1.5)
        }
        
        results = backtest_scenario_1_2(historical_data, params)
        return results['sharpe_ratio']
    
    study = optuna.create_study(direction='maximize', study_name='scenario_1_2')
    study.optimize(objective, n_trials=1000)
    return study.best_params

# 他のシナリオも同様に実装
def optimize_scenario_2_1(historical_data): ...
def optimize_scenario_2_2(historical_data): ...
def optimize_scenario_3_1(historical_data): ...
def optimize_scenario_3_2(historical_data): ...
def optimize_scenario_3_3(historical_data): ...
```

**実装タスク**
- [ ] シナリオ1_1の最適化関数とバックテスト
- [ ] シナリオ1_2の最適化関数とバックテスト
- [ ] シナリオ2_1の最適化関数とバックテスト
- [ ] シナリオ2_2の最適化関数とバックテスト
- [ ] シナリオ3_1の最適化関数とバックテスト
- [ ] シナリオ3_2の最適化関数とバックテスト
- [ ] シナリオ3_3の最適化関数とバックテスト
- [ ] 全シナリオの最適化を一括実行するスクリプト

#### 3.2.2 マルチオブジェクティブ最適化（応用）
- [ ] 複数指標の同時最適化（シャープレシオ + 最大ドローダウン）
- [ ] パレート最適解の取得
- [ ] トレードオフ分析

#### 3.2.3 ウォークフォワード分析（オーバーフィッティング防止）
```python
def walk_forward_optimization(data, scenario_id, n_splits=5):
    """
    時系列を考慮したウォークフォワード分析
    """
    results = []
    split_size = len(data) // (n_splits + 1)
    
    for i in range(n_splits):
        # 訓練期間とテスト期間を分割
        train_start = 0
        train_end = split_size * (i + 1)
        test_start = train_end
        test_end = split_size * (i + 2)
        
        train_data = data[train_start:train_end]
        test_data = data[test_start:test_end]
        
        # 訓練期間で最適化
        if scenario_id == '1_1':
            best_params = optimize_scenario_1_1(train_data)
        elif scenario_id == '1_2':
            best_params = optimize_scenario_1_2(train_data)
        elif scenario_id == '2_1':
            best_params = optimize_scenario_2_1(train_data)
        elif scenario_id == '2_2':
            best_params = optimize_scenario_2_2(train_data)
        elif scenario_id == '3_1':
            best_params = optimize_scenario_3_1(train_data)
        elif scenario_id == '3_2':
            best_params = optimize_scenario_3_2(train_data)
        elif scenario_id == '3_3':
            best_params = optimize_scenario_3_3(train_data)
        # 他のシナリオも同様
        
        # テスト期間で検証
        test_results = backtest_with_params(test_data, best_params, scenario_id)
        results.append(test_results)
    
    return results
```

- [ ] 各シナリオのウォークフォワード分析実行
- [ ] 安定性の評価（期間ごとのパフォーマンス変動）
- [ ] 最終的な推奨パラメータの決定

#### 3.2.4 市場環境適応型パラメータ（応用）
各シナリオ内でさらに市場環境に応じてパラメータを動的調整

- [ ] ボラティリティレジーム検出
  - 高ボラ環境: ストップロス広め
  - 低ボラ環境: ストップロス狭め

- [ ] トレンド強度別パラメータ
  - 強トレンド: ブレイクアウト重視
  - 弱トレンド: 押し目重視

#### 3.2.5 最適化結果の保存（重要）
```python
# 各シナリオの最適パラメータを保存
optimal_params = {
    'scenario_1_1': {
        'breakout_threshold': 3.5,
        'n_wave_ratio': 1.618,
        'ema_distance': 15,
        'stop_loss_atr': 2.0,
        'confirmation_bars': 2
    },
    'scenario_1_2': {
        'fib_tolerance': 8.0,
        'max_wait_bars': 10,
        'entry_timing': 'confirmation',
        'stop_loss_type': 'swing_low',
        'n_wave_weight': 1.2
    },
    'scenario_2_1': { ... },
    'scenario_2_2': { ... },
    'scenario_3_1': {
        'trendline_break_threshold': 5.0,
        'dow_confirmation_bars': 3,
        'ema9_reversal_threshold': 0.05,
        'macd_sensitivity': 'medium',
        'support_reversal_pips': 10,
        'stop_loss_type': 'trendline',
        'target_type': 'n_wave'
    },
    'scenario_3_2': {
        'channel_confidence': 0.8,
        'channel_support_threshold': 3.0,
        'fib_priority': 'high',
        'dow_internal_weight': 0.7,
        'entry_timing': 'confirmation',
        'stop_loss_distance': 10,
        'target_type': 'channel_upper'
    },
    'scenario_3_3': {
        'range_min_duration': 20,
        'range_support_threshold': 5.0,
        'fib_tolerance': 8.0,
        'dow_mini_wave_weight': 0.6,
        'entry_position_pct': 0.1,
        'stop_loss_pct': 0.05,
        'target_type': 'range_upper'
    }
}

# JSONファイルとして保存
import json
with open('models/layer2/optimal_params.json', 'w') as f:
    json.dump(optimal_params, f, indent=2)
```

- [ ] 各シナリオの最適パラメータをJSON形式で保存
- [ ] パラメータのバージョン管理
- [ ] パラメータの説明ドキュメント作成

### 3.3 アプローチB: シナリオ別強化学習モデル（オプション/高難度）

**各シナリオごとに独立した強化学習エージェントを訓練**

#### 3.3.1 シナリオ専用環境の構築
```python
import gym
from stable_baselines3 import PPO

class TradingEnvironment_Scenario_1_1(gym.Env):
    """シナリオ1_1専用の取引環境"""
    def __init__(self, data):
        # シナリオ1_1に特化したアクション空間
        self.action_space = gym.spaces.Discrete(4)  
        # 0: Hold, 1: Buy (aggressive), 2: Buy (conservative), 3: Close
        
        # シナリオ1_1に関連する観測空間
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, 
            shape=(feature_dim,), dtype=np.float32
        )
        # 特徴量: ブレイク幅、N波動比率、EMA乖離率など
        
    def step(self, action):
        # シナリオ1_1固有のロジックで報酬計算
        reward = self.calculate_scenario_1_1_reward(action)
        return observation, reward, done, info
    
    def reset(self):
        return initial_observation

class TradingEnvironment_Scenario_1_2(gym.Env):
    """シナリオ1_2専用の取引環境"""
    def __init__(self, data):
        # シナリオ1_2に特化したアクション空間
        self.action_space = gym.spaces.Discrete(5)
        # 0: Wait, 1: Buy at Fib 38.2%, 2: Buy at Fib 50%, 
        # 3: Buy at Fib 61.8%, 4: Close
        
        self.observation_space = gym.spaces.Box(...)
        # 特徴量: フィボナッチレベルまでの距離、押し目の深さなど
    
    def step(self, action):
        reward = self.calculate_scenario_1_2_reward(action)
        return observation, reward, done, info
    
    def reset(self):
        return initial_observation

# 他のシナリオも同様に実装
```

#### 3.3.2 シナリオごとのエージェント訓練
```python
# シナリオ1_1のエージェント訓練
env_1_1 = TradingEnvironment_Scenario_1_1(train_data_1_1)
model_1_1 = PPO('MlpPolicy', env_1_1, verbose=1)
model_1_1.learn(total_timesteps=100000)
model_1_1.save('models/layer2/rl_agent_scenario_1_1')

# シナリオ1_2のエージェント訓練
env_1_2 = TradingEnvironment_Scenario_1_2(train_data_1_2)
model_1_2 = PPO('MlpPolicy', env_1_2, verbose=1)
model_1_2.learn(total_timesteps=100000)
model_1_2.save('models/layer2/rl_agent_scenario_1_2')

# 他のシナリオも同様に訓練
```

#### 3.3.3 報酬関数の設計（シナリオごとに異なる）
- [ ] シナリオ1_1の報酬関数
  - ブレイクアウト成功時のボーナス
  - N波動ターゲット到達時の大きな報酬
  - ダマシブレイクへのペナルティ

- [ ] シナリオ1_2の報酬関数
  - 理想的なフィボナッチレベルでのエントリー報酬
  - 押し目形成確認後のエントリーボーナス
  - 早すぎるエントリーへのペナルティ

- [ ] 共通の報酬要素
  - 利益に対する報酬
  - リスク管理（適切なストップロス）への報酬
  - ドローダウンへのペナルティ

#### 3.3.4 エージェントの評価と選択
- [ ] 各シナリオのエージェントを独立評価
- [ ] ハイパーパラメータチューニング（学習率、ネットワーク構造など）
- [ ] 学習曲線の監視と早期停止

**実装タスク**
- [ ] シナリオ1_1専用環境とエージェント
- [ ] シナリオ1_2専用環境とエージェント
- [ ] シナリオ2_1専用環境とエージェント
- [ ] シナリオ2_2専用環境とエージェント
- [ ] シナリオ3_1専用環境とエージェント
- [ ] シナリオ3_2専用環境とエージェント
- [ ] シナリオ3_3専用環境とエージェント

**注意**: 強化学習は収束が難しく、各シナリオごとに時間がかかるため、まずはアプローチA（パラメータ最適化）の完成を優先することを強く推奨

### 3.4 統合とバックテスト

#### 3.4.1 Layer 2の統合実装
```python
class Layer2Optimizer:
    """各シナリオに対応するパラメータまたはモデルを管理"""
    def __init__(self):
        # シナリオごとの最適パラメータを読み込み
        with open('models/layer2/optimal_params.json', 'r') as f:
            self.optimal_params = json.load(f)
        
        # または、強化学習モデルを読み込み（アプローチBの場合）
        # self.rl_agents = {
        #     'scenario_1_1': PPO.load('models/layer2/rl_agent_scenario_1_1'),
        #     'scenario_1_2': PPO.load('models/layer2/rl_agent_scenario_1_2'),
        #     ...
        # }
    
    def get_parameters(self, scenario_id, market_condition=None):
        """
        指定されたシナリオの最適パラメータを取得
        
        Args:
            scenario_id: シナリオID（'1_1', '1_2'など）
            market_condition: 市場環境（オプション、動的調整用）
        
        Returns:
            最適化されたパラメータ辞書
        """
        base_params = self.optimal_params.get(f'scenario_{scenario_id}', {})
        
        # 市場環境に応じた動的調整（オプション）
        if market_condition:
            base_params = self.adjust_for_market_condition(base_params, market_condition)
        
        return base_params
    
    def adjust_for_market_condition(self, params, market_condition):
        """ボラティリティなどに応じてパラメータを微調整"""
        if market_condition['volatility'] == 'high':
            params['stop_loss_atr'] *= 1.2  # ストップロス広める
        elif market_condition['volatility'] == 'low':
            params['stop_loss_atr'] *= 0.8  # ストップロス狭める
        
        return params
```

#### 3.4.2 完全システムのバックテスト
```python
def integrated_backtest(data, layer1_model, layer2_optimizer):
    """Layer 1とLayer 2を統合したバックテスト"""
    trades = []
    
    for i in range(len(data)):
        current_data = data[:i+1]
        features = create_features(current_data)
        
        # Layer 1: シナリオ判定
        scenario_id, probability = layer1_model.predict_proba(features[-1])
        
        if probability > 0.6:  # 確信度閾値
            # Layer 2: シナリオ専用のパラメータ取得
            optimal_params = layer2_optimizer.get_parameters(scenario_id)
            
            # パラメータを使ってエントリー判定
            if check_entry_conditions(current_data, scenario_id, optimal_params):
                trade = execute_trade(current_data, scenario_id, optimal_params)
                trades.append(trade)
    
    return analyze_trades(trades)
```

- [ ] Layer 2をシステム全体に統合
- [ ] 完全システムのバックテスト実行
  - Layer 1でシナリオ判定
  - Layer 2でシナリオ専用の最適パラメータ適用
  - エントリー/決済実行

#### 3.4.3 シナリオ別パフォーマンス分析
- [ ] 各シナリオの個別パフォーマンス評価
  - シナリオ1_1の勝率、利益率、取引回数
  - シナリオ1_2の勝率、利益率、取引回数
  - シナリオ2_1の勝率、利益率、取引回数
  - シナリオ2_2の勝率、利益率、取引回数
  - シナリオ3_1の勝率、利益率、取引回数
  - シナリオ3_2の勝率、利益率、取引回数
  - シナリオ3_3の勝率、利益率、取引回数

- [ ] シナリオ間の比較
  - どのシナリオが最も利益を出しているか
  - どのシナリオが最も安定しているか
  - 改善が必要なシナリオの特定

#### 3.4.4 Phase 2との比較
- [ ] 全体的なパフォーマンス向上の確認
  - 利益の増加
  - リスク調整後リターン（シャープレシオ）の改善
  - 最大ドローダウンの削減
  - 勝率の向上

- [ ] シナリオごとの改善度合い
  - Layer 2導入前後の比較

#### 成果物
- Layer2統合バックテストレポート（Phase3_layer2_report.pdf）
- シナリオ別最適パラメータ一覧（optimal_params.json）
- 各シナリオのパフォーマンス比較表
- パラメータ感度分析レポート
- 改善提案リスト

---

## 🚀 Phase 4: システム統合とフォワードテスト

**目標**: 完全な自動取引システムの構築とデモ口座でのテスト

### 4.1 リアルタイム取引システムの構築

#### 4.1.1 リアルタイムデータ取得
- [ ] MT5からのリアルタイムティック取得
- [ ] 定期的なデータ更新（1分ごとなど）
- [ ] 複数時間軸の同期更新

#### 4.1.2 シグナル生成パイプライン
```python
class RealTimeTradingSystem:
    def __init__(self):
        self.layer1_model = load_model('models/layer1/best_model.pkl')
        
        # Layer 2: シナリオごとの最適パラメータを読み込み
        with open('models/layer2/optimal_params.json', 'r') as f:
            self.layer2_params = json.load(f)
        
        # またはシナリオ別ファイルから読み込み
        # self.layer2_params = {
        #     'scenario_1_1': json.load(open('models/layer2/scenario_1_1_params.json')),
        #     'scenario_1_2': json.load(open('models/layer2/scenario_1_2_params.json')),
        #     ...
        # }
        
    def run(self):
        while True:
            # データ取得
            current_data = self.get_latest_data()
            
            # 特徴量計算
            features = self.create_features(current_data)
            
            # Layer 1: シナリオ判定
            scenario, probability = self.layer1_model.predict_proba(features)
            
            if probability > 0.6:  # 確信度閾値
                # Layer 2: 該当シナリオの最適パラメータ取得
                params = self.layer2_params[f'scenario_{scenario}']
                
                # エントリー判定（シナリオ専用のロジックとパラメータ使用）
                if self.check_entry_conditions(current_data, scenario, params):
                    self.place_order(scenario, params)
            
            # 既存ポジションの管理
            self.manage_positions()
            
            time.sleep(60)  # 1分待機
```

#### 4.1.3 注文執行システム
- [ ] MT5への注文送信
- [ ] ポジション管理
  - オープンポジションの追跡
  - ストップロス/テイクプロフィットの設定
  - トレーリングストップの実装

- [ ] エラーハンドリング
  - 接続エラー
  - 注文拒否
  - スリッページ対応

### 4.2 リスク管理システム

- [ ] 資金管理ルール
  - 最大ポジションサイズ
  - 1トレードあたりの最大リスク（資金の1-2%）
  - 同時保有ポジション数制限

- [ ] デイリーストップロス
  - 1日の最大損失額
  - 連続損失回数制限

- [ ] 緊急停止機能
  - 異常なドローダウン検出
  - システムエラー時の自動停止

### 4.3 ロギングとモニタリング

- [ ] 取引ログの記録
  - エントリー/決済の詳細
  - 判断理由（どのシナリオ、どのパラメータ）
  - 各Layer の出力

- [ ] パフォーマンスダッシュボード
  - リアルタイム損益
  - 勝率、プロフィットファクター
  - オープンポジション一覧

- [ ] アラート機能
  - 重要なシグナル発生時
  - エラー発生時
  - 目標達成/損失閾値到達時

### 4.4 デモ口座でのフォワードテスト

- [ ] デモ口座での稼働開始
- [ ] 日次パフォーマンスレビュー
- [ ] 問題点の洗い出し
  - 予期しない動作
  - モデルの誤判断パターン
  - システムバグ

- [ ] 継続的な改善
  - モデルの再学習
  - パラメータの微調整
  - バグ修正

#### 成果物
- フォワードテスト結果レポート（Phase4_forward_test_report.pdf）
- トレードジャーナル
- システム改善提案書

---

## 🔄 Phase 5: 継続的改善とリアル運用準備（継続的）

### 5.1 モデルの定期更新（月次）

- [ ] 最新データでのモデル再学習
- [ ] パフォーマンスドリフトの監視
  - モデル精度の低下検出
  - 市場環境変化への適応

- [ ] A/Bテスト
  - 新旧モデルの並行運用
  - パフォーマンス比較

### 5.2 新シナリオの追加

- [ ] 市場分析による新パターン発見
- [ ] 新シナリオのルール化
- [ ] モデルへの統合

### 5.3 リアル口座移行準備

- [ ] 最終チェックリスト
  - [ ] 最低3ヶ月のデモ取引で安定した利益
  - [ ] すべての機能が正常動作
  - [ ] リスク管理システムが堅牢
  - [ ] 緊急時対応マニュアル完備

- [ ] 少額資金での段階的運用開始
- [ ] 徐々に投入資金を増加

---

## 📊 マイルストーン一覧

| Phase | タスク | 期間 | 成功指標 |
|-------|--------|------|----------|
| Phase 0 | 環境構築 | 1-2日 | すべてのライブラリがインストールされている |
| Phase 1 | ルールベースシステム | 2-3週間 | バックテストが実行でき、ベースライン勝率40%以上 |
| Phase 2 | Layer 1（環境認識） | 2-3週間 | モデル精度70%以上、バックテスト勝率が5-10%向上 |
| Phase 3 | Layer 2（最適化） | 2-3週間 | シャープレシオ向上、ドローダウン削減 |
| Phase 4 | フォワードテスト | 2週間+ | デモ口座で安定動作、Phase3と同等のパフォーマンス |
| Phase 5 | リアル運用 | 継続的 | 安定した月次利益 |

**総開発期間**: 約2.5-3ヶ月（フルタイムの場合）

---

## 🛠️ 技術スタック詳細

### 必須ライブラリ
```python
# データ処理
pandas==2.0.0
numpy==1.24.0

# テクニカル指標
pandas-ta==0.3.14b
ta-lib==0.4.26  # または ta-lib-bin（Windows）

# 機械学習
scikit-learn==1.3.0
lightgbm==4.0.0
xgboost==1.7.6
optuna==3.3.0

# バックテスト
backtesting==0.3.3
vectorbt==0.25.0  # オプション

# MT5連携
MetaTrader5==5.0.45

# 可視化
matplotlib==3.7.0
seaborn==0.12.0
mplfinance==0.12.9
plotly==5.14.0

# その他
jupyter==1.0.0
joblib==1.3.0  # モデル保存
pyyaml==6.0  # 設定ファイル
```

### 推奨開発環境
- Python: 3.8 - 3.11
- RAM: 8GB以上
- ストレージ: 50GB以上（ヒストリカルデータ保存用）
- OS: Windows 10/11（MT5との互換性）

---

## ⚠️ 重要な注意事項

### 1. オーバーフィッティングの回避
- 常に訓練データとテストデータを分離
- ウォークフォワード分析を必ず実施
- シンプルなモデルから始める

### 2. リスク管理の徹底
- どれだけAIが優秀でも、リスク管理なしでは破産する
- 1トレードのリスクは口座の1-2%以内
- 感情を排除し、システムを信頼する

### 3. 現実的な期待値
- AIは魔法ではない
- 勝率60-70%、プロフィットファクター1.5-2.0が現実的
- 月利5-10%を安定して達成できれば優秀

### 4. 法令遵守
- 自動売買が許可されているブローカーを使用
- 税務申告を適切に行う

---

## 📚 学習リソース

### 書籍
- 「システムトレード 基本と原則」マイケル・コベル
- 「アルゴリズムトレーディング入門」アーニー・チャン
- 「Python for Finance」Yves Hilpisch

### オンラインリソース
- [Backtesting.py Documentation](https://kernc.github.io/backtesting.py/)
- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [Optuna Tutorial](https://optuna.org/)
- [MT5 Python Documentation](https://www.mql5.com/en/docs/python_metatrader5)

---

## 🎯 次のステップ

### クイックスタートガイド（教師なしクラスタリング方式）

#### ステップ1: 環境構築（Phase 0）
```bash
# プロジェクトディレクトリ作成
mkdir fx_trading_system
cd fx_trading_system

# 仮想環境作成
python -m venv venv
venv\Scripts\activate

# 必要なパッケージインストール
pip install pandas numpy xgboost scikit-learn matplotlib seaborn MetaTrader5 gym optuna backtesting joblib
```

#### ステップ2: データ収集（Phase 1の前半）
```python
# MT5からデータ取得
import MetaTrader5 as mt5
mt5.initialize()
data = mt5.copy_rates_range("USDJPY", mt5.TIMEFRAME_M15, ...)
```

#### ステップ3: クラスタリング実行（Phase 2）

**あなたの作業**:
1. ✅ 重要な特徴量を選択（config/feature_selection.py）
2. ⏸️ AIがクラスタリング実行（5分）
3. ✅ 各クラスタの特性を確認
4. ✅ 各クラスタに名前を付ける
5. ✅ トレード不可能なクラスタを除外

**AIの作業**:
- K-Meansクラスタリング
- クラスタ数の最適化（5-12個をテスト）
- クラスタ特性の分析レポート生成
- シルエットスコア計算

```python
from src.clustering.market_regime_detector import MarketRegimeDetector
from config.feature_selection import SELECTED_FEATURES

# 1. クラスタリング実行
detector = MarketRegimeDetector(n_clusters=7)
clusters = detector.fit_clusters(historical_data, SELECTED_FEATURES)

# 2. 分析
analysis = detector.analyze_clusters(historical_data, clusters)

# 3. あなたがラベル付け
cluster_labels = create_cluster_labels(detector)
```

#### ステップ4: RL訓練（Phase 3）

**AIの作業**（自動）:
```python
# 各クラスタでRLエージェントを訓練
agents, results = train_all_cluster_agents(
    data=historical_data,
    detector=detector,
    cluster_labels=cluster_labels,
    n_episodes=1000
)
```

**あなたの作業**:
- 訓練結果グラフを確認
- パフォーマンスが悪いクラスタを特定
- 必要に応じて報酬関数を調整

---

## 🔄 教師なしクラスタリング vs 従来型の比較

| 項目 | 教師なしクラスタリング | 従来型（シナリオ定義） |
|------|----------------------|---------------------|
| **パターン定義** | AIが自動発見 | 手動で定義 |
| **実装時間** | 短い（ラベリングのみ） | 長い（全ルール実装） |
| **精度上限** | データ依存（高い） | ルール依存（制限あり） |
| **新パターン対応** | 自動的に発見 | 手動で追加 |
| **メンテナンス** | 再クラスタリングのみ | ルール更新が必要 |
| **あなたの作業** | 特徴量選択＋ラベル付け | 全シナリオのルール実装 |
| **推奨度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 📊 作業分担の明確化

### あなたが行う作業（トレード知識が必要）

#### Phase 2: クラスタリング
- [ ] 重要な特徴量を選択（30-50個）
- [ ] クラスタ分析レポートを読む
- [ ] 各クラスタに意味のある名前を付ける
- [ ] トレード不可能なクラスタを特定

#### Phase 3: RL訓練
- [ ] 訓練結果グラフを確認
- [ ] パフォーマンスが悪いクラスタを分析
- [ ] 報酬関数のカスタマイズ（オプション）

#### Phase 4-5: 本番運用
- [ ] フォワードテスト結果の監視
- [ ] 定期的な再訓練（月1回）
- [ ] リスク管理パラメータの調整

### AIが行う作業（自動化）

#### Phase 2: クラスタリング
- ✅ K-Meansクラスタリング実行
- ✅ クラスタ数の最適化（エルボー法、シルエットスコア）
- ✅ クラスタ特性の自動分析
- ✅ バックテストによるクラスタ検証

#### Phase 3: RL訓練
- ✅ 環境構築（Gym）
- ✅ XGBoost Q-Learning実装
- ✅ 各クラスタでエージェント訓練（1000エピソード）
- ✅ 学習曲線の生成

#### Phase 4: バックテスト
- ✅ 統合システムのバックテスト実行
- ✅ パフォーマンスレポート生成

---

## 🎯 次のステップ

1. **Phase 0を完了する**
   - このロードマップを保存
   - 開発環境をセットアップ
   - プロジェクト構造を作成

2. **最初のコードを書く**
   - MT5からデータを取得するスクリプト
   - 簡単なテクニカル指標の計算

3. **小さく始めて徐々に拡大**
   - 最初は1つのシナリオだけ実装
   - 動作確認後、他のシナリオを追加

**重要**: 完璧を目指さず、まずは動くものを作る。その後、反復的に改善していく。

---

**作成者メモ**: このロードマップは実践的かつ段階的に進められるように設計されています。各フェーズを着実に完了させ、焦らず確実に進めてください。成功を祈っています！
