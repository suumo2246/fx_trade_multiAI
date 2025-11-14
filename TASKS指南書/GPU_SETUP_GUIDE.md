# 🖥️ GPU環境セットアップガイド

## 📋 前提条件

### ハードウェア要件
- **NVIDIA GPU**: GTX 1060 6GB以上推奨（FX取引では RTX 3060 12GB以上が理想）
- **システムメモリ**: 16GB以上推奨
- **ストレージ**: SSD 100GB以上の空き容量

### ソフトウェア要件
- **Windows 10/11** または **Linux (Ubuntu 20.04+)**
- **Python 3.8-3.11** (3.12は一部ライブラリで非対応)

## 🔧 ステップ1: NVIDIA環境の準備

### 1.1 NVIDIA Driverのインストール
```bash
# 現在のドライバーバージョン確認
nvidia-smi
```

最新版をダウンロード: [NVIDIA Driver Downloads](https://www.nvidia.com/Download/index.aspx)

### 1.2 CUDA Toolkit のインストール
CUDA 11.8 または 12.x を推奨

**Windows:**
1. [CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive) から CUDA 11.8 をダウンロード
2. インストール後、環境変数を確認:
```cmd
nvcc --version
```

**Linux:**
```bash
# CUDA 11.8 の場合
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run
```

### 1.3 cuDNN のインストール
1. [cuDNN Archive](https://developer.nvidia.com/cudnn-archive) からダウンロード
2. CUDA フォルダに展開

## 🚀 ステップ2: GPU対応Pythonライブラリのインストール

### 2.1 基本セットアップ
```bash
# 仮想環境作成・有効化
python -m venv venv_gpu
# Windows
venv_gpu\Scripts\activate
# Linux
source venv_gpu/bin/activate

# pip アップグレード
pip install --upgrade pip setuptools wheel
```

### 2.2 PyTorch (CUDA対応版) インストール
```bash
# CUDA 11.8 の場合
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1 の場合
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CPU版（比較用）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 2.3 基本GPU対応ライブラリ
```bash
# 機械学習（GPU対応）
pip install xgboost lightgbm catboost

# GPU監視ツール
pip install nvidia-ml-py3 gpustat pynvml

# その他GPU対応ライブラリ
pip install cupy-cuda11x  # CUDA 11.x用
# pip install cupy-cuda12x  # CUDA 12.x用
```

### 2.4 FX特化ライブラリ
```bash
# テクニカル分析
pip install pandas numpy matplotlib seaborn
pip install ta finta mplfinance>=0.12.7a0
pip install backtesting

# 時系列分析（GPU対応）
pip install darts neuralprophet

# 強化学習
pip install stable-baselines3 ray[rllib]
```

### 2.5 RAPIDS (オプション・Linux推奨)
```bash
# Conda環境でのみ推奨
conda install -c rapidsai -c nvidia -c conda-forge \
    cudf=23.10 cuml=23.10 cugraph=23.10 cuspatial=23.10 \
    python=3.10 cudatoolkit=11.8
```

## ✅ ステップ3: GPU環境の確認

### 3.1 GPU認識テスト
```python
# gpu_check.py
import torch
import nvidia_ml_py3 as nvml

def check_gpu_environment():
    print("🔍 GPU環境チェック")
    print("=" * 50)
    
    # CUDA利用可能性
    print(f"CUDA利用可能: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA バージョン: {torch.version.cuda}")
        print(f"GPU デバイス数: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
            print(f"GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
        
        # メモリ使用状況
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            allocated = torch.cuda.memory_allocated() / 1024**3
            reserved = torch.cuda.memory_reserved() / 1024**3
            print(f"GPU メモリ使用量: {allocated:.2f} GB / {reserved:.2f} GB")
    
    # NVIDIA-ML確認
    try:
        nvml.nvmlInit()
        driver_version = nvml.nvmlSystemGetDriverVersion()
        print(f"NVIDIA Driver: {driver_version}")
        
        device_count = nvml.nvmlDeviceGetCount()
        for i in range(device_count):
            handle = nvml.nvmlDeviceGetHandleByIndex(i)
            info = nvml.nvmlDeviceGetMemoryInfo(handle)
            name = nvml.nvmlDeviceGetName(handle)
            print(f"GPU {i}: {name.decode()} - Memory: {info.used/1024**3:.2f}/{info.total/1024**3:.2f} GB")
    
    except Exception as e:
        print(f"NVIDIA-ML エラー: {e}")

def test_gpu_computation():
    print("\n🧮 GPU計算テスト")
    print("=" * 50)
    
    if torch.cuda.is_available():
        device = torch.device('cuda')
        
        # 簡単な行列演算
        import time
        size = 5000
        
        # CPU
        start = time.time()
        a_cpu = torch.randn(size, size)
        b_cpu = torch.randn(size, size)
        c_cpu = torch.matmul(a_cpu, b_cpu)
        cpu_time = time.time() - start
        
        # GPU
        start = time.time()
        a_gpu = torch.randn(size, size, device=device)
        b_gpu = torch.randn(size, size, device=device)
        c_gpu = torch.matmul(a_gpu, b_gpu)
        torch.cuda.synchronize()
        gpu_time = time.time() - start
        
        print(f"CPU計算時間: {cpu_time:.3f}秒")
        print(f"GPU計算時間: {gpu_time:.3f}秒")
        print(f"GPU加速比: {cpu_time/gpu_time:.1f}倍")
    else:
        print("❌ CUDA が利用できません")

if __name__ == "__main__":
    check_gpu_environment()
    test_gpu_computation()
```

### 3.2 機械学習ライブラリのGPUテスト
```python
# gpu_ml_test.py
def test_xgboost_gpu():
    try:
        import xgboost as xgb
        print("✅ XGBoost GPU対応テスト")
        
        # サンプルデータ
        from sklearn.datasets import make_classification
        X, y = make_classification(n_samples=10000, n_features=20, random_state=42)
        
        # GPU版
        model = xgb.XGBClassifier(
            tree_method='gpu_hist',
            gpu_id=0,
            n_estimators=100
        )
        model.fit(X, y)
        print("✅ XGBoost GPU学習成功")
    except Exception as e:
        print(f"❌ XGBoost GPU エラー: {e}")

def test_lightgbm_gpu():
    try:
        import lightgbm as lgb
        print("✅ LightGBM GPU対応テスト")
        
        from sklearn.datasets import make_classification
        X, y = make_classification(n_samples=10000, n_features=20, random_state=42)
        
        # GPU版
        model = lgb.LGBMClassifier(
            device='gpu',
            gpu_platform_id=0,
            gpu_device_id=0,
            n_estimators=100
        )
        model.fit(X, y)
        print("✅ LightGBM GPU学習成功")
    except Exception as e:
        print(f"❌ LightGBM GPU エラー: {e}")

if __name__ == "__main__":
    test_xgboost_gpu()
    test_lightgbm_gpu()
```

## ⚙️ FX取引での GPU活用例

### 4.1 リアルタイム特徴量計算
```python
import cupy as cp  # GPU版NumPy
import cudf as cdf  # GPU版Pandas

# GPU での高速テクニカル指標計算
def gpu_calculate_ema(prices, period=9):
    prices_gpu = cp.asarray(prices)
    alpha = 2.0 / (period + 1)
    ema = cp.zeros_like(prices_gpu)
    ema[0] = prices_gpu[0]
    
    for i in range(1, len(prices_gpu)):
        ema[i] = alpha * prices_gpu[i] + (1 - alpha) * ema[i-1]
    
    return cp.asnumpy(ema)
```

### 4.2 大規模バックテスト
```python
# 複数シナリオ並列実行
import ray

@ray.remote(num_gpus=0.25)  # GPU分割使用
def gpu_backtest_scenario(scenario_params, data):
    # シナリオ別バックテスト実行
    return run_backtest_gpu(scenario_params, data)

# 並列実行
futures = []
for scenario in scenario_list:
    future = gpu_backtest_scenario.remote(scenario, market_data)
    futures.append(future)

results = ray.get(futures)
```

## 🚨 トラブルシューティング

### よくあるエラー

**1. CUDA メモリ不足**
```python
# メモリクリア
torch.cuda.empty_cache()

# バッチサイズ調整
batch_size = 1024 if torch.cuda.get_device_properties(0).total_memory > 8e9 else 512
```

**2. CUDA バージョン不整合**
```bash
# 現在の環境確認
python -c "import torch; print(torch.version.cuda)"
nvcc --version

# PyTorch再インストール
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**3. ライブラリのGPU認識失敗**
```bash
# 環境変数設定（Windows）
set CUDA_PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8

# 環境変数設定（Linux）
export CUDA_HOME=/usr/local/cuda-11.8
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

## 📊 パフォーマンス最適化

### GPU使用量監視
```bash
# リアルタイム監視
watch -n 1 nvidia-smi

# Python から監視
gpustat -i 1
```

### メモリ使用量最適化
```python
# モデル訓練時の設定
import os
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'

# 混合精度訓練（メモリ削減）
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
with autocast():
    output = model(input)
    loss = criterion(output, target)
```

これでGPU環境が構築できたら、FX自動トレードシステムで大幅な高速化を実現できます！