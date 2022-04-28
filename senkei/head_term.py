
from turtle import title
import MeCab
import math

mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
# text = '解析したいテキスト'
# mecab.parse('')#文字列がGCされるのを防ぐ
# node = mecab.parseToNode(text)
# while node:
#     #単語を取得
#     word = node.surface
#     #品詞を取得
#     pos = node.feature.split(",")[1]
#     print('{0} , {1}'.format(word, pos))
#     #次の単語に進める
#     node = node.next
    
# text = "解析したいテキストを入れる。"
# m = MeCab.Tagger("-Ochasen /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

# nouns = [line for line in m.parse(text).splitlines()
#                if "名詞" in line.split()[-1]]

# terms = []
# for str in nouns:
#     terms.append(str.split()[0])

# print(terms)
   
   #print()
   #print('')



def get_nouns(sentence_list):
    # m = MeCab.Tagger("-Ochasen /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    
    # terms_page = []
    # for i in range(len(sentence_list)):    
    #     # 分けてノードごとにする
    #     node = m.parseToNode(sentence_list[i])
    #     terms = []
    #     select_conditions = ['名詞']
        
    #     while node:

    #         # 単語
    #         term = node.surface
    #         # 品詞
    #         pos = node.feature.split(',')[0]
    #         # もし品詞が条件と一致してたら
    #         if pos in select_conditions:
    #             terms.append(term)
    #         node = node.next
    #         # 連結
    #     terms_page.extend(terms)
    # #print(type(terms_page))
    
    # terms_page = list(set(terms_page)
    nounAndPronoun = []
    for i in range(len(sentence_list)):  
        mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        text = sentence_list[i]
        result = mecab.parse(text)
        #print(result)
        lines = result.split('\n')
        
        for line in lines:
            feature = line.split('\t')
            if len(feature) == 2:
                info = feature[1].split(',')
                hinshi = info[0]
                if hinshi in ('名詞', '固有名詞'):
                    nounAndPronoun.append(info[6])
                    
    return nounAndPronoun


def get_nouns_title(sentence):
    # m = MeCab.Tagger("-Ochasen /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    text = sentence
    result = mecab.parse(text)
    #print(result)
    lines = result.split('\n')
    nounAndPronoun = []
    for line in lines:
        feature = line.split('\t')
        if len(feature) == 2: #'EOS'と''を省く
            info = feature[1].split(',')
            hinshi = info[0]
            if hinshi in ('名詞', '固有名詞'):
                nounAndPronoun.append(info[6])
    # terms_page = []
    # # 分けてノードごとにする
    # node = m.parseToNode(sentence)
    # terms = []
    # select_conditions = ['名詞']
        
    # while node:
    #     # 単語
    #     term = node.surface
    #     # 品詞
    #     pos = node.feature.split(',')[0]
    #     # もし品詞が条件と一致してたら
    #     if pos in select_conditions:
    #         terms.append(term)
    #     node = node.next
    #     # 連結
    # terms_page.extend(terms)
    # terms_page = list(set(terms_page))
    nounAndPronoun = list(set(nounAndPronoun))
    
    return nounAndPronoun

import pandas as pd

sitename_list = ['ai-trend.jp','atarimae.biz','iwata-system-support.com','jfor.net','k-san.link',
                 'linear-algebra.com','linky-juku.com','manabitimes.jp','math-fun.net',
                 'math-juken.com','math-note.xyz','mathwords.net','oguemon.com','opencourse.doshisha.ac.jp',
                 'ramenhuhu.com','risalc.info','sun.ac.jp','takun-physics.net',
                 'tau.doshisha.ac.jp','univ-study.net','w3e.kanazawa-it.ac.jp',
                 'www.geisya.or.jp','www.headboost.jp','www.momoyama-usagi']

#あるサイトの
#for i in range(1):
for i in range(len(sitename_list)):
    sitename = sitename_list[i]

    column_id = []
    column_URL = []
    column_title = []
    column_title_terms = []
    column_title_terms_num = []
    column_head_text = []
    column_head_text_num = []
    column_head_terms = []
    column_head_terms_num = []
    column_all_term = []
    column_all_term_num = []
    
    df = pd.read_csv('/Users/kazuki/Desktop/research/data_1619/senkei/html_data/correspondence_list_'+sitename+'.csv',header=None)
    filename = df[0]
    fileurl = df[1]
    
    #あるページの
    #for j in range(1):
    for j in range(len(df[0])):
        filename = df[0][j]
        fileurl = df[1][j]
        print('id',filename)
        
        df_file_head = pd.read_csv('/Users/kazuki/Desktop/research/data_1619/senkei/Headline_extraction/head_data/'+sitename+'/head_'+filename+'.csv')
        #タイトルがあるなら
        #if len(df_file_head['URL']) > 0:
        print(len(df_file_head['URL']))
        if len(df_file_head['URL'])>0 and df_file_head['URL'][0] == 'title':
            title_ = df_file_head.query('URL == ["title"]')['タグ名'][0]
        else:
            title_ = ''
            
        #print('タイトル',title_)
        column_title.append(title_)
        title_term = get_nouns_title(title_)
        column_title_terms.append(title_term)
        column_title_terms_num.append(len(title_term))
        #print('URL',fileurl)
        print('タイトル内の用語',title_term)
        print('タイトル内の用語数',len(title_term))
        
        head_text = []
        for k in range(len(df_file_head['URL'])):
        # for k in range(len(df_file_head)):
            head_text.append(df_file_head['タグテキスト'][k])
        
            
        head_text = [x for x in head_text if pd.isnull(x) == False]
        #print('見出し',head_text)
        #print('見出し数',len(head_text))
        column_head_text_num.append(len(head_text))
        
        head_term = get_nouns(head_text)
        column_head_terms.append(head_term)
        print('見出し内の用語',head_term)
        print('見出し内の用語数',len(head_term))
        column_head_terms_num.append(len(head_term))
        
        
        term_all = title_term+head_term
        term_all = list(set(term_all))
        column_all_term.append(term_all)
        column_all_term_num.append(len(term_all))
        print('タイトル・見出し用語',term_all)
        print('タイトル・見出し用語数',len(term_all))
        
        
        column_id.append(filename)
        column_URL.append(fileurl)
        column_head_text.append(head_text)

    df_output = pd.DataFrame({'id':column_id,'URL':column_URL,'タイトル':column_title,'タイトル・見出し出現用語':column_all_term,'タイトル・見出し出現用語数':column_all_term_num,'タイトル内単語':column_title_terms,'タイトル内単語数':column_title_terms_num,'見出し文':column_head_text,'見出し文数':column_head_text_num,'見出し内単語':column_head_terms,'見出し内単語数':column_head_terms_num})
    
    #print(df_output.head(3))
    
    df_output.to_csv('head_data_site/'+sitename+"_header_term.csv",sep=',')
    