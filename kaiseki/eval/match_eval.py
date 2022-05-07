import csv
from pathlib import Path
import os
from re import A
import pandas as pd
import numpy as np
import datetime as dt

def main(list_handmatch_site,list_textname,limit):
  
  
  dir_handmatch,dir_eval,dir_handmatch_check= make_derectory()
  
  for i in  range(len(list_handmatch_site)):
    text_name = list_textname[0]
    site_name = list_handmatch_site[i]
    #プログラムでマッチングさせた結果
    df_match_result = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/text_match/'+text_name+'/'+text_name+''+site_name+'_'+limit+'.csv')
    #手作業でマッチングさせた結果
    #節番号	節名	マッチページ	マッチページURL	補足
    df_handmatch = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/hand_match/handmatch_'+text_name+'_'+site_name+'.csv')
    #print(df_match_result)
    #print(df_handmatch)
    
    
    #df_handmatch中のページが、df_match_resultにあるかどうか
    ##タイトルは変わってるため、URLで判断
    df_handmatch_neo = eval(df_match_result,df_handmatch)
    df_handmatch_neo.to_csv(dir_handmatch +'/eval_handmatch_'+text_name+'_'+site_name+'_'+limit+'.csv',sep=',',index=None) 
    df_handmatch_neo.to_excel(dir_handmatch +'/eval_handmatch_'+text_name+'_'+site_name+'_'+limit+'.xlsx') 
    
    #出力ファイルの中で'match'、'not match'の内訳の出力、csv、xlsx
    eval_calc(df_handmatch_neo,text_name,site_name,dir_eval)
    
    
    #df_handmatch_neoで
    #matchするページは、節との共通語を、
    #matchしないページ内出現用語と、その理想のマッチ節を出力し、
    #なぜマッチしないのかを確認
    
    #テキストの出現用語
    df_text_mecab = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/kosen_biseki1_mecab.csv')
    #各サイトの全ページ見出し用語
    df_all_head_term = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/head_data_site/'+site_name+'_header_term.csv')
    
    check_match(df_handmatch_neo,df_match_result,dir_handmatch_check,text_name,site_name,limit,df_text_mecab,df_all_head_term)


#手作業でのマッチ結果に対して、
#マッチしたページは、そのマッチ用語と節内出現用語、ページ見出し内出現用語
#マッチしなかったページは、節内出現用語、ページ見出し内出現用語　


def check_match(df_handmatch_neo,df_match_result,dir_handmatch_check,text_name,site_name,limit,df_text_mecab,df_all_head_term):
  column_setu = []
  column_setu_name = []
  column_page = []
  column_url = []
  column_match = []
  column_match_term = []
  column_setu_term = []
  column_head_term = []
  column_hosoku = []
  
  
  
  for num in range(len(df_handmatch_neo)):
    if df_handmatch_neo['eval_match'][num]=='match':
      column_setu.append(df_handmatch_neo['節番号'][num])
      column_setu_name.append(df_handmatch_neo['節名'][num])
      column_page.append(df_handmatch_neo['マッチページ'][num])
      column_url.append(df_handmatch_neo['マッチページURL'][num])
      column_match.append('match')
      
      match_term = df_match_result['マッチ用語'][(df_match_result['節番号'] == df_handmatch_neo['節番号'][num])
                        &
                        (df_match_result['マッチページURL'] == df_handmatch_neo['マッチページURL'][num])]
      
      match_term = match_term.reset_index()['マッチ用語'][0]
      column_match_term.append(match_term)
      
      setu_term = df_match_result['節内出現用語'][(df_match_result['節番号'] == df_handmatch_neo['節番号'][num]) 
                        &
                        (df_match_result['マッチページURL'] == df_handmatch_neo['マッチページURL'][num])]
      
      setu_term = setu_term.reset_index()['節内出現用語'][0]
      column_setu_term.append(setu_term)
      
      
      head_term = df_match_result['マッチページ見出し用語'][(df_match_result['節番号'] == df_handmatch_neo['節番号'][num]) 
                        &
                        (df_match_result['マッチページURL'] == df_handmatch_neo['マッチページURL'][num])]
      head_term  = head_term.reset_index()['マッチページ見出し用語'][0]
      column_head_term.append(setu_term)
  
      column_hosoku.append(df_handmatch_neo['補足'][num])
      
    elif df_handmatch_neo['eval_match'][num]=='not match':
      column_setu.append(df_handmatch_neo['節番号'][num])
      column_setu_name.append(df_handmatch_neo['節名'][num])
      column_page.append(df_handmatch_neo['マッチページ'][num])
      column_url.append(df_handmatch_neo['マッチページURL'][num])
      column_match.append('not match')
      column_match_term.append('')
      
      setu_term = df_text_mecab['term_mecab'][df_text_mecab['setu_num'] == df_handmatch_neo['節番号'][num]]
      setu_term = setu_term.reset_index()['term_mecab'][0]
      column_setu_term.append(setu_term)
      #column_setu_term.append(df_text_mecab[df_text_mecab['setu_num'] == df_handmatch_neo['節番号'][num]]['term_mecab'])
      head_term = df_all_head_term['タイトル・見出し出現用語'][df_all_head_term['URL']==df_handmatch_neo['マッチページURL'][num]]
      print(head_term)
      if not head_term.empty:
        head_term = head_term.reset_index()['タイトル・見出し出現用語'][0]
        column_head_term.append(head_term)
      else:
        column_head_term.append([])
      #column_head_term.append(df_all_head_term[df_all_head_term['URL']==df_handmatch_neo['マッチページURL'][num]]['タイトル・見出し出現用語'])
    
      column_hosoku.append(df_handmatch_neo['補足'][num])
    
  df_output = pd.DataFrame({'節番号':column_setu,'節名':column_setu_name,'手作業マッチページ':column_page,'手作業マッチページURL':column_url,'マッチング結果':column_match,'マッチ用語':column_match_term,'節内出現用語':column_setu_term,'マッチページ見出し用語':column_head_term,'補足':column_hosoku})
  df_output.to_csv(dir_handmatch_check +'/check_handmatch_'+text_name+'_'+site_name+'_'+limit+'.csv',sep=',',index=None) 
  df_output.to_excel(dir_handmatch_check +'/check_handmatch_'+text_name+'_'+site_name+'_'+limit+'.xlsx') 
        
      
    
    
    
def eval(df_match_result,df_handmatch):
  #df_handmatch_neo = 人手の結果が、マッチング結果にあるか否かの列を追加したバージョン
  df_handmatch_neo = df_handmatch.copy()
  df_handmatch_neo['eval_match'] = ''
  for j in range(len(df_handmatch)):
    handmatch_page_url = df_handmatch['マッチページURL'][j]
    handmatch_page_setu = df_handmatch['節番号'][j]
    #マッチング結果中のある節番号部分
    df_for_check = df_match_result[df_match_result['節番号']==handmatch_page_setu]
    if not df_for_check.empty:
      #for k in range(len(df_for_check)):
        #print(df_for_check['マッチページURL'].values)
      if handmatch_page_url in df_for_check['マッチページURL'].values:
        df_handmatch_neo['eval_match'][j]= 'match'
        print('match')
      else:
        df_handmatch_neo['eval_match'][j]= 'not match'
        print('not match')
        print(handmatch_page_url)
        print(df_for_check['マッチページURL'].values)
    else:
      df_handmatch_neo['eval_match'][j]= 'not match'
      print('not match')
  
  return df_handmatch_neo

#プログラム実行日のフォルダを作る
def make_derectory():
  dt_now = dt.datetime.now()
 
  #フォルダ名用にyyyymmddの文字列を取得する
  mmdd = dt_now.strftime('%m%d')
 
  #作成するフォルダ名を定義する
  directory_name = u'handmatch_eval_' + mmdd
 
  #現在のフォルダパスを取得する(プログラムが実行されているフォルダパス)
  #current_directory = os.path.dirname(os.path.abspath(__file__))
 
  #作成のために確認するフォルダパスを作成する
  create_directory =  '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/handmatch_eval'+ '/' + directory_name
 
  #対象フォルダが存在しない場合
  if(not (os.path.exists(create_directory))):
 
    #フォルダを作成
    os.mkdir(create_directory)
  
  directory_name2 = u'eval_calc' + mmdd
  create_directory2 = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/handmatch_eval/eval_calc/'+ '/' + directory_name2
  if(not (os.path.exists(create_directory2))):
 
    #フォルダを作成
    os.mkdir(create_directory2)
  
  directory_name3 = u'matchしない理由の調査'
  create_directory3 = create_directory +'/'+directory_name3
  if(not (os.path.exists(create_directory3))):
 
    #フォルダを作成
    os.mkdir(create_directory3)
  
  
  return create_directory,create_directory2,create_directory3
  
def eval_calc(df_handmatch_neo,text_name,site_name,dir):
  #人手の結果と、マッチしたページ、マッチしなかったページの内訳を見る
  #’タイトル変更無し’・’タイトル変更あり’、最近作られた
  #また、マッチしなかったページのうち、別の節でならマッチしているか
  
  
  #補足のNaN要素は、”変更無し”に変更
  df_handmatch_neo = df_handmatch_neo.fillna('変更無し')
  #まず、全体のうち、'match'/'not match'の数を数える
  df_bool_match = (df_handmatch_neo['eval_match'] == 'match')
  print('match sum')
  print(df_bool_match.sum())
  df_bool_notmatch = (df_handmatch_neo['eval_match'] == 'not match')
  print('not match sum')
  print(df_bool_notmatch.sum())
  
  #matchのうち、’変更無し’・’タイトル変更あり’の内訳調査
  
  
  #変更無し
  df_bool_match_no_titlechange = ((df_handmatch_neo['eval_match'] == 'match') & (df_handmatch_neo['補足']=='変更無し'))
  print('match_no_titlechange sum タイトル変更無し')
  print(df_bool_match_no_titlechange.sum())
  #最近作られた
  df_bool_match_make_recently = ((df_handmatch_neo['eval_match'] == 'match' )& (df_handmatch_neo['補足']== '最近作られた'))
  print('df_bool_match_make_recently sum　最近作られた')
  print(df_bool_match_make_recently.sum())
  #タイトル変更あり
  df_bool_match_titlechange = ((df_handmatch_neo['eval_match'] == 'match' )&(df_handmatch_neo['補足']!='変更無し') &(df_handmatch_neo['補足']!= '最近作られた'))
  print('df_bool_match_titlechange sum　タイトル変更あり')
  print(df_bool_match_titlechange.sum())
  
  #not matchのうち、’変更無し’・’タイトル変更あり’・’最近作られた’の内訳も調査
  #変更無し
  df_bool_not_match_no_titlechange = ((df_handmatch_neo['eval_match'] == 'not match') & (df_handmatch_neo['補足']=='変更無し'))
  print('not_match_no_titlechange sum タイトル変更無し')
  print(df_bool_not_match_no_titlechange.sum())
  #最近作られた
  df_bool_not_match_make_recently = ((df_handmatch_neo['eval_match'] == 'not match' )& (df_handmatch_neo['補足']== '最近作られた'))
  print('df_bool_not_match_make_recently sum　最近作られた')
  print(df_bool_not_match_make_recently.sum())
  #タイトル変更あり
  df_bool_not_match_titlechange = ((df_handmatch_neo['eval_match'] == 'not match' )&(df_handmatch_neo['補足']!='変更無し') &(df_handmatch_neo['補足']!= '最近作られた'))
  print('df_bool_not_match_titlechange sum　タイトル変更あり')
  print(df_bool_not_match_titlechange.sum())

  
  
  

  with open(dir +'/eval_calc_handmatch_'+text_name+'_'+site_name+'_'+limit+'.csv', 'w', newline='') as output_file:
      writer = csv.writer(output_file)
      writer.writerow(["","matchページ", "", "not matchページ"])
      writer.writerow(["ページ数",df_bool_match.sum(), df_bool_notmatch.sum()])
      writer.writerow(["タイトル変更無し", df_bool_match_no_titlechange.sum(), df_bool_not_match_no_titlechange.sum()])
      writer.writerow(["タイトル変更あり",df_bool_match_titlechange.sum(), df_bool_not_match_titlechange.sum()])
      writer.writerow(["収集以降作られたページ",df_bool_match_make_recently.sum(), df_bool_not_match_make_recently.sum()])




if __name__ == "__main__":    
    
    #list_handmatch_site = ['manabitimes.jp','univ-juken.com']
    list_handmatch_site = ['univ-juken.com','manabitimes.jp']
    list_textname = ['kosen_biseki1']
    limit = '1'
  
    main(list_handmatch_site,list_textname,limit)