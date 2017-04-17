getArticle(art_url)
-給單一新聞連結回傳該文章內容 art_dict

v標題 art_title
v連結 art_url
v日期 art_date
v來源 art_src
v段落 art_paras
段數 numPara
全文 art_body

getCatLinks()
-回傳該新聞網所有分類(子項目)連結清單 catList

新聞網首頁 main_url
標籤 tag/tags

getArticlesList(cat_url)
-回傳該分類下所有新聞清單 articlesList
cat_url 分類連結
art_info (art_title, art_url, art_src)

addContent(articlesList)
-給某分類下之新聞清單，回傳所有art_dict集合 arts_dictList

jsonOut(inputList)
-以json格式輸出，檔名 date_src_output.json