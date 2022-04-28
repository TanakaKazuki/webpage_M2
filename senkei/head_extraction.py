# "見出しを抽出し、csvに出力するプログラム"
#  "correspondenceの１列目の番号番目のtxtファイルを読み込む"



# 出力csvイメージ
# URL｜タグ｜タグテキスト｜テキスト
#    ｜　　｜　　　
#    ｜　　｜


import re
import csv
from pathlib import Path
from lxml import html
import os

# 不要なタグを検索する xpath 表現のタプル
REMOVE_TAGS = ('.//style', './/script', './/noscript')

# 見出しタグを検索する xpath 表現
XPATH_H_TAGS = './/h1|.//h2|.//h3|.//h4|.//h5|.//h6'

# 見出しタグを検出するための正規表現
RE_H_MATCH = re.compile('^h[1-6]$').match


    

def main(fname,furl,sitename):
    """メイン関数"""
    filename = fname[0]
    fileurl = furl[1]
    print(filename)
    print(fileurl)
    
    for i in range(len(fname)):
        filename = fname[i]
        fileurl = furl[i]
        
        # (1/8) HTML ファイルを指定します
        if os.path.exists('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/'+sitename+'./'+filename+'.txt'):
            src_file = Path(r'/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/'+sitename+'./'+filename+'.txt')
        elif os.path.exists('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/'+sitename+'./'+filename+'_NotFindTitle.txt'):
            src_file = Path(r'/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/'+sitename+'./'+filename+'_NotFindTitle.txt')
        
        # (2/8) HTML データを取得します
        with src_file.open('rb') as f:
            html_data = f.read()
        
        # エンコーディングを指定してパーサーを作成
        html_parser = html.HTMLParser(encoding='utf-8')

        
        # (3/8) HTML を解析します
        root = html.fromstring(html_data,parser=html_parser)

        # (4/8) HTML から不要なタグを削除します
        for remove_tag in REMOVE_TAGS:
            for tag in root.findall(remove_tag):
                tag.drop_tree()

        # (5/8) テキストの入れ物を用意します
        #      (デバッグ用にラベル行も追加)
        texts = []
        texts.append(
           # ['URL','タグ名', 'タグテキスト', 'タグに属するテキスト'])
           ['URL','タグ名', 'タグテキスト'])

        # (6/8) タイトルタグを取得します
        t = root.find('.//title')
        if t is not None:
            text = t.text_content()

            # 空でなければリストに追加
            if text:
                texts.append([t.tag, text, ''])

            print(f'(デバッグ) {t.tag}: {text}\n')

        # (7/8) 見出しタグを検索します
        for h_tag in root.xpath(XPATH_H_TAGS):
            # 見出しタグのテキストを取得
            h_text = h_tag.text_content()

            print(f'(デバッグ) {h_tag.tag}: {h_text}')

            # 見出しタグと同じ階層にあったテキストを入れるリスト
            contents = []

            # 見出しの次のタグを取得
            next_tag = h_tag.getnext()

            # 次のタグがなくなるまでループ
            # while next_tag is not None:
            #     # タグが見出しだったらブレーク
            #     if RE_H_MATCH(next_tag.tag):
            #         print(f'(デバッグ) 次の見出しタグ {next_tag.tag} が見つかった。')
            #         print(f'(デバッグ) while ブレーク\n')
            #         break

            #     # タグのテキストを取得
            #     text = next_tag.text_content()

            #     # 空でなければリストに追加
            #     if text:
            #         contents.append(text)

            #     print(f'(デバッグ) {next_tag.tag}: {text}')

            #     # さらに次のタグを取得してループする
            #     next_tag = next_tag.getnext()
            # else:
            #     # 同じ階層のタグをたどり尽くして、次のタグが無かった場合。
            #     print(f'(デバッグ) 次のタグが無かった。 {next_tag}')

            # # リストを連結してひとつの文字列にします
            # contents = '|'.join(contents)

            # リストに追加
            #texts.append([fileurl ,h_tag.tag, h_text, contents])
            texts.append([fileurl ,h_tag.tag, h_text])

        # (8/8) テキストを CSV に保存します
        csv_file = Path(r'/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/head_data/'+sitename+'/head_'+filename+'.csv')
        with csv_file.open('w', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerows(texts)

    # 以上です
    return


import pandas as pd

if __name__ == "__main__":
    """読み込むファイル名の指定"""
    #path
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_ai-trend.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_atarimae.biz.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_iwata-system-support.com.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_jfor.net.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_k-san.link.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_linear-algebra.com.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_linky-juku.com.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_manabitimes.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_math-fun.net.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_math-juken.com.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_math-note.xyz.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_mathwords.net.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_oguemon.com.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_opencourse.doshisha.ac.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_ramenhuhu.com.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_risalc.info.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_sun.ac.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_takun-physics.net.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_tau.doshisha.ac.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_univ-study.net.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_w3e.kanazawa-it.ac.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_www.geisya.or.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_www.headboost.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_www.momoyama-usagi.csv
    

    df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/correspondence_list_www.momoyama-usagi.csv',header=None)
    filename = df[0]
    fileurl = df[1]
    print(filename.head(50))
    print(fileurl.head(50))
    
    #'ai-trend.jp'
    #'atarimae.biz'
    #'iwata-system-support.com'
    #'jfor.net'
    #'k-san.link'
    #'linear-algebra.com'
    #'linky-juku.com'
    #'manabitimes.jp'
    #'math-fun.net'
    #'math-juken.com'
    #'math-note.xyz'
    #'mathwords.net'
    #'oguemon.com'
    #opencourse.doshisha.ac.jp
    #ramenhuhu.com
    #risalc.info
    #'sun.ac.jp'
    #'takun-physics.net'
    #'tau.doshisha.ac.jp'
    #'univ-study.net'
    #'w3e.kanazawa-it.ac.jp'
    #'www.geisya.or.jp.csv'
    #'www.headboost.jp'
    #'www.momoyama-usagi'
    
    sitename ='www.momoyama-usagi'

    main(filename,fileurl,sitename)

