#!/usr/bin/python3
# coding: utf-8

import re
from array import array
import csv
import requests
import sys
import os
import functools
from concurrent import futures

#やること
#ダウンロードを行う
#普通のテキストの整形
#韻文テキストの整形
#Sp など、複数のテキストを一緒にしなければいけない場合の処理
#並行処理（時間がかかるので）


static_path = os.getcwd() + "/static/"
text_list = ["Vin_I.txt", "Vin_II.txt", "Vin_III.txt", "Vin_IV.txt", "Vin_V.txt",
         "DN_I.txt", "DN_II.txt", "DN_III.txt",
         "MN_I.txt", "MN_II.txt", "MN_III.txt",
         "AN_I.txt", "AN_II.txt", "AN_III.txt", "AN_IV.txt", "AN_V.txt",
         "SN_I.txt", "SN_II.txt", "SN_III.txt", "SN_IV.txt", "SN_V.txt",
          "Khp.txt", "Ud.txt", "It.txt", "Nidd_I.txt", "Nidd_II.txt", "Khp.txt",
          "Dhātuk.txt", "Yam_I.txt", "Yam_II.txt", "Kv.txt", "Pugg.txt", "Paṭis_I.txt", "Paṭis_II.txt", 
           "Vibh.txt","Dhs.txt", "Mil.txt", "Vism.txt"]
text_dict = {"Vin_I.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/1_vin/vin3s1ou.htm", 
"Vin_II.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/1_vin/vin4s2ou.htm", 
"Vin_III.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/1_vin/vin1maou.htm", 
"Vin_IV.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/1_vin/vin2cuou.htm", 
"Vin_V.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/1_vin/vin5paou.htm",
         "DN_I.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/1_digh/dighn1ou.htm",
          "DN_II.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/1_digh/dighn2ou.htm", 
          "DN_III.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/1_digh/dighn2ou.htm",
         "MN_I.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/2_majjh/majjn1ou.htm", 
         "MN_II.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/2_majjh/majjn2ou.htm", 
         "MN_III.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/2_majjh/majjn3ou.htm",
         "AN_I.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/4_angu/angut1ou.htm", 
         "AN_II.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/4_angu/angut2ou.htm", 
         "AN_III.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/4_angu/angut3ou.htm", 
         "AN_IV.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/4_angu/angut4ou.htm", 
         "AN_V.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/4_angu/angut5ou.htm",
         "SN_I.txt":"http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/3_samyu/samyu1ou.htm", 
         "SN_II.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/3_samyu/samyu2ou.htm", 
         "SN_III.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/3_samyu/samyu3ou.htm", 
         "SN_IV.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/3_samyu/samyu4ou.htm", 
         "SN_V.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/3_samyu/samyu2ou.htm",
         "Ap.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/apadanou.htm", 
         "Khp.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/khudp_ou.htm", 
         "Dhp.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/dhampdou.htm",
         "Sn.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/sutnipou.htm",
         "Ud.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/udana_ou.htm", 
         "It.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/itivutou.htm", 
         "Vm.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/vimvatou.htm",
         "Pv.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/petvatou.htm",
         "Th.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/theragou.htm",
         "Thi.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/therigou.htm",
         "Nidd_I.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/nidde1ou.htm", 
         "Nidd_II.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/nidde2ou.htm",
         "Bv.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/budvmsou.htm",
         "Cp.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/carpitou.htm",
         "Ja_1.txt":"http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/jatak1ou.htm",
         "Ja_2.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/jatak2ou.htm",
         "Ja_3.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/jatak3ou.htm",
         "Ja_4.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/jatak4ou.htm",
         "Ja_5.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/jatak5ou.htm",
         "Ja_6.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/jatak6ou.htm",
          "Dhātuk.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/3_abh/dhatukou.htm", 
          "Yam_I.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/3_abh/yamak_1ou.htm", 
          "Yam_II.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/3_abh/yamak_2ou.htm", 
          "Kv.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/3_abh/kathavou.htm", 
          "Pugg.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/3_abh/pugpan_ou.htm", 
          "Paṭis_I.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/patis1ou.htm", 
          "Paṭis_II.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/patis2ou.htm", 
           "Vibh.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/3_abh/vibhanou.htm",
         "Dhs.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/3_abh/dhamsgou.htm", 
         "Mil.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/2_parcan/milindou.htm",
        "Vism.txt":"http://gretil.sub.uni-goettingen.de/gretil/2_pali/4_comm/buvismou.htm", 
        "Sp_1":"http://gretil.sub.uni-goettingen.de/gretil/2_pali/4_comm/samp_1ou.htm",
        "Sp_2": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/4_comm/samp_2ou.htm",
        "Sp_3": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/4_comm/samp_3ou.htm",
        "Sp_4":"http://gretil.sub.uni-goettingen.de/gretil/2_pali/4_comm/samp_4ou.htm",
        "Sp_5": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/4_comm/samp_5ou.htm",
        "Sp_6": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/4_comm/samp_6ou.htm",
        "Sp_7": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/4_comm/samp_7ou.htm",
        }

def mainpart():
    print("### Start ###")
    print(" ")
    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(text_requests, text_dict.items())
        list(res)
    print("\n\n#### All texts were installed" + ": Process 100 %"+  "*" * (100 // 5))#八百長

Sp_flag = 0
def text_requests(text_dict_item):
    global Sp_flag
    name, _ = text_dict_item
    if name == "Th.txt":
        Thera_make()
    elif name == "Thi.txt":
        Theri_make()
    elif name == "Ap.txt":
        Ap_create()
    elif name == "Sn.txt":
        Sn_create()
    elif name in {"Cp.txt", "Vm.txt", "Pv.txt", "Dhp.txt", "Bv.txt"}:
        text_name, extention = name.split(".")
        exec("{}_make()".format(text_name))
    elif name in ["Ja_{}.txt".format(i) for i in range(1, 7)]:
        text_name, extention = name.split(".")
        J_create(name, text_name[-1], text_name)
    elif name in ["Sp_{}".format(i) for i in range(1,8)]:
        if Sp_flag == 1:
            pass
        else:
            Sp_flag = 1
            Sp_create()
    else:
        text_create(name)

class process_num():
    def __init__(self):
        self.count = 0
    def plus(self):
        self.count += 1
    def plus_Sp(self):
        self.count += 7
    def output(self):
        return self.count

def process_print(func, process_counter = process_num()):
    @functools.wraps(func)
    def printer(*args, **kwargs):
        proc_per = ( process_counter.output() * 100 // len(text_dict) )
        if args:
            text_name = args[0].split(".")[0]
            if not(os.path.exists(static_path + text_name + "_.txt")):
                print("\r#### Preparing {:14}: ".format(text_name) + "Process {:3} %".format(proc_per) + "*" * (proc_per // 5) + "_" * (20 - (proc_per // 5)), end = "")
                result = func(*args, **kwargs)               
                if text_name == "Sp":
                    process_counter.plus_Sp()
                else:
                    process_counter.plus()
                print("\r#### Done with {:14}: ".format(text_name) + "Process {:3} %".format(proc_per) + "*" * (proc_per // 5) + "_" * (20 - (proc_per // 5)), end="")
                return result
            else:
                if text_name == "Sp":
                    process_counter.plus_Sp()
                else:
                    process_counter.plus()
                print("\r#### Pass {:19}: ".format(text_name) + "Process {:3} %".format(proc_per) + "*" * (proc_per // 5) + "_" * (20 - (proc_per // 5)), end = "")
        else:
            file_name = func.__name__.split("_")[0]
            if  not(os.path.exists(static_path + file_name + "_.txt")) and not(os.path.exists(static_path + file_name + "_.csv")):
                print("\r#### Preparing {:14}: ".format(file_name) + "Process {:3} %".format(proc_per) + "*" * (proc_per // 5) + "_" * (20 - (proc_per // 5)), end="")
                result = func(*args, **kwargs)
                if file_name == "Sp":
                    process_counter.plus_Sp()
                else:
                    process_counter.plus()
                print("\r#### Done with {:14}: ".format(file_name) + "Process {:3} %".format(proc_per) + "*" * (proc_per // 5) + "_" * (20 - (proc_per // 5)), end="")
                return result
            else:
                if file_name == "Sp":
                    process_counter.plus_Sp()
                else:
                    process_counter.plus()
                print("\r#### Pass {:19}: ".format(file_name) + "Process {:3} %".format(proc_per) + "*" * (proc_per // 5) + "_" * (20 - (proc_per // 5)), end="")
    return printer


def text_make(text):
    response = requests.get(text_dict[text])
    response.encoding = "utf-8"
    vin_ = response.text
    vin_ = re.sub(r"<!DOCTYPE html>(.|\s)*?(?=\[page)", "", vin_)
    vin_ = re.sub(r"\r\n", "\n", vin_)#これが大事な一行になる
    if text in {"SN_II.txt", "SN_III.txt", "SN_IV.txt", "SN_V.txt"}:
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?(?=CHAPTER)", "", vin_)
    elif text == "SN_I.txt":
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?(?=<b>SN_1)", "", vin_)
    elif text == "Khp.txt":
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?(?=Buddhaṃ)", "", vin_)
    elif text == "Nidd_I.txt":
        vin_ = re.sub(r"""(?<=page 001\])(.|\s)*?Part I""", "", vin_)
    elif text == "Nidd_II.txt":
        vin_ = re.sub(r"""(?<=page 001\])(.|\s)*?Vatthugāthā\.""", "", vin_)
#    elif text == "Sp_1":
#        get = re.sub(r"(?<=page 001\])(.|\s)*?sammāsambuddhassa\.<br>", "", vin_)
#    elif text == "Sp_2":
#        get = re.sub(r"(?<=\d\])(.|\s)*?PĀRĀJIKA II<br>", "", vin_)
#    elif text == "Sp_3":
#        get = re.sub(r"(?<=\d\])(.|\s)*?SAṄGHĀDISESA I-XIII<br>", "", vin_)
#    elif text == "Sp_4":
#        get = re.sub(r"""(?<=\d\])(.|\s)*?SAMBUDDHASSA\.<span class="red"><sup>1</sup></span><br>""", "", vin_)
#    elif text == "Sp_5":
#        get = re.sub(r"(?<=\d\])(.|\s)*?SAMANTAPĀSĀDIKĀ<br>", "", vin_)
#    elif text == "Sp_6":
#        get = re.sub(r"(?<=\d\])(.|\s)*?KAMMAKKHANDHAKA-VAṆṆANĀ<br>", "", vin_)
#    elif text == "Sp_7":
#        get = re.sub(r"(?<=\d\])(.|\s)*?I<br>", "", vin_)
#    elif text == "Sn.txt":
#        get = re.sub(r"(?<=\d\])(.|\s)*?Uragasutta\.<BR>", "", vin_)
    elif text == "J_1":
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?(?=JaNi)", "", vin_)
    elif text == "Paṭis_II.txt":
        vin_ = re.sub(r"""(?<=page 001\])(.|\s)*?INDRIYAKATHĀ</span><BR>""", "", vin_)
    elif text == "Dhs.txt":
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?{MĀTIKĀ\.}<br>", "", vin_)
    elif text == "Dhātuk.txt":
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?BUDDHASSA<BR>", "", vin_)
    elif text == "Mil.txt":
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?TASSA BHAGAVATO ARAHATO SAMMĀSAMBUDDHASSA\.<BR>", "", vin_)
    elif text == "Vism.txt":
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?NIDĀNĀDIKATHĀ<BR>", "", vin_)
    elif "&nbsp;" in text[:1000] or text in {"Yam_I.txt", "Yam_II.txt", "Pugg.txt", "Paṭis_I.txt"}:
#        print("Case ;&")
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?(?=\n(\w|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\w))", "", vin_)
    else:
 #       print("Case normal")
        vin_ = re.sub(r"(?<=page 001\])(.|\s)*?(?=\n     \S)", "", vin_)
    vin_ = re.sub(r"\[page(.|\s)*?\]", "%", vin_)
    vin_ = re.sub(r"(?<=page 001])(.|\s)*?(?=\n\     \S)", "", vin_)
    vin_ = re.sub(r"(<span class=\"red\">)(\d*)(</span>)", "*"r"\2", vin_)
    #ローマ数字＋タイトル的な部分を消したい
    vin_ = re.sub(r"\((.|\s).*?\d\)", "", vin_)
#    vin_ = re.sub(r"\s+(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3})\.", "", vin_)
#    vin_ = re.sub(r"\s+(I[VX]|V*?I{0,3})\..*?\.", "", vin_)
    vin_ = re.sub(r"\[\d.*?\]", "", vin_)#カッコで括られたセクションの名前のようなところを削除したい
    vin_ = re.sub(r"\s+\d{1,3}\. .*?VAGGA\.", "", vin_)#Jataka の ~ vagga っていうのを消したい
    vin_ = re.sub(r"\s+\[.*?\](\<BR\>|\<br\>)", "", vin_)
    vin_ = re.sub(r"\s+VAGGA (I[VX]|V*?I{0,3})\..*?\.", "", vin_)
    vin_ = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"(<span class=\"large\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"\. \. \.", "@", vin_)
    vin_ = re.sub(r"(?<=\n)\s+?\[.*?\](<BR>|<br>)", "", vin_)#Majjhimanikaya の数字のやつを消したい
    vin_ = re.sub(r"(?<=\n)\s+?(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3}|I{1,3})\.\s{0,1}(?=(<BR>|<br>))", "", vin_)
    vin_ = re.sub(r"(?<=\n)\s+?(X[CL]|L?X{0,3})(I[VX]|V?I{0,3}|I{1,3})\. \w*?\.\s{0,1}(?=(<BR>|<br>))", "", vin_)
    vin_ = re.sub(r"(?<=\n)\s+?.*?, ((C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3}))\.\s{0,1}(?=(<BR>\n|<br>\n))", "", vin_)
    vin_ = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"(red|blue)\">|</span>|<b>|</b>|&nbsnbsp;|&nbsp;|&#8216;|&lt;|&gt;|_{3,})", "", vin_)
    vin_ = re.sub(r"(<BR>|<br>)", "", vin_)
    vin_ = re.sub(r"\n{2,}", "\n", vin_)
    vin_ = re.sub(r"\n%\n", "%", vin_)
    vin_ = re.sub(r"(\w)-%", r"\1"+"&", vin_)
    vin_ = re.sub(r"&{2,}", "&", vin_)#これ特に要らない気もするけど、とりあえず残す。
    vin_ = re.sub(r"(\w)\-\n", r"\1"+"#", vin_)# -改行 は # でとりあえず置き換えておく)
    vin_ = re.sub(r"\n", " \n", vin_)
    vin_ = re.sub(r"--", "@", vin_)#--pa--, --la-- が検索のときに入らないようにするだけ
    text_for_count = re.sub(r"%", " %", vin_)
    text_for_search = re.sub(r"[%&#\n]", "", text_for_count)
    return text_for_count, text_for_search



def bin_maker(text_for_count, text_name):
    line = 0
    page = 0
    j = 0
    page_list = array("I")#あるテキストインデックスにおいて、何ページ・何行目であるかが入る
    line_list = array("I")
    text_index = array("I")#すべての改行位置先頭のテキストインデックスが入る
    end = len(text_for_count) - 1
    for i in range(len(text_for_count) - 1):
        j = j + 1# j はテキストの index そのものを指す
        if i == len(text_for_count) - 1:
            break
        elif text_for_count[i] == "%" or text_for_count[i] == "&" or i == end:#ページ更新の儀式
            j = j - 1
            line = 1
            page += 1
            text_index.append(j)
            page_list.append(page)
            if i != end:
                line_list.append(line)
        elif text_for_count[i] == "\n" or text_for_count[i] == "#":#行更新の儀式
            line += 1
            j = j - 1
            text_index.append(j)
            line_list.append(line)
            page_list.append(page)
            
    index_bin = text_name + "_index_" + ".bin"
    fp = open(static_path + index_bin, "wb")
    text_index.tofile(fp)
    fp.close()
    line_bin = text_name + "_line_" + ".bin"
    fp = open(static_path + line_bin, "wb")
    line_list.tofile(fp)
    fp.close()
    page_bin = text_name + "_page_" + ".bin"
    fp = open(static_path + page_bin, "wb")
    page_list.tofile(fp)
    fp.close()




def Sp_make(text = "Sp"):
    Sp_raw = ""
    for i in range(1, 8):
        response = requests.get(text_dict["Sp_{}".format(i)])
        response.encoding = "utf-8"
        vin_ = response.text
        vin_ = re.sub(r"<!DOCTYPE html>(.|\s)*?(?=\[page)", "", vin_)
        vin_ = re.sub(r"\r\n", "\n", vin_)#これが大事な一行になる
        if i == 1:
            vin_ = re.sub(r"(?<=page 001\])(.|\s)*?sammāsambuddhassa\.<br>", "", vin_)
        elif i == 2:
            start, end = re.search(r"(?<=\d\])(.|\s)*?II<br>", vin_).span()
            vin_ = vin_[:start] + vin_[end:]
#            vin_ = re.sub(r"(?<=\d\])(.|\s)*?II<br>", "", vin_)
        elif i == 3:
            start, end = re.search(r"(?<=\d\])(.|\s)*?SAṄGHĀDISESA I-XIII<br>", vin_).span()
            vin_ = vin_[:start] + vin_[end:]
        elif i == 4:
            start, end = re.search(r"""(?<=\d\])(.|\s)*?SAMBUDDHASSA\.<span class="red"><sup>1</sup></span><br>""", vin_).span()
            vin_ = vin_[:start] + vin_[end:]
        elif i == 5:
            start, end = re.search(r"(?<=\d\])(.|\s)*?SAMANTAPĀSĀDIKĀ<br>", vin_).span()
            vin_ = vin_[:start] + vin_[end:]
        elif i == 6:
            start, end = re.search(r"(?<=\d\])(.|\s)*?KAMMAKKHANDHAKA-VAṆṆANĀ<br>", vin_).span()
            vin_ = vin_[:start] + vin_[end:]
        elif i == 7:
            start, end = re.search(r"(?<=\d\])(.|\s)*?I<br>", vin_).span()
            vin_ = vin_[:start] + vin_[end:]
        Sp_raw += vin_
    vin_ = Sp_raw; Sp_raw = ""
    vin_ = re.sub(r"\[page(.|\s)*?\]", "%", vin_)
    vin_ = re.sub(r"(<span class=\"red\">)(\d*)(</span>)", "*"r"\2", vin_)
    #ローマ数字＋タイトル的な部分を消したい
    vin_ = re.sub(r"\((.|\s).*?\d\)", "", vin_)
#    vin_ = re.sub(r"\s+(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3})\.", "", vin_)
#    vin_ = re.sub(r"\s+(I[VX]|V*?I{0,3})\..*?\.", "", vin_)
    vin_ = re.sub(r"\[\d.*?\]", "", vin_)#カッコで括られたセクションの名前のようなところを削除したい
    vin_ = re.sub(r"\s+\d{1,3}\. .*?VAGGA\.", "", vin_)#Jataka の ~ vagga っていうのを消したい
    vin_ = re.sub(r"\s+\[.*?\](\<BR\>|\<br\>)", "", vin_)
    vin_ = re.sub(r"\s+VAGGA (I[VX]|V*?I{0,3})\..*?\.", "", vin_)
    vin_ = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"(<span class=\"large\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"\. \. \.", "@", vin_)
    vin_ = re.sub(r"(?<=\n)\s+?\[.*?\](<BR>|<br>)", "", vin_)#Majjhimanikaya の数字のやつを消したい
    vin_ = re.sub(r"(?<=\n)\s+?(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3}|I{1,3})\.\s{0,1}(?=(<BR>|<br>))", "", vin_)
    vin_ = re.sub(r"(?<=\n)\s+?(X[CL]|L?X{0,3})(I[VX]|V?I{0,3}|I{1,3})\. \w*?\.\s{0,1}(?=(<BR>|<br>))", "", vin_)
    vin_ = re.sub(r"(?<=\n)\s+?.*?, ((C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3}))\.\s{0,1}(?=(<BR>\n|<br>\n))", "", vin_)
    vin_ = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"(red|blue)\">|</span>|<b>|</b>|&nbsnbsp;|&nbsp;|&#8216;|&lt;|&gt;|_{3,})", "", vin_)
    vin_ = re.sub(r"(<BR>|<br>)", "", vin_)
    vin_ = re.sub(r"\n{2,}", "\n", vin_)
    vin_ = re.sub(r"\n%\n", "%", vin_)
    vin_ = re.sub(r"(\w)-%", r"\1"+"&", vin_)
    vin_ = re.sub(r"&{2,}", "&", vin_)#これ特に要らない気もするけど、とりあえず残す。
    vin_ = re.sub(r"(\w)\-\n", r"\1"+"#", vin_)# -改行 は # でとりあえず置き換えておく)
    vin_ = re.sub(r"\n", " \n", vin_)
    vin_ = re.sub(r"--", "@", vin_)#--pa--, --la-- が検索のときに入らないようにするだけ
    text_for_count = re.sub(r"%", " %", vin_)
    text_for_search = re.sub(r"[%&#\n]", "", text_for_count)
    return text_for_count, text_for_search


def Jataka(text_for_search, text_number):
    pre_long = len(text_for_search)
    verse = []
    J_verse_start = array("I")
    J_verse_end = []
    Jataka = r"Ja\_(.|\s)*?\da?b? \|\|"
    A = re.finditer(Jataka, text_for_search)
    for text in A:
        J_verse_start.append(text.start())#韻文の開始位置を保存しておく
        J_verse_end.append(text.end())
        verse.append([text.group(0)])
        verse_long = len(text_for_search[text.start(): text.end()])
        text_for_search = text_for_search[0: text.start()] + "."*verse_long + text_for_search[text.end():]
    new_Ja = "Ja_" + str(text_number) + "_.txt"
    with open(static_path + new_Ja, "w", encoding="utf-8") as f:
        f.write(text_for_search)        
    new_bin = "J_" + str(text_number) + "_start_point_.bin"
    fp = open(static_path + new_bin, "wb")
    J_verse_start.tofile(fp)
    fp.close()
    new_verse = "J_" + str(text_number) + ".csv"
    with open(static_path + new_verse, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(verse)




def Sn_text_make(text = "Sn"):
    response = requests.get(text_dict["Sn.txt"])
    response.encoding = "utf-8"
    vin_ = response.text
    vin_ = re.sub(r"<!DOCTYPE html>(.|\s)*?(?=\[page)", "", vin_)
    vin_ = re.sub(r"\r\n", "\n", vin_)#これが大事な一行になる
    vin_ = re.sub(r"(?<=\[page 001\])(.|\s)*?Uragasutta\.", "", vin_)
    vin_ = re.sub(r"\[page(.|\s)*?\]", "%", vin_)
     #全てのテキストごとに異なる最初の部分を処理
    vin_ = re.sub(r"\[F\._.*?\]", "", vin_)
    vin_ = re.sub(r"\s+?\d{1,2}.*?(sutta|\d\))\.", "", vin_)
    vin_ = re.sub(r"(<span class=\"red\">)(\d*)(</span>)", "*"r"\2", vin_)
    #ローマ数字＋タイトル的な部分を消したい
    vin_ = re.sub(r"(?<=\n)\s*?(I[VX]|V*?I{0,3})\..*?\.", "", vin_)
    vin_ = re.sub(r"\[\d.*?\]", "", vin_)#カッコで括られたセクションの名前のようなところを削除したい
    vin_ = re.sub(r"\s+\d{1,3}\. .*?VAGGA\.", "", vin_)
    vin_ = re.sub(r"\s+\[.*?\](\<BR\>|\<br\>)", "", vin_)
    vin_ = re.sub(r"\s+VAGGA (I[VX]|V*?I{0,3})\..*?\.", "", vin_)
    vin_ = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"(<span class=\"large\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"(red|blue)\">|<b>|</b>|</span>|&nbsnbsp;|&nbsp;|&#8216;)", "", vin_)
    vin_ = re.sub(r"(<BR>|<br>)", "", vin_)
    vin_ = re.sub(r"\n{2,}", "\n", vin_)
    vin_ = re.sub(r"\n%\n", "%", vin_)
    vin_ = re.sub(r"(\w)-%", r"\1"+"&", vin_)
    vin_ = re.sub(r"&{2,}", "&", vin_)#これ特に要らない気もするけど、とりあえず残す。
    vin_ = re.sub(r"(\w)-\n", r"\1"+"#", vin_)# -改行 は # でとりあえず置き換えておく)
    vin_ = re.sub(r"\n", " \n", vin_)
    text_for_count = re.sub(r"%", " %", vin_)
    text_for_search = re.sub(r"[%&#\n]", "", text_for_count)
    return text_for_count, text_for_search


def Sn(text_for_search):
    pre_long = len(text_for_search)
    verse = []
    J_verse_start = array("I")
    J_verse_end = []
    Jataka = r"\d{1,4}\. .*?\|\|.*?\|\|"
    A = re.finditer(Jataka, text_for_search)
    for text in A:
        J_verse_start.append(text.start())#韻文の開始位置を保存しておく
        J_verse_end.append(text.end())
        if text.group(0) != "":
            verse.append([text.group(0)])
        verse_long = len(text_for_search[text.start(): text.end()])
        text_for_search = text_for_search[0: text.start()] + "."*verse_long + text_for_search[text.end():]
    new_Ja = "Sn_.txt"
    with open(static_path + new_Ja, "w", encoding="utf-8") as f:
        f.write(text_for_search)        
    new_bin = "Sn_verse_start_point.bin"
    fp = open(static_path + new_bin, "wb")
    J_verse_start.tofile(fp)
    fp.close()
    new_verse = "Sn_verse.csv"
    with open(static_path + new_verse, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(verse)

def Ap_make(text = "Ap"):
    response = requests.get(text_dict["Ap.txt"])
    response.encoding = "utf-8"
    vin_ = response.text
    vin_ = re.sub(r"<!DOCTYPE html>(.|\s)*?(?=\[page)", "", vin_)
    vin_ = re.sub(r"\r\n", "\n", vin_)#これが大事な一行になる
    vin_ = re.sub(r"\[page(.|\s)*?\]", "%", vin_)
    vin_ = re.sub(r"(<span class=\"red\">)(\d*)(</span>)", "*"r"\2", vin_)
    vin_ = re.sub(r"\((.|\s).*?\d\)", "", vin_)
    vin_ = re.sub(r"\[\d.*?\]", "", vin_)#カッコで括られたセクションの名前のようなところを削除したい
    vin_ = re.sub(r"\s+\d{1,3}\. .*?VAGGA\.", "", vin_)#Jataka の ~ vagga っていうのを消したい
    vin_ = re.sub(r"\s+\[.*?\](\<BR\>|\<br\>)", "", vin_)
    vin_ = re.sub(r"\s+VAGGA (I[VX]|V*?I{0,3})\..*?\.", "", vin_)
    vin_ = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"(<span class=\"large\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"\. \. \.", "@", vin_)
    vin_ = re.sub(r"\*", "", vin_)
    vin_ = re.sub(r"(?<=\n)\s+?\[.*?\](<BR>|<br>)", "", vin_)#Majjhimanikaya の数字のやつを消したい
    vin_ = re.sub(r"(?<=\n)\s+?(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3}|I{1,3})\.\s{0,1}(?=(<BR>|<br>))", "", vin_)
    vin_ = re.sub(r"(?<=\n)\s+?(X[CL]|L?X{0,3})(I[VX]|V?I{0,3}|I{1,3})\. \w*?\.\s{0,1}(?=(<BR>|<br>))", "", vin_)
    vin = re.sub(r"(?<=\n)\s+?.*?, ((C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[VX]|V?I{0,3}))\.\s{0,1}(?=(<BR>\n|<br>\n))", "", vin_)
    vin_ = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"(red|blue)\">|</span>|<b>|</b>|&nbsnbsp;|&nbsp;|&#8216;|&lt;|&gt;)", "", vin_)
    vin_ = re.sub(r"(\n\s{3,}.*?<BR>)(\n)(\S)", r"\1"+ "~\n" + r"\3", vin_)#apadanaは韻文単位で獲得したいため
    vin_ = re.sub(r"(?<=\n)_*?<BR>\n", "", vin_)
    vin_ = re.sub(r"(?<=\d) //", " //~", vin_)
    vin_ = re.sub(r"(<BR>|<br>)", "", vin_)
    vin_ = re.sub(r"\n{2,}", "\n", vin_)
    vin_ = re.sub(r"\n%\n", "%", vin_)
    vin_ = re.sub(r"(\w)-%", r"\1"+"&", vin_)
    vin_ = re.sub(r"&{2,}", "&", vin_)#これ特に要らない気もするけど、とりあえず残す。
    vin_ = re.sub(r"(\w)\-\n", r"\1"+"#", vin_)# -改行 は # でとりあえず置き換えておく)
    vin_ = re.sub(r"\n", " \n", vin_)
    vin_ = re.sub(r"--", "@", vin_)#--pa--, --la-- が検索のときに入らないようにするだけ
    text_for_count = re.sub(r"%", " %", vin_)
    text_for_search = re.sub(r"[%&#\n]", "", text_for_count)
    return text_for_count, text_for_search

@process_print
def Theri_make(text = "Thi"):
    response = requests.get("http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/therigou.htm")
    response.encoding = "utf-8"
    vin_ = response.text
    vin_ = re.sub(r"<!DOCTYPE html>(.|\s)*?(?=\[page)", "", vin_)
    vin_ = re.sub(r"\r\n", "\n", vin_)#これが大事な一行になる
    vin_ = re.sub(r"itthaṃ sudaṃ bhagavā Muttaṃ sikkhamānaṃ imāya<BR>\ngāthāya abhiṇhaṃ ovadati\. ||<BR>", "", vin_)
    vin_ = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"(<span class=\"large\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"\[page(.|\s)*?\]", "%", vin_)#%page区切りは%で表す
    vin_ = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"(red|blue)\">|</span>|<b>|</b>|&nbsnbsp;|&nbsp;|&#8216;|</body>|</html>)", "", vin_)
    vin_ = re.sub(r"-<BR>\n", "", vin_)#Therigathaだとこれは必須になる
    vin_ = re.sub(r"%", "", vin_)
    vin_ = re.sub(r"^\s{2,}.*?$", "", vin_)
    vin_ = re.sub(r"(?<!\|)<BR>\n", "", vin_)#Therigathaだとこれは必須になる
    vin_ = re.sub(r"-\n", "", vin_)
    vin_ = re.sub(r"\n{2,}", "\n", vin_)
    vin_ = re.sub(r"\r {1,}(?=|| Th)", "", vin_)
    vin_ = re.sub(r"\n\s{1,}\|\| Th", " || Th", vin_)
    vin_ = re.sub(r"(?<=\n)\s{2,}.*?\n", "", vin_)
    vin_ = re.sub(r"(?<=\n)gāthaṃ abhāsitthā ti\. \|\|\n", "", vin_)#Theriのみ使用
    vs = re.finditer(r"(\s|.)*? Thī_.*? \|\|", vin_)
    verse_set = []
    for v in vs:
        verse = v.group(0)
        verse = re.sub(r" \|\n", "|<BR>", verse)
        verse = re.sub(r"\n", "", verse)
        verse_set.append(verse)
    with open(static_path + "Theri_.csv", "w", encoding="utf-8", newline="") as g:
        writer = csv.writer(g)
        writer.writerows(verse_set)

@process_print
def Thera_make(text = "Th"):
    response = requests.get("http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/theragou.htm")
    response.encoding = "utf-8"
    vin_ = response.text
    vin_ = re.sub(r"<!DOCTYPE html>(.|\s)*?(?=\[page)", "", vin_)
    vin_ = re.sub(r"\r\n", "\n", vin_)#これが大事な一行になる
    vin_ = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"(<span class=\"large\">)(.|\s)*?(</span>)", "", vin_)
    vin_ = re.sub(r"\[page(.|\s)*?\]", "", vin_)
    vin_ = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"(red|blue)\">|</span>|<b>|</b>|&nbsnbsp;|&nbsp;|&#8216;|</body>|</html>)", "", vin_)
    vin_ = re.sub(r"-<BR>\n", "", vin_)
    vin_ = re.sub(r"uddānaṃ:(.|\s).*?ti\.<BR>", "", vin_)#悪いけどuddAnaをつぶす
    vin_ = re.sub(r"( {4,})(.*?<BR>\n.*?)( {4,})(.*?\|\| Th_\*\d)", r"\2" + r"\4", vin_)
    vin_ = re.sub(r"-\n", "", vin_)
    vin_ = re.sub(r"\n{2,}", "\n", vin_)
    vin_ = re.sub(r"(?<=\n)abhāsittha\.<BR>", "", vin_)
    vin_ = re.sub(r"(?<=\n)abhāsitthā 'ti.<BR>", "", vin_)
    vin_ = re.sub(r"\n\s{1,}\|\| Th", " || Th", vin_)
    vin_ = re.sub(r"(?<=\n)\s{2,}.*?\n", "", vin_)
    vin_ = re.sub(r"(<BR>\n){2,}", "<BR>\n", vin_)
    vin_ = re.sub(r"\|\| 939 \|\|", "|| Th_939 ||", vin_)#電子テキストの致命的ミスを直す
    vin_ = vin_[:-5] + " || Th_end ||"#最後の韻文も拾えるようにする
    vs = re.finditer(r"(\s|.)*? Th_.*? \|\|", vin_)
    verse_set = []
    for v in vs:
        verse = v.group(0)
        lines = verse.split("<BR>\n")#韻文のpada区切りに関係ない無意味な改行を削る。文字数が30文字未満だったら無意味な改行と判断
        changed_verse = ""
        for line in lines[1:]:
            if len(line) >= 30:
                changed_verse += line + " <BR>"
            else:
                changed_verse = changed_verse[:-4] + line + " <BR>"
        verse_set.append(changed_verse)
    with open(static_path + "Thera_.csv", "w", encoding="utf-8", newline="") as g:
        writer = csv.writer(g)
        writer.writerows(verse_set)

#Cp のテキスト整形のやりかた
@process_print
def Cp_make(text = "Cp"):
    Cp_number = r"<b>Cp_.*</b>"
    Cp_vers = r"\d\s\|\|</b><BR>"
    response = requests.get("http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/carpitou.htm")
    response.encoding = "utf-8"
    text = response.text
    Cp = re.finditer(Cp_number, text)
    Cp_list = [
        (Cp_index.start(), Cp_index.end()) 
        for Cp_index in Cp
        ]
    Cp_text = re.finditer(Cp_vers, text)
    Cp_text_list = [C.end() for C in Cp_text]
    result_list = [
        [text[Cp_list[j][0]: Cp_list[j][1]], text[Cp_list[j][1]+1: Cp_text_list[j]]] 
        for j in range(len(Cp_list))
        ]
    final_result = []
    for text in result_list:
        number = re.sub(r"(<b>|</b>)", "", text[0])
        number = re.sub(r"_", " ", number)
        main = re.sub(r"(<span class=\"red\">)(\d*)(</span>)", "*"r"\2", text[1])
        main = re.sub(r"(<sup>)(\d*)(</sup>)", "*"r"\2", main)
        main = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"red\">|</span>|<b>|</b>|&nbsp;|&#8216;|<BR>)", "", main)
        main = re.sub(r"\n", "<BR>", main)
        main.lstrip().rstrip()
        final_result.append([number, main])        
    with open(static_path + "Cp_.csv", "w", encoding="utf-8", newline="") as g:
        writer = csv.writer(g)
        writer.writerows(final_result)

#         "Vv.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/vimvatou.htm",
#         "Pv.txt": "http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/petvatou.htm",

@process_print
def Vm_make(text = "Vv"):
    response = requests.get("http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/vimvatou.htm")
    response.encoding = "utf-8"
    text = response.text
    start_point = re.finditer(r"<b>Vv.*?</b>", text)
    end_point = re.finditer(r"\d \|\|</b><BR>", text)
    start_points = [(n.start(), n.end()) for n in start_point]
    end_points = [n.end() for n in end_point]
    result = []
    for i in range(len(start_points)):
        number = text[start_points[i][0]: start_points[i][1]]
        main = text[start_points[i][1]+1: end_points[i]]
        number = number.replace("<b>", "").replace("</b>", "")
        main = re.sub(r"(<span class=\"red\"><sup>)(\d*)(</sup></span>)", "*"r"\2", main)
        main = re.sub(r"(<b>|</b>)", "", main)
        main = re.sub(r"<b>.*?</b>", "", main)
        main = re.sub(r"<i>.*?</i>", "", main)
        main = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", main)
        main = re.sub(r"(<sup>)(\d*)(</sup>)", "*"r"\2", main)
        main = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"red\">|</span>|<b>|</b>|&nbsp;|&#8216;)", "", main)
        main = re.sub(r"^ ?.*?$", "", main)
        if main[-4:] == "<BR>":
            main = main[:-4]
        result.append([number + "(Vv)", main.strip()])#(Vv, Vm のテキスト名をここに入力しておく)
    with open(static_path + "Vm_.csv", "w", encoding="utf-8", newline="") as g:
        writer = csv.writer(g)
        writer.writerows(result)

@process_print
def Pv_make(text = "Pv"):
    response = requests.get("http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/petvatou.htm")
    response.encoding = "utf-8"
    text = response.text
    start_point = re.finditer(r"<b>Vv.*?</b>", text)
    end_point = re.finditer(r"\d \|\|</b><BR>", text)
    start_points = [(n.start(), n.end()) for n in start_point]
    end_points = [n.end() for n in end_point]
    result = []
    for i in range(len(start_points)):
        number = text[start_points[i][0]: start_points[i][1]]
        main = text[start_points[i][1]+1: end_points[i]]
        number = number.replace("<b>", "").replace("</b>", "")
        main = re.sub(r"(<span class=\"red\"><sup>)(\d*)(</sup></span>)", "*"r"\2", main)
        main = re.sub(r"(<b>|</b>)", "", main)
        main = re.sub(r"<b>.*?</b>", "", main)
        main = re.sub(r"<i>.*?</i>", "", main)
        main = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", main)
        main = re.sub(r"(<sup>)(\d*)(</sup>)", "*"r"\2", main)
        main = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"red\">|</span>|<b>|</b>|&nbsp;|&#8216;)", "", main)
        main = re.sub(r"^ ?.*?$", "", main)
        if main[-4:] == "<BR>":
            main = main[:-4]
        result.append([number + "(Pv)", main.strip()])#(Vv, Vm のテキスト名をここに入力しておく)
    with open(static_path + "Pv_.csv", "w", encoding="utf-8", newline="") as g:
        writer = csv.writer(g)
        writer.writerows(result)

@process_print
def Dhp_make(name = "Dhp", targetter = r"\/\/ Dhp_.* \/\/<BR>"):
    response = requests.get("http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/dhampdou.htm")
    response.encoding = "utf-8"
    text = response.text
    text = re.sub(r"<!DOCTYPE html>(.|\s)*?(?=\[page)", "", text)
    main = re.sub(r"\r\n", "\n", text)
    vers_number = re.findall(targetter, main)#例えば Dhp は r"\/\/ Dhp_.* \/\/<BR>"
    vers_number = [num.replace("<BR>", "").replace(" ", "").replace("/", "").replace("<b>", "").replace("_", " ") for num in vers_number]
    main = re.sub(r"(<span class=\"red\">)(\d*)(</span>)", "*"r"\2", main)
    main = re.sub(r"<b>.*?</b>", "", main)
    main = re.sub(r"<i>.*?</i>", "", main)
    main = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", main)
    main = re.sub(r"<BR> ?.*?<BR>", "", main)
    main = re.sub(r"(<sup>)(\d*)(</sup>)", "*"r"\2", main)
    main = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"red\">|</span>|<b>|</b>|&nbsp;|&#8216;|<BR>|\[page 001\])", "", main)
    main = re.sub(r"^ ?.*?$", "", main)
    lines = main.split("\n")
    result_lines = [line for line in lines if line != "" and line[0] != " "]
    final_result = []
    vers_heap = ""
    for line in result_lines:
        if line[-2:] == "//":
            vers_heap += line
            final_result.append(vers_heap)
            vers_heap = ""
        else:
            vers_heap += line + "<BR>"
    out = zip(vers_number, final_result)
    print_out = [list(i) for i in out]
    with open(static_path + "Dhp_.csv", "w", encoding="utf-8", newline="") as g:
        writer = csv.writer(g)
        writer.writerows(print_out)

@process_print
def Bv_make(name = "Bv", targetter = r"\/\/ Bv_.* \/\/<BR>"):
    response = requests.get("http://gretil.sub.uni-goettingen.de/gretil/2_pali/1_tipit/2_sut/5_khudd/budvmsou.htm")
    response.encoding = "utf-8"
    text = response.text
    text = re.sub(r"<!DOCTYPE html>(.|\s)*?(?=\[page)", "", text)
    main = re.sub(r"\r\n", "\n", text)
    vers_number = re.findall(targetter, main)#例えば Dhp は r"\/\/ Dhp_.* \/\/<BR>"
    vers_number = [num.replace("<BR>", "").replace(" ", "").replace("/", "").replace("<b>", "").replace("_", " ") for num in vers_number]
    main = re.sub(r"(<span class=\"red\">)(\d*)(</span>)", "*"r"\2", main)
    main = re.sub(r"<b>.*?</b>", "", main)
    main = re.sub(r"<i>.*?</i>", "", main)
    main = re.sub(r"(<span class=\"red\">)(.|\s)*?(</span>)", "", main)
    main = re.sub(r"<BR> ?.*?<BR>", "", main)
    main = re.sub(r"(<sup>)(\d*)(</sup>)", "*"r"\2", main)
    main = re.sub(r"(<i>(.|\s)*?</i>|<span class=\"red\">|</span>|<b>|</b>|&nbsp;|&#8216;|<BR>|\[page 001\])", "", main)
    main = re.sub(r"^ ?.*?$", "", main)
    lines = main.split("\n")
    result_lines = [line for line in lines if line != "" and line[0] != " "]
    final_result = []
    vers_heap = ""
    for line in result_lines:
        if line[-2:] == "//":
            vers_heap += line
            final_result.append(vers_heap)
            vers_heap = ""
        else:
            vers_heap += line + "<BR>"
    out = zip(vers_number, final_result)
    print_out = [list(i) for i in out]
    with open(static_path + "Bv_.csv", "w", encoding="utf-8", newline="") as g:
        writer = csv.writer(g)
        writer.writerows(print_out)

@process_print
def Sp_create(text = "Sp"):
    text_for_count, text_for_search = Sp_make(text)
    bin_maker(text_for_count, text_name = "Sp")
    new_text = "Sp_.txt"
    with open(static_path + new_text, "w", encoding="utf-8") as f:
        f.write(text_for_search)

@process_print
def Ap_create():
    text_for_count, text_for_search = Ap_make()
    bin_maker(text_for_count, "Ap")
    with open(static_path + "Ap_.txt", "w", encoding="utf-8") as f:
        f.write(text_for_search)

@process_print
def Sn_create(text = "Sn", text_name = "Sn"):
    text_for_count, text_for_search = Sn_text_make(text)
    Sn(text_for_search)
    bin_maker(text_for_count, text_name)

@process_print
def J_create(text, text_number, text_name):
    text_for_count, text_for_search = text_make(text)
    Jataka(text_for_search, text_number)
    bin_maker(text_for_count, text_name)

@process_print
def text_create(text):
    text_for_count, text_for_search = text_make(text)
    name, extention = text.split(".")
    bin_maker(text_for_count, name)
    new_text = name + "_.txt"
    with open(static_path + new_text, "w", encoding="utf-8") as f:
        f.write(text_for_search)

if __name__ == "__main__":
#    Sp_flag = 0
#    def text_requests(text_dict_item):
#        global Sp_flag
#        name, _ = text_dict_item
#        if name == "Th.txt":
#            Thera_make()
#        elif name == "Thi.txt":
#            Theri_make()
#        elif name == "Ap.txt":
#            Ap_create()
#        elif name == "Sn.txt":
#            Sn_create()
#        elif name in {"Cp.txt", "Vm.txt", "Pv.txt", "Dhp.txt", "Bv.txt"}:
#            text_name, extention = name.split(".")
#            exec("{}_make()".format(text_name))
#        elif name in ["Ja_{}.txt".format(i) for i in range(1, 7)]:
#            text_name, extention = name.split(".")
#            J_create(name, text_name[-1], text_name)
#        elif name in ["Sp_{}".format(i) for i in range(1,8)]:
#            if Sp_flag == 1:
#                pass
#            else:
#                Sp_flag = 1
#                Sp_create()
#        else:
#            text_create(name)
    mainpart()
    
#    with futures.ThreadPoolExecutor() as executor:
#        res = executor.map(text_requests, text_dict.items())
#        list(res)
#    Theri_make()
#    Thera_make()
#    Cp_make()
#    Vm_make()
#    Pv_make()
#    Dhp_make()
#    Bv_make()
#    Sn_create()
#    Ap_create()



