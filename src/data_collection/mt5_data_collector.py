import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import os
import json

class MT5DataCollector:
    """MT5からデータ収集を行なうクラス"""
    def __init__(self, data_dir="data/raw", mt5_path=None):
        """
        初期化
        data_dir: データ保存ディレクトリ
        mt5_path: MT5のインストールパス（オプション）
        """
        self.data_dir = data_dir
        self.mt5_path = mt5_path
        os.makedirs(data_dir, exist_ok=True)

    def initialize_mt5(self):
        """MT5の初期化（パス指定対応）"""
        try:
            # MT5パスが指定されている場合
            if self.mt5_path:
                print(f"🔍 MT5パス指定: {self.mt5_path}")
                if not mt5.initialize(path=self.mt5_path):
                    print(f"❌ MT5の初期化に失敗 (指定パス: {self.mt5_path})")
                    return False
            else:
                # デフォルトパスでMT5を探す
                if not mt5.initialize():
                    print("❌ MT5の初期化に失敗")
                    print("💡 MT5が見つからない場合は、パスを指定してください")
                    return False
            
            print("✅ MT5初期化成功")
            
            # MT5の基本情報表示
            terminal_info = mt5.terminal_info()
            if terminal_info:
                print(f"   MT5パス: {terminal_info.path}")
                print(f"   会社: {terminal_info.company}")
                print(f"   ビルド: {terminal_info.build}")
                print(f"   接続状態: {'接続中' if terminal_info.connected else '未接続'}")
            
            return True
            
        except Exception as e:
            print(f"❌ MT5初期化エラー: {e}")
            return False
    
    def get_sample_data(self,symbol="GOLD",timeframe=mt5.TIMEFRAME_M15,count=1000):
        """サンプルデータの取得
        symbol:通貨ペア
        timeframe:時間足
        count:取得件数
        """
        print(f"{symbol}M15データ取得開始")
    
        try:
            rates = mt5.copy_rates_from_pos(symbol,timeframe,0,count)

            if rates is None:
                print(f"{symbol}データ取得失敗")
                return None
        
            df = pd.DataFrame(rates)
            df['datetime'] = pd.to_datetime(df['time'],unit='s')

            print(f"✅ {symbol} データ取得成功: {len(df)}件")
            print(f"   期間: {df['datetime'].iloc[0]} ～ {df['datetime'].iloc[-1]}")

            return df
    
        except Exception as e:
            print(f"❌ エラー: {e}")
            return None
    def save_sample_data(self,df,symbol="GOLD",timeframe="M15"):
        """サンプルデータの保存"""
        if df is None:
            return False
        try:
            #ファイル名生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_{timeframe}_sample_{timestamp}.csv"
            filepath = os.path.join(self.data_dir, filename)

            #CSV保存
            df.to_csv(filepath, index=False)
            print(f"データ保存完了:{filepath}")

            #メタデータ保存
            metadata = {
                'symbol':symbol,
                'timeframe':timeframe,
                'count':len(df),
                'start_time':df['datetime'].iloc[0].strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': df['datetime'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'created_at': timestamp
            }
            meta_filename = f"{symbol}_{timeframe}_sample_{timestamp}_meta.json"
            meta_filepath = os.path.join(self.data_dir,meta_filename)

            with open(meta_filepath,'w')as f:
                json.dump(metadata,f,indent=2)  
            return filepath
        except Exception as e:
            print(f"保存エラー:{e}")
            return False

    def data_quality_check(self, df):
        """データ品質チェック"""
        print("\n🔍 データ品質チェック:")
        
        # 基本統計
        print(f"   データ件数: {len(df)}")
        print(f"   欠損値: {df.isnull().sum().sum()}")
        print(f"   重複値: {df.duplicated().sum()}")
        
        # 価格データの異常値チェック
        price_cols = ['open', 'high', 'low', 'close']
        for col in price_cols:
            if col in df.columns:
                q99 = df[col].quantile(0.99)
                q01 = df[col].quantile(0.01)
                outliers = ((df[col] > q99) | (df[col] < q01)).sum()
                print(f"   {col} 外れ値: {outliers}件")
        
        # 時間の連続性チェック
        time_diff = df['datetime'].diff().dropna()
        expected_diff = pd.Timedelta(minutes=15)  # M15の場合
        irregular_intervals = (time_diff != expected_diff).sum()
        print(f"   時間間隔の異常: {irregular_intervals}件")
        
        print("✅ データ品質チェック完了\n")
        
        return {
            'total_count': len(df),
            'missing_values': df.isnull().sum().sum(),
            'duplicates': df.duplicated().sum(),
            'irregular_intervals': irregular_intervals
        }
    
    def cleanup(self):
        """MT5接続クリーンアップ"""
        mt5.shutdown()
        print("🔄 MT5接続終了")

def main():
    """メイン実行"""
    print("🚀 ノートPC用データ収集開始")
    print("=" * 50)
    
    # MT5パスを指定してデータコレクター初期化
    mt5_path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
    collector = MT5DataCollector(mt5_path=mt5_path)
    
    try:
        # MT5初期化
        if not collector.initialize_mt5():
            print("\n💡 MT5初期化に失敗した場合の確認事項:")
            print("1. MT5がインストールされているか")
            print("2. MT5が起動しているか") 
            print("3. デモ口座またはライブ口座にログインしているか")
            print("4. パスが正しいか確認してください")
            return
        
        # サンプルデータ取得（複数銘柄）
        symbols = ["GOLD", "USDJPY", "EURJPY"]  # 金・主要円ペア
        
        for symbol in symbols:
            print(f"\n📈 {symbol} 処理中...")
            
            # データ取得
            df = collector.get_sample_data(symbol=symbol, count=1000)
            
            if df is not None:
                # データ品質チェック
                quality = collector.data_quality_check(df)
                
                # データ保存
                filepath = collector.save_sample_data(df, symbol=symbol)
                
                if filepath:
                    print(f"✅ {symbol} 完了")
                    print(f"   ファイル: {filepath}")
                else:
                    print(f"❌ {symbol} 保存失敗")
            else:
                print(f"❌ {symbol} データ取得失敗")
                print(f"   {symbol} が利用可能か確認してください")
        
        print("\n🎉 データ収集完了！")
        print("📁 保存先: data/raw/ フォルダを確認してください")
        print("🔄 次のステップ: テクニカル指標の実装")
        
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # クリーンアップ
        collector.cleanup()

if __name__ == "__main__":
    main()
