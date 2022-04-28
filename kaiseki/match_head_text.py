import re
import csv
from pathlib import Path
from lxml import html
import os

import pandas as pd

if __name__ == "__main__":
    """読み込むファイル名の指定"""
    #path
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_atarimae.biz.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_batapara.com.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_eman-physics.net.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_examist.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_fromhimuka.com.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_hiraocafe.com.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_hooktail.sub.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_manabitimes.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_math-fun.net.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_math-juken.com.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_opencourse.doshisha.ac.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_racco.mikeneko.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_ramenhuhu.com.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_rikeilabo.com.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_tau.doshisha.ac.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_ufcpp.net.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_univ-juken.com.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_univ-study.net.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_w3e.kanazawa-it.ac.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_www.geisya.or.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_www.maroon.dti.ne.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_www.momoyama-usagi.com.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_www.sci.hokudai.ac.jp.csv
    #/Users/kazuki/Desktop/research/data_1619/kaiseki/html_data/correspondence_list_yorikuwa.com.csv
    df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/html_data/correspondence_list_yorikuwa.com.csv',header=None)
    filename = df[0]
    fileurl = df[1]
    print(filename.head(50))
    print(fileurl.head(50))
    
    #'atarimae.biz'
    #'batapara.com'
    #'eman-physics.net'
    #'examist.jp'
    #'fromhimuka.com'
    #'hiraocafe.com'
    #'hooktail.sub.jp'
    #'manabitimes.jp'
    #'math-fun.net'
    #'math-juken.com'
    #'racco.mikeneko.jp'
    #'ramenhuhu.com'
    #'tau.doshisha.ac.jp'
    #'ufcpp.net'
    #'univ-juken.com'
    #'univ-study.net'
    #'w3e.kanazawa-it.ac.jp'
    #'www.geisya.or.jp'
    #'www.maroon.dti.ne.jp'
    #'www.momoyama-usagi.com'
    #'www.sci.hokudai.ac.jp'
    #'yorikuwa.com'
    sitename ='yorikuwa.com'

    main(filename,fileurl,sitename)