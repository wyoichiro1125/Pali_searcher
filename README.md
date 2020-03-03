# Pali_searcher

- This system is for searching e-texts based on the PTS version.If you use the Chaṭṭha Saṅgāyana CD version, you may have trouble finding corresponding passages in the PTS texts. However, this system can (hopefully) save you some time, allowing you to search for the corresponding strings in the PTS versions.

- Please keep in mind that this system only uses e-texts inputted by the Dhammakaya Foundation and uploaded on GRETIL, which are the original format PTS texts. Consequently, this system has only a limited numbers of texts in comparison with the Chaṭṭha Saṅgāyana CD version. In addition, I cannot correct all the typos in the e-texts in themselves. Please take these factors into consideration when using this system.

---

# How to install and launch

- First, please download the system from the following address and unzip the file

- Second, please click “Pali_searcher(.exe)” in the unzipped folder. Please make sure you have an internet connection when installing, because the installation requires the system to download texts from GRETIL and create data to search the texts. This process will take few minutes. **Please do not interrupt the system while downloading texts**. When you get the message reading, “All texts have been installed”, please hit the Enter key on the black console and close the application.

- When you next launch Pali_searcher(.exe), you will be able to use Pali_searcher on your web browser. Because this application runs on your local server, you do not need to have an internet connection at this time.

- If you would like to terminate the system, please press the Ctrl & C keys at the same time on the console.

- If you have errors while searching, this likely means that the e-texts were not installed correctly. Please delete all files except for those with the extensions .css and .js in the static folder.

---


# Note on KH-transcription system


- If you can use KH-transcription system, just check “Use KH-transcription”. 

- However, when you use regular expressions (in Pali_searcher, you can use Python’s regex) with the KH-transcription system at the same time, **Pali_searcher gives priority to the KH-transcription**. For instance, if you input ¥S (meaning “any characters but space characters”) and check “Use KH-transcription”, it converts ¥S into ¥ṣ. If you would like to avoid this, you need to input Unicode characters like ā by yourself and check “Input Unicode characters by yourself” or just surround the parts you do not need to change with { }. Ex. {¥S}gacchatIti is converted into ¥Sgacchatīti when you check “Use KH-transcription”. The first ¥S remains unchanged, because it is surrounded by {}; on the other hand, the final “I” will be converted into “ī”.


(Watanabe Yoichiro)

* I am greatful to Dr. Max Brandstadt, who kindly checked my English.


---

# Pali_searcher

- PTS版のパーリ文献電子テキストを検索するためのツールです。
VRI版だと頁数・行数を数えるのにひと手間かかりますが、その手間が省けるようになっています。

- 但し、Gretil http://gretil.sub.uni-goettingen.de/gretil.html
に掲載された、Dhammakaya Foundation 入力版の判型を保った電子テキストのみに対応しているため網羅性は高くありません。
また電子テキスト自体のタイプミスも多分にあるものと思われますのであくまでも参考程度に利用していただけますと幸いです。

---

# ダウンロードの方法

- データを下記アドレスからダウンロードして解凍して下さい。
  - Windows: https://github.com/wyoichiro1125/Pali_searcher/raw/master/Pali_searcher(Windows).zip
  - Mac: https://github.com/wyoichiro1125/Pali_searcher/raw/master/Pali_searcher(mac).zip

- 解凍されたフォルダの内部にある Pali_searcher (.exe) をクリックして下さい。

- 初回立ち上げ時に、Gretil からテキストをダウンロードし、整形を行います。この際、インターネットにできていることを確認してください。
**終了まで数分かかります。この際、アプリケーションを途中で終了しないでください。**

- 検索用データのインストールが完了したメッセージが表示されたら、Enterキーを押してコンソールを閉じてください。もう一度 Pali_searcher(.exe) を起動すると、ブラウザ上で Pali_searcher が使用できます。

- 強制終了する場合には、黒いコンソール上で Ctrlキーと C キーを同時に押してください。

- 検索中にエラーが出た場合、検索用テキストが完全にインストールされていない可能性が最も高いものと思われます。.css ならびに .js の拡張子を持ったファイルをのぞいた static フォルダ内のデータを一度全て削除してからもう一度アプリケーションを実行してください。

---

# 検索方法

- 「Show line-changes」 を押すと元の電子テキストの改行を反映させた検索結果を出すことができます。

- KH転写方式で検索したい場合、「Use KH-transcription system」をチェックしてください。

- Pythonの正規表現に対応しています。しかし、**KH転写方式と重なった場合KH転写の方が優先されてしまうので注意して下さい**。例えば、\S は「空白文字以外」ではなく、\ṣ と変換されてしまいます。もしも正規表現を使用したい場合は、「Input Unicode characters by yourself」をチェックし、ṣ等を自分で入力していただくか、あるいはKH転写を適応しない部分を {} で囲んでください。例えば、{¥S}gacchati は、空白文字以外をその直前に有する gacchati を意味することになります（具体的には upasarga を伴う gacchati）。



（制作：渡邉要一郎）
