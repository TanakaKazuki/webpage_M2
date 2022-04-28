from turtle import title
import MeCab
import math

mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

text = '解析したい漸化式'
mecab.parse('')#文字列がGCされるのを防ぐ
node = mecab.parseToNode(text)
while node:
    #単語を取得
    word = node.surface
    #品詞を取得
    pos = node.feature.split(",")[1]
    print('{0} , {1}'.format(word, pos))
    #次の単語に進める
    node = node.next
    
text = "解析したい漸化式を入れる。"
m = MeCab.Tagger("-Ochasen /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
m.parse('')
nouns = [line for line in m.parse(text).splitlines()
  if "名詞" in line.split()[-1]]

terms = []
for str in nouns:
  terms.append(str.split()[0])

print(terms)
   
   #print()
   #print('')
   
m = MeCab.Tagger("-Ochasen /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
m.parse('')  
terms_page = []
    # 分けてノードごとにする
sentence = "解析したい漸化式を入れる。"
node = m.parseToNode(sentence)
terms = []
select_conditions = ['名詞']
       
while node:
  # 単語
  term = node.surface
  # 品詞
  pos = node.feature.split(',')[0]
  # もし品詞が条件と一致してたら
  if pos in select_conditions:
    terms.append(term)
  node = node.next
  # 連結
terms_page.extend(terms)
terms_page = list(set(terms_page))

print(terms_page)


text = "解析したい漸化式を入れる。"
m = MeCab.Tagger("-Ochasen /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

nouns = [line for line in m.parse(text).splitlines()
               if "固有名詞" in line.split()[-1]]


for str in nouns:
   print(str.split())
   


mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
text = input("解析する漸化式,部分積分を入力してください：")
result = mecab.parse(text)
print(result)
lines = result.split('\n')
nounAndVerb = []#「名詞」と「動詞」を格納するリスト
for line in lines:
    feature = line.split('\t')
    if len(feature) == 2: #'EOS'と''を省く
        info = feature[1].split(',')
        hinshi = info[0]
        if hinshi in ('名詞', '固有名詞'):
            nounAndVerb.append(info[6])

print(nounAndVerb)