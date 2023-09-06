#import pandas as pd
#from datetime import datetime, timedelta
#
## CSVファイルを読み込む
#df1 = pd.read_csv('product_1.csv')  # 'import_csv.csv' はインポート用のCSV
#df2 = pd.read_csv('Book3.csv')  # 'latest_input.csv' は最終入庫日が含まれたCSV
#
## 最終入庫日をdatetimeオブジェクトとして解釈
#df2['Column15'] = pd.to_datetime(df2['Column15'])
#
## 1年前の日付を取得
#one_year_ago = datetime.now() - timedelta(days=365)
#
## 最終入庫日が1年以内の行を特定
#recent_input = df2[df2['Column15'] > one_year_ago]
#
## is_activeをTrueに更新
#df1.loc[df1['product_code'].isin(recent_input['Column3']), 'is_active'] = True
#
## 更新されたCSVを保存
#df1.to_csv('updated_import_csv.csv', index=False)

import pandas as pd
from datetime import datetime, timedelta

# CSVファイルを読み込む
df1 = pd.read_csv('product_1.csv')  
df2 = pd.read_csv('Book3.csv')

# 最終入庫日をdatetimeオブジェクトとして解釈
df2['Column15'] = pd.to_datetime(df2['Column15'], format='%Y%m%d', errors='coerce')


# 1年前の日付を取得
one_year_ago = datetime.now() - timedelta(days=365)

# is_activeカラムを作成
df2['is_active'] = df2['Column15'] > one_year_ago

merged_df = pd.merge(df1, df2, left_on='product_code', right_on='Column3', how='left')

# is_activeを更新
df1['is_active'] = merged_df['is_active_y']

# 更新されたCSVを保存
df1.to_csv('final_product_1.csv', index=False)