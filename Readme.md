# ポートフォリオの相関分析　
![alt text](sample_correlation_heatmap.png)

## 　使い方 

- ダウンロードしたら、まず保存したディレクトリに移動してください。 
- `input.txt`ファイルを開いて、`名称,wealthadvisorの銘柄ページのURL`の順で編集してください。 
  - 例:ｅＭＡＸＩＳ　Ｓｌｉｍ　米国株式（Ｓ＆Ｐ５００）,https://www.wealthadvisor.co.jp/FundData/SnapShot.do?fnc=2018070301
![alt text](example_input.png)

- config.pyファイルを開いて、月次データの開始年月と終了年月を指定してください。
![alt text](example_config.png)
- 準備ができたら`Python main.py`や`Python3 main.py`などで実行ください。 