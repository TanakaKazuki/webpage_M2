import csv
from pathlib import Path
import os
from re import A
import pandas as pd
import numpy as np


def main(list_handmatch_site,list_textname,limit):
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
    df_handmatch_neo.to_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/handmatch_eval/eval_handmatch_'+text_name+'_'+site_name+'_'+limit+'.csv',sep=',',index=None) 
    df_handmatch_neo.to_excel('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/handmatch_eval/eval_handmatch_'+text_name+'_'+site_name+'_'+limit+'.xlsx') 
    
    #出力ファイルの中で'match'、'not match'の内訳の出力、csv、xlsx
    eval_calc(df_handmatch_neo,text_name,site_name)
    
    
    
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
    
  
def eval_calc(df_handmatch_neo,text_name,site_name):
  #人手の結果と、マッチしたページ、マッチしなかったページの内訳を見る
  #’タイトル変更無し’・’タイトル変更あり’
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
  # df_bool_match_make_recently = ((df_handmatch_neo['eval_match'] == 'match' )& (df_handmatch_neo['補足']== '最近作られた'))
  # print('df_bool_match_make_recently sum　最近作られた')
  # print(df_bool_match_make_recently.sum())
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
  # df_bool_not_match_make_recently = ((df_handmatch_neo['eval_match'] == 'not match' )& (df_handmatch_neo['補足']== '最近作られた'))
  # print('df_bool_not_match_make_recently sum　最近作られた')
  # print(df_bool_not_match_make_recently.sum())
  #タイトル変更あり
  df_bool_not_match_titlechange = ((df_handmatch_neo['eval_match'] == 'not match' )&(df_handmatch_neo['補足']!='変更無し') &(df_handmatch_neo['補足']!= '最近作られた'))
  print('df_bool_not_match_titlechange sum　タイトル変更あり')
  print(df_bool_not_match_titlechange.sum())

  
  
  

  with open('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/handmatch_eval/eval_calc/eval_calc_handmatch_'+text_name+'_'+site_name+'_'+limit+'.csv', 'w', newline='') as output_file:
      writer = csv.writer(output_file)
      writer.writerow(["","matchページ", "", "not matchページ"])
      writer.writerow(["ページ数",df_bool_match.sum(), df_bool_notmatch.sum()])
      writer.writerow(["タイトル変更無し", df_bool_match_no_titlechange.sum(), df_bool_not_match_no_titlechange.sum()])
      writer.writerow(["タイトル変更あり",df_bool_match_titlechange.sum(), df_bool_not_match_titlechange.sum()])
      # writer.writerow(["収集以降作られたページ",df_bool_match_make_recently.sum(), df_bool_not_match_make_recently.sum()])




if __name__ == "__main__":    
    
    #list_handmatch_site = ['manabitimes.jp','univ-juken.com']
    list_handmatch_site = ['univ-juken.com']
    list_textname = ['kosen_biseki1']
    limit = '1'
  
    main(list_handmatch_site,list_textname,limit)