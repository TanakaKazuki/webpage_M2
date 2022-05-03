import csv
from pathlib import Path
import os
from re import A
import pandas as pd


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
    
    df_handmatch_neo = eval(df_match_result,df_handmatch)
    
    #df_handmatch中のページが、df_match_resultにあるかどうか
    ##タイトルは変わってるため、URLで判断
    
    df_handmatch_neo.to_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/handmatch_eval/eval_handmatch_'+text_name+'_'+site_name+'_'+limit+'.csv',sep=',',index=None) 
    df_handmatch_neo.to_excel('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/handmatch_eval/eval_handmatch_'+text_name+'_'+site_name+'_'+limit+'.xlsx') 
    
    
    
    
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
    
  
  
        

          
    



if __name__ == "__main__":    
    
    #list_handmatch_site = ['manabitimes.jp','univ-juken.com']
    list_handmatch_site = ['univ-juken.com']
    list_textname = ['kosen_biseki1']
    limit = '1'
  
    main(list_handmatch_site,list_textname,limit)