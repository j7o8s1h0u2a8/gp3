# gp3
for final project

OK: getCNN, getBBC, getNYT
getVOA ... 景曄
getABC ... 建榮

<h2>變數命名</h2>
新聞網首頁 main_url
分類標籤 tag/tags
分類連結 cat_url
標題 art_title
連結 art_url
日期 art_date
來源 art_src
段落 art_paras
段數 numPara
全文 art_body

<h2>Functions</h2>
getCatLinks()
- 回傳該新聞網所有分類(子項目)連結清單 catList

getArticlesList(cat_url)
- 回傳該分類下所有新聞清單 articlesList
- art_title, art_url, art_src

getArticle(art_url)
- 給單一新聞連結回傳該文章內容 art_dict
- art_title, art_url, art_date, art_src, art_paras

jsonOut(inputList)
-以json格式輸出，檔名 date_src_output.json

[此function先保留]
addContent(articlesList)
- 給某分類下之新聞清單，回傳所有art_dict集合 arts_dictList
