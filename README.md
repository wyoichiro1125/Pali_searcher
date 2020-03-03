




# Pali_searcher

- PTS版のパーリ文献電子テキストを検索するためのツールです。
VRI版だと頁数・行数を数えるのにひと手間かかりますが、その手間が省けるようになっています。

- 但し、Gretil http://gretil.sub.uni-goettingen.de/gretil.html
に掲載された、Dhammakaya Foundation 入力版の判型を保った電子テキストのみに対応しているため網羅性は高くありません。
また電子テキスト自体のタイプミスも多分にあるものと思われますのであくまでも参考程度に利用していただけますと幸いです。

---

#ダウンロードの方法

- データを下記アドレスからダウンロードして解凍して下さい。

Windows: https://github.com/wyoichiro1125/Pali_searcher/raw/master/Pali_searcher(Windows).zip

Mac: https://github.com/wyoichiro1125/Pali_searcher/raw/master/Pali_searcher(mac).zip

- 解凍されたフォルダの内部にある Pali_searcher (.exe) をクリックして下さい。

- 初回立ち上げ時に、Gretil からテキストをダウンロードし、整形を行います。この際、インターネットにできていることを確認してください。
**終了まで数分かかります。この際、アプリケーションを途中で終了しないでください。**

- 検索用データのインストールが完了したメッセージが表示されたら、Enterキーを押してコンソールを閉じてください。もう一度 Pali_searcher(.exe) を起動すると、ブラウザ上で Pali_searcher が使用できます。

- 強制終了する場合には、黒いコンソール上で Ctrlキーと C キーを同時に押してください。

---

#検索方法

- 「Show line-changes」 を押すと元の電子テキストの改行を反映させた検索結果を出すことができます。

- KH転写方式で検索したい場合、「Use KH-transcription system」をチェックしてください。

- Pythonの正規表現に対応しています。しかし、**KH転写方式と重なった場合KH転写の方が優先されてしまうので注意して下さい**。例えば、\S は「空白文字以外」ではなく、\ṣ と変換されてしまいます。もしも正規表現を使用したい場合は、「Input Unicode characters by yourself」をチェックしてください


---

# エラー時の対応について

エラーが出た場合、検索用テキストが完全にインストールされていない可能性が最も高いものと思われます。static フォルダ内のデータを一度全て削除してからもう一度アプリケーションを実行してください。


