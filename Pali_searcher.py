#!/usr/bin/python3
# coding: utf-8
from flask import Flask, make_response, request, render_template, session
from array import array
import io
import re
import csv
import os
import webbrowser
import threading
import sys


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

static = resource_path("static")

app = Flask(__name__, static_folder = resource_path("static"), template_folder=resource_path("templates"))


class Pali_text:
    __slots__ = ("name", "start_page", "end_page", "start_line", "end_line", "text")
    def __init__(self, name, start_page, start_line, end_page, end_line, text):
        self.name = name
        self.start_page = start_page
        self.end_page = end_page
        self.start_line = start_line
        self.end_line = end_line
        self.text = text
        
    def output(self):
        result = ""
        if self.name[:2] == "Ja":
            roman = ["I", "II", "III", "IV", "V", "VI"]
            self.name = self.name[:3] + roman[int(self.name[3]) - 1]
        if self.start_line == self.end_line:
            if self.start_page == 1:
                self.start_line -= 1
            result = """<span style="color:blue">""" + "{} {}.{}</span>: {}".format(self.name, self.start_page, self.start_line, self.text)
        elif self.start_page == self.end_page:
            if self.start_page == 1:
                self.start_line -= 1
                self.end_line -= 1
            result = """<span style="color:blue">"""+"{} {}.{}-{}</span>: {}".format(self.name, self.start_page, self.start_line, self.end_line, self.text)
        else:
            if self.start_page == 1:
                self.start_line -= 1
                self.end_line -= 1
            result = """<span style="color:blue">"""+"{} {}.{}-{}.{}</span>: {}".format(self.name, self.start_page, self.start_line, self.end_page, self.end_line, self.text)
        return result

def KH_changer(word):
    KH_list =  ["A", "I", "U", "M", "G", "J", "T", "D", "N", "z", "S"]
    NC_list = ["ā", "ī", "ū", "ṃ", "ṅ", "ñ", "ṭ", "ḍ", "ṇ", "ś", "ṣ"]
    result_word = ""
    for i in word:
        KH_match_flag = 0
        for j in range(len(KH_list)):
            if i == KH_list[j]:
                result_word += NC_list[j]
                KH_match_flag = 1
                break
        if KH_match_flag == 0:
            result_word += i
    return result_word

def opener(name, index, line, page):     
    #この関数の前に、中身が空の page, line, index array を作る必要があり
    index_bin =  static + "/" + name + "_index_.bin"
    line_bin =  static + "/" + name + "_page_.bin"
    page_bin =  static + "/" + name + "_line_.bin"
    # I made mistake when I named these bin files; I try to re-name here. 
    f1 = open(index_bin, "rb")
    try:
        index.fromfile(f1, 10**6)
    except EOFError:
        pass
    f1.close()
    f2 = open(line_bin, "rb")
    try:
        line.fromfile(f2, 10**6)
    except EOFError:
        pass
    f2.close()
    f3 = open(page_bin, "rb")
    try:
        page.fromfile(f3, 10**6)
    except EOFError:
        pass
    f3.close()
    data = open( static + "/" + name + "_.txt", "r", encoding="utf-8")
    text_for_search = data.read()
    return text_for_search

def Jataka_opener(number, index, line, page, start_point):
    name = "Ja_{}".format(number)
    index_bin =  static + "/" + name + "_index_.bin"
    line_bin =  static + "/" + name + "_line_.bin"
    page_bin =  static + "/" + name + "_page_.bin"
    start_bin =  static + "/" + "J_" + str(number) + "_start_point_.bin"
    # I made mistake when I named these bin files; I try to re-name here. 
    f1 = open(index_bin, "rb")
    try:
        index.fromfile(f1, 10**6)
    except EOFError:
        pass
    f1.close()
    f2 = open(line_bin, "rb")
    try:
        line.fromfile(f2, 10**6)
    except EOFError:
        pass
    f2.close()
    f3 = open(page_bin, "rb")
    try:
        page.fromfile(f3, 10**6)
    except EOFError:
        pass
    f3.close()
    f4 = open(start_bin, "rb")
    try:
        start_point.fromfile(f4, 1000)
    except EOFError:
        pass
    f4.close()

def Sn_opener(index, line, page, start_point):
    index_bin =  static + "/" + "Sn_index_.bin"
    line_bin =  static + "/" + "Sn_line_.bin"
    page_bin =  static + "/" + "Sn_page_.bin"
    start_bin =  static + "/" + "Sn_verse_start_point.bin"
    f1 = open(index_bin, "rb")
    try:
        index.fromfile(f1, 10**6)
    except EOFError:
        pass
    f1.close()
    f2 = open(line_bin, "rb")
    try:
        line.fromfile(f2, 10**6)
    except EOFError:
        pass
    f2.close()
    f3 = open(page_bin, "rb")
    try:
        page.fromfile(f3, 10**6)
    except EOFError:
        pass
    f3.close()
    f4 = open(start_bin, "rb")
    try:
        start_point.fromfile(f4, 1000)
    except EOFError:
        pass
    f4.close()

def Pali_word_searcher(s, text_for_search):
    matchs = re.finditer(s, text_for_search, re.IGNORECASE)
    li = [i.start() for i in matchs]
    return li

def Pali_pre_space(n, text, breakpoint={".", ":", "?", "!", "|", "@", ". ", ","}):#モノによっては breakpoint を適時変更してやる必要がある
    while n - 1 != 0 and not(text[n] in breakpoint):
        n = n - 1
    return n + 2 #コンマなどの後ろには基本半角スペースがあるため

def Pali_pos_space(n, text, breakpoint={".", ":", "?", "!", "|", "@", ". ", ","}):
    while (n+1 != len(text) - 1) and not(text[n] in breakpoint):
        n = n + 1
    return n + 1
    #この上で、どこまで出力するのかを決定する。あんまり長いとよくないので、いい感じにしないといけない。

def page_line_search(target, index, start_index):#start は、index[x] の x に相当する汎用インデックス番号を定める
    for i in range(start_index-1, len(index)):#このスタートは単純増加していく汎用インデックス番号
        try:
            index[i+1]
        except IndexError:
            return i
        if (index[i] <= target) and (index[i+1] > target):
            return i

def text_maker(word, BR="0", text_name="", break_point={".", ":", "?", "!", "|", "@", ". ", ","}):
    result = []
    index = array("I"); page = array("I"); line = array("I")
    text = opener(text_name, index, page, line)
    start_index = 0
    start_point_list = Pali_word_searcher(word, text)
    for start_point in start_point_list:
        if text_name:#あとで Apadanaの場合などに関して場合分けを考える
            sentence_start = Pali_pre_space(start_point, text, break_point)
            sentence_end = Pali_pos_space(start_point, text, break_point)
            start_index = page_line_search(sentence_start, index, start_index)
            end_index = page_line_search(sentence_end, index, start_index)
            searched_text = text[sentence_start: sentence_end]
            if BR == "1":
                new_searched_text = ""
                edges = [index[k] - sentence_start 
                         for k in range(start_index, end_index+1) 
                         if index[k] - sentence_start != 0]
                for j in range(len(searched_text)):
                    if j in edges:
                        new_searched_text +=  ("<BR>" + searched_text[j])
                    else:
                        new_searched_text += searched_text[j]
                new_searched_text = re.sub(r"(?<=\S)<BR>", "-<BR>", new_searched_text)
                searched_text = new_searched_text
        searched_text = searched_text.replace("@", " . . . ")
        spaned = re.compile(r"(" + word + ")", re.IGNORECASE)
        searched_text = re.sub(spaned, """<span style="color:red">"""+ r"\1" +"</span>", searched_text)    
        result.append(
                Pali_text(text_name, page[start_index], line[start_index], page[end_index], line[end_index], searched_text)
            )
    return result
    
def verse_text_searcher(text_name, searched):
    spaned = re.compile(r"(" + searched + ")", re.IGNORECASE)
    csvfile = open(  static + "/" + text_name + "_.csv", "r", encoding="utf-8", newline="\n")
    lines = csv.reader(csvfile, delimiter=",", skipinitialspace=True)
    result = ['<span style="color:blue">' + line[0] +"</span>: " 
        + re.sub(spaned, 
        """<span style="color:red">"""+ r"\1" +"</span>"
        , line[1].lstrip().rstrip()) + "<BR>"
        for line in lines 
        if re.search(searched, re.sub(r"\*\d\d?|<BR>|<br>", "", line[1]), re.IGNORECASE)
            ]
    csvfile.close()
    return result

def Th_searcher(text, searched):
    if text == "Th":
        csvfile = open( static + "/" + "Thera_.csv", "r", encoding="utf-8", newline="\n")
    else:
        csvfile = open( static + "/" + "Theri_.csv", "r", encoding="utf-8", newline="\n")
    lines = csv.reader(csvfile, skipinitialspace=True)
    spaned = re.compile(r"(" + searched + ")", re.IGNORECASE)
    result = [
        '<span style="color:blue">' + 
        re.sub(r"(.*?\|\|)(.*?)(\|\|)", r"\2", line[0]) + "</span>: " + re.sub(spaned, """<span style="color:red">"""+ r"\1" + "</span>", 
        re.sub(r"(.*?\|\|)(.*?)(\|\|)", r"\1", line[0]).lstrip().rstrip()) 
        + "<BR>"
        for line in lines
        if re.search(searched, re.sub(r"\*\d\d?|<BR>|<br>", "", line[0]), re.IGNORECASE)
        ]
    csvfile.close()
    return result

    

@app.route('/')
def form():
    return """
<!DOCTYPE html>
        <html lang=ja>
            <body>
            <title>試製PTS版パーリテキスト検索システム</title>
            <p1>試製PTS版パーリテキスト検索システム</p1><br>
                <form action="/result" method="post" enctype="cgi-bin/abc.cgi"><br>
                    <input type="text" name="word" /><br>
			<input type="radio" name="KH" value="1">KH方式を使用 
			<input type="radio" name="KH" value="0" checked = "checked">KH方式を使用しない<br>
		<input type="radio" name="BR" value="1">改行を反映する
		<input type="radio" name="BR" value="0" checked = "checked">改行を反映しない<br><br>
テキストを選択してください <input type="checkbox" id="all_texts" />all texts<br><br>


<label><input type="checkbox" name="text" value="Vin"/>Vin<br>

<label><input type="checkbox" name="text" class="Sutt" value="DN"/>DN
<label><input type="checkbox" name="text" class="Sutt" value="MN"/>MN
<label><input type="checkbox" name="text" class = "Sutt" value="SN"/>SN
<label><input type="checkbox" name="text" class = "Sutt" value="AN"/>AN
<input type="checkbox" id="sutta_all" />all<br>


<label><input type="checkbox" name="text" class="Ku" value="Khp"/>Khp
<label><input type="checkbox" name="text" class="Ku" value="Dhp"/>Dhp 
<label><input type="checkbox" name="text" class="Ku" value="Ud"/>Ud
<label><input type="checkbox" name="text" class="Ku" value="It"/>It
<label><input type="checkbox" name="text" class="Ku" value="Sn"/>Sn
<label><input type="checkbox" name="text" class="Ku" value="Pv"/>Pv 
<label><input type="checkbox" name="text" class="Ku" value="Vm"/>Vv
<label><input type="checkbox" name="text" class="Ku" value="Th"/>Th
<label><input type="checkbox" name="text" class="Ku" value="Thi"/>Thi
<label><input type="checkbox" name="text" class="Ku" value="J"/>J
<label><input type="checkbox" name="text" class="Ku" value="Nidd_I"/>Nidd I
<label><input type="checkbox" name="text" class="Ku" value="Nidd_II"/>Nidd II
<label><input type="checkbox" name="text" class="Ku" value="Paṭis"/>Paṭis
<label><input type="checkbox" name="text" class="Ku" value="Ap"/>Ap
<label><input type="checkbox" name="text" class="Ku" value="Bv"/>Bv
<label><input type="checkbox" name="text" class="Ku" value="Cp"/>Cp 
<input type="checkbox" id="ku_all" />all<br>


<label><input type="checkbox" name="text" class="abhi" value="Dhs"/>Dhs
<label><input type="checkbox" name="text" class="abhi" value="Vibh"/>Vibh
<label><input type="checkbox" name="text" class="abhi" value="Dhātuk"/>Dhātuk
<label><input type="checkbox" name="text" class="abhi" value="Pugg"/>Pugg
<label><input type="checkbox" name="text" class="abhi" value="Kv"/>Kv
<label><input type="checkbox" name="text" class="abhi" value="Yam"/>Yam
<input type="checkbox" id="abhi_all" />all
<br>

<label><input type="checkbox" name="text" class="other" value="Mil"/>Mil
<label><input type="checkbox" name="text" class="other" value="Vism"/>Vism
<label><input type="checkbox" name="text" class="other" value="Sp"/>Sp
<label><input type="checkbox" name="text" class="other" value="Ja"/>Ja
<input type="checkbox" id="other_all" />all
<br>
                    <input type="submit" />
                </form>
        <script type="text/javascript">
            var checkall = document.getElementById('all_texts');
            checkall.addEventListener('click', function () {
                var checkboxes = document.getElementsByName('text');
                for (i in checkboxes) {
                    checkboxes[i].checked = this.checked;
                }
            });
            var checkall1 = document.getElementById('sutta_all');
            checkall1.addEventListener('click', function () {
                var checkboxes = document.getElementsByClassName('Sutt');
                for (i in checkboxes) {
                    checkboxes[i].checked = this.checked;
                }
            });
            var checkall2 = document.getElementById('ku_all');
            checkall2.addEventListener('click', function () {
                var checkboxes = document.getElementsByClassName('Ku');
                for (i in checkboxes) {
                    checkboxes[i].checked = this.checked;
                }
            });
            var checkall3 = document.getElementById('abhi_all');
            checkall3.addEventListener('click', function () {
                var checkboxes = document.getElementsByClassName('abhi');
                for (i in checkboxes) {
                    checkboxes[i].checked = this.checked;
                }
            });
            var checkall4 = document.getElementById('other_all');
            checkall4.addEventListener('click', function () {
                var checkboxes = document.getElementsByClassName('other');
                for (i in checkboxes) {
                    checkboxes[i].checked = this.checked;
                }
            });
        </script>
<br>
<br>

*電子テキストは全て GRETIL - Göttingen Register of Electronic Texts in Indian Languages（http://gretil.sub.uni-goettingen.de/gretil.html）
に公開されている Dhammakaya Foundation により入力された PTS 版を元にしています。<br>

**これはβ版です。不具合がありましたら渡邉までご報告いただけると幸いです。<br>
<br>

製作：渡邉要一郎



            </body>
        </html>
    """

@app.route('/result', methods=["POST"])
def result_view():
    results = []; text_list = []
    searched = str(request.form["word"])
    if not searched:
        return "No result"
    if str(request.form["KH"]) == "1":
        searched = KH_changer(searched)
    try:
        re.compile(searched)
    except Exception:
        return "Regex Error!"
    BR = str(request.form["BR"])
    cheaklist = request.form.getlist("text")

    text_order = ["Vin_I", "Vin_II", "Vin_III", "Vin_IV", "Vin_V", 
    "DN_I", "DN_II", "DN_III",
    "MN_I", "MN_II", "MN_III",
    "SN_I", "SN_II", "SN_III", "SN_IV", "SN_V",
    "AN_I", "AN_II", "AN_III", "AN_IV", "AN_V",
    "Khp", "Dhp", "Ud", "It", "Sn", "Pv", "Vm", "Th", "Thi", "J", "Nidd_I", "Nidd_II", "Paṭis_I", "Paṭis_II", "Ap", "Bv", "Cp",
    "Dhs", "Vibh", "Dhātuk", "Pugg", "Kv", "Yam_I", "Yam_II", "Mil", "Vism", "Sp", "Ja_1", "Ja_2", "Ja_3", "Ja_4", "Ja_5", "Ja_6"]
    
    #テキストリストを開く
    text_list = []
    for text in cheaklist:
        if text == "Vin":
            text_list += ["Vin_I", "Vin_II", "Vin_III", "Vin_IV", "Vin_V"]
        elif text == "DN":
            text_list += ["DN_I", "DN_II", "DN_III"]
        elif text == "MN":
            text_list += ["MN_I", "MN_II", "MN_III"]
        elif text == "SN":
            text_list += ["SN_I", "SN_II", "SN_III", "SN_IV", "SN_V"]
        elif text == "AN":
            text_list += ["AN_I", "AN_II", "AN_III", "AN_IV", "AN_V"]
        elif text == "Paṭis":
            text_list += ["Paṭis_I", "Paṭis_II"]
        elif text == "Yam":
            text_list += ["Yam_I", "Yam_II"]
        elif text == "Ja":
            text_list += ["Ja_1", "Ja_2", "Ja_3", "Ja_4", "Ja_5", "Ja_6"]
        else:
            text_list.append(text)

    text_list.sort(key = lambda x: text_order.index(x))
    
    for text in text_list:
        if text == "J":
            result = []
            for num in range(1, 7):
                page = array("I"); line_start = array("I"); index = array("I"); verse_start_point = array("I")
                Jataka_opener(num, index, line_start, page, verse_start_point)
                roman_number = ["I", "II", "III", "IV", "V", "VI"]
                csvfile = open(  static + "/" + "J_{}.csv".format(num), "r", encoding = "utf-8", newline="\n")
                lines = csv.reader(csvfile, delimiter=",", skipinitialspace=True)
                i = 0
                start_index = 0
                for line in lines:    
                    if re.search(searched, line[0]):
                        try:
                            start = verse_start_point[i]
                        except IndexError:
                            break
                        end = start + len(line[0])
                        start_index = page_line_search(start, index, start_index)
                        end_index = page_line_search(end, index, start_index)
                        searched_text = line[0]
                        new_text = ""
                        if BR == "1":
                            edges = [index[k] - verse_start_point[i] 
                             for k in range(start_index, end_index+1) 
                             if index[k] - verse_start_point[i] != 0]
                            for j in range(len(searched_text)):
                                if j in edges:
                                    new_text +=  ("<BR>" + searched_text[j])
                                else:
                                    new_text += searched_text[j]
                        else:
                            new_text = line[0]
                        searched_text = re.sub(r"(?<=\S)<BR>", "-<BR>", new_text)
                        searched_text = searched_text.replace("@", " . . . ")
                        spaned = re.compile(r"(" + searched + ")", re.IGNORECASE)
                        searched_text = re.sub(spaned, """<span style="color:red">"""+ r"\1" +"</span>", searched_text)
                        new_set = Pali_text("J_{}".format(roman_number[num-1]), page[start_index], line_start[start_index], page[end_index], line_start[end_index], searched_text)
                        result.append(new_set.output() + "<BR>")
                    i += 1
            results += result
        elif text == "Ap":
            pre_result = text_maker(searched, BR, text, break_point={"~"})
            results += [re.sub(r"~", "", item.output() + "<BR>") for item in pre_result]
        elif text == "Sn":
            result = []
            line_start = array("I"); index = array("I"); verse_start_point = array("I"); page = array("I")
            Sn_opener(index, line_start, page, verse_start_point)
            csvfile = open(  static + "/" + "Sn_verse.csv", "r", encoding = "utf-8", newline="\n")
            lines = csv.reader(csvfile, delimiter=",", skipinitialspace=True)
            i = 0
            start_index = 0
            for line in lines:    
                if re.search(searched, line[0]):    
                    try:
                        start = verse_start_point[i]
                    except IndexError:
                        break
                    end = start + len(line[0])
                    start_index = page_line_search(start, index, start_index)
                    end_index = page_line_search(end, index, start_index)
                    searched_text = line[0]
                    new_text = ""
                    if BR == "1":
                        edges = [index[k] - verse_start_point[i] 
                             for k in range(start_index, end_index+1) 
                             if index[k] - verse_start_point[i] != 0]
                        for j in range(len(searched_text)):
                            if j in edges:
                                new_text +=  ("<BR>" + searched_text[j])
                            else:
                                new_text += searched_text[j]
                    else:
                        new_text = line[0]
                    searched_text = re.sub(r"(?<=\S)<BR>", "-<BR>", new_text)
                    searched_text = searched_text.replace("@", " . . . ")
                    spaned = re.compile(r"(" + searched + ")", re.IGNORECASE)
                    searched_text = re.sub(spaned, """<span style="color:red">"""+ r"\1" +"</span>", searched_text)
                    new_set = Pali_text("Sn", page[start_index], line_start[start_index], page[end_index], line_start[end_index], searched_text)
                    result.append(new_set)
                i += 1
            #ここから散文の方の検索；最後に全体をまとめてソートし、完成
            csvfile.close()
            pre_result = text_maker(searched, BR, "Sn")
            result += pre_result
            result.sort(key = lambda x: (x.start_page, x.start_line))
            results += [item.output() + "<BR>" for item in result]

        elif text in {"Dhp", "Cp", "Bv", "Vm", "Pv"}:
            results += verse_text_searcher(text, searched)
        elif text in {"Th", "Thi"}:
            results += Th_searcher(text, searched)
        else:
            pre_result = text_maker(searched, BR, text)
            results += [item.output() + "<BR>" for item in pre_result]
    if results == []:
        return "No result"
    result_text = ""
    for i in range(len(results)):
        if i >= 1 and results[i] != results[i - 1]:
            result_text += results[i]
#    return result_text
    return render_template('user.html', result = result_text)

if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port=5000, debug=False)
    # if debug = True, the webbrowser will open twice.
# $ pyinstaller Pali_searcher.py -F --add-data "./templates/*:templates" --add-data "./static/*:static"
# If you use Windows, change "/*:" > "/*;"
