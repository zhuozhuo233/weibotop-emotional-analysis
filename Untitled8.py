#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[18]:


import requests
import json
from lxml import etree
from bs4 import BeautifulSoup

headers={
    'Cookie':'SINAGLOBAL=5067277944781.756.1539012379187; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFXAgGhhYE-bL1UlBNsI6xh5JpX5KMhUgL.Foqce0eN1h2cehB2dJLoIEXLxK-L1h5LB-eLxK-L1h5LB-eLxK-L1K5L1heLxKBLBonL1h.LxKMLBKzL1KMt; UOR=jx3.xoyo.com,widget.weibo.com,login.sina.com.cn; ALF=1665190926; SSOLoginState=1633654926; SCF=AjnY75MXDIg2Sev-TVKQBdyuwLa-mrIYwFgLkjivnwGqe4HMR8MVkSqyfw315Fic7gc1c38G1W-RUtxrwPqe0qY.; SUB=_2A25MW-jeDeRhGeBI6FEW-C_KyziIHXVvEV0WrDV8PUNbmtAKLUzhkW9NRppHJg76K77LtSOxPlpC13YygxcK3EKM; _s_tentry=login.sina.com.cn; Apache=441836365226.03375.1633654927612; ULV=1633654927618:48:1:1:441836365226.03375.1633654927612:1632876696485',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
}

def get_top():
    url = "https://s.weibo.com/top/summary"
    r = requests.get(url,headers=headers)
#     print(r.text)
#     print(r.status_code)
    html_xpath = etree.HTML(r.text)
    data = html_xpath.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr[1]/td[2]')
    num = 1
    for tr in (data):
        print('-------------')
        title = tr.xpath('./a/text()')
        hot_score = tr.xpath('./span/text()')
        href = tr.xpath('./a/@href')
        if hot_score:
            print('{} {} hot: {}'.format(num,title[0],hot_score[0]))
            request = get_weibo_list('https://s.weibo.com/weibo?q=%23'+tittle[0]+'%23&Refer=top')
            print(result)
            num += 1
            
def get_weibo_list(url):
    r = requests.get(url,headers=headers)
    
    bs = BeautifulSoup(r.text)
    body = bs.body
    div_m_main = body.find('div',attrs={'class':'m-main'})
    div_m_wrap = div_m_main.find('div',attrs={'class':'m-wrap'})
    div_m_con_l = div_m_wrap.find('div',attrs={'class':'m-con-l'})
    data_div = div_m_con_l.findAll('div',attrs={'class':'card-wrap','action-type':'feed_list_item'})
    
    weibo_list = []
    for each_div in data_div:
        div_card = each_div.find('div',attrs={'class':'card'})
        div_card_feed = div_card.find('div',attrs={'class':'card-feed'})
        div_content = div_card_feed.find('div',attrs={'class':'content'})
        
        p_feed_list_content = div_content.find('p',attrs={'class':'txt','node-type':'feed_list_content'})
        content_text = p_feed_list_content.get_text()
        
        p_feed_list_content_full = div_content.find('p',attrs={'class':'txt','node-type':'feed_list_content_full'})
        if p_feed_list_content_full:
            content_text = p_feed_list_content_full.get_text()
            
        weibo_list.append(content_text.strip())
        
    return weibo_list
            
            


# In[19]:


get_top()


# In[20]:


#????????????????????????????????????????????????
cont = get_weibo_list('https://s.weibo.com/weibo?q=%23%E6%AD%A6%E7%A3%8A%E7%BB%9D%E6%9D%80%23&Refer=top')
cont


# In[29]:


import re
import jieba
#????????????????????????????????????????????????????????????????????????????????????
def process(text):
    #??????url
    text = re.sub("(https?|ftp|file)://[-A-Za-z0-9+&@#/%=~_|]"," ",text)
    #??????@xxx(?????????)
    text = re.sub("@.+?( |$)", " ", text)
    #??????{%xxx%}????????????????????????????????????
    text = re.sub("\{%.+?%\}", " ",text)
    #??????#xx#??????????????????
    text = re.sub("\{#.+?#\}", " ", text)
    #?????????xx???(????????????????????????????????????????????????)
    text = re.sub("???.+????", " ", text)
    #?????????????????????
    text = re.sub('\u200b'," ",text)
                  
    #??????
    words = [w for w in jieba.lcut(text) if w.isalpha()]
                
    result = " ".join(words)
    return result
                  


# In[30]:


#?????????????????????????????????????????????
pro_cont = []
for each in cont:
    pro_cont.append(process(each))
pro_cont


# In[31]:


#?????????????????????????????????????????????pd???DataFrame??????
import pandas as pd
df_title = pd.DataFrame(pro_cont,columns=['words'])
df_title.head(5)


# In[35]:


#??????????????????????????????????????????????????????????????????????????????????????????id,????????????????????????
#train.txt??????????????? test.txt???????????????

#???????????????
stopwords = []
with open('stopwords.txt','r',encoding='utf-8') as f:
    for w in f:
        stopwords.append(w.strip())  #??????????????????
stopwords  #???????????????


# In[38]:


# ?????????????????????????????????
# ???????????????????????????????????????????????????????????????????????????????????????id???????????????????????????
# train.txt??????????????????test.txt???????????????
# ????????????????????????????????????????????????????????????
# ??????????????????????????????????????????????????????????????????????????? 1??????????????????0???????????????


# In[37]:


#?????????????????????????????????????????????????????????
def load_corpus(path):
    data = []
    with open(path,'r',encoding='utf8') as f:
        for line in f:
            [_,sentiment,content] = line.split(',',2) #????????????
            #?????????????????????process????????????????????????
            content = process(content)
            data.append((content,int(sentiment)))
    return data


# In[39]:


#??????????????????????????????DataFrame???????????????
import pandas as pd
train_data = load_corpus('train.txt')
test_data = load_corpus('test.txt')

df_train = pd.DataFrame(train_data,columns=["words","label"])
df_test = pd.DataFrame(test_data,columns=["words","label"])
df_train.head(2)


# In[40]:


#???BOW ?????????????????????????????????
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(token_pattern='\[?\w+\]?',stop_words=stopwords)
X_train = vectorizer.fit_transform(df_train["words"])
y_train = df_train["label"]
print(type(X_train),X_train.shape)


# In[44]:


#???BOW?????????????????????????????????
X_test = vectorizer.transform(df_test["words"])
y_test = df_test["label"]


# In[45]:


#??????????????????????????????
from sklearn.naive_bayes import MultinomialNB
#?????????
clf = MultinomialNB()
#???????????????????????????
clf.fit(X_train,y_train)


# In[46]:


#????????????????????????????????????
y_pred = clf.predict(X_test)
print(y_pred)


# In[47]:


#?????????????????????
from sklearn import metrics

print(metrics.classification_report(y_test,y_pred))
print("?????????:",metrics.accuracy_score(y_test,y_pred))
auc_score = metrics.roc_auc_score(y_test,y_pred)  #?????????AUC
print("AUC:",auc_score)


# In[52]:


#????????????????????????????????????????????????????????????????????????
#???BOW????????????????????????
x = vectorizer.transform(df_title['words'])
#??????
y_title = clf.predict(x)
#print(y_pred)
#??????numpy????????????????????????
import numpy as np
title = "????????????"
print(title,'????????????????????????',np.mean(y_title))


# In[53]:


#????????????
import pickle
with open('./mnb_model.pkl','wb') as f:
    pickle.dump(clf,f)


# In[54]:


#???????????????????????????
with open('./mnb_model.pkl','rb') as f:
    save_clf = pickle.load(f)
    
#???????????????,????????????
save_clf.predict(x)
import numpy as np
title = "????????????"
print(title,'?????????????????????:',np.mean(y_title))


# In[ ]:




