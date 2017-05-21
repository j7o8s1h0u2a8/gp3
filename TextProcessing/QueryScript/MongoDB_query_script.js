// 依來源分類算篇數
db.news.aggregate({$group:{_id:'$source', count:{$sum:1}}},{$sort:{'count':1}});
db.news.aggregate({$group:{_id:{src:'$source',tag:'$counted'},count: {$sum:1}}}, {$sort:{'_id':1}});

// 依等級分類算篇數
db.news.aggregate({$group:{_id:'$level', count:{$sum:1}}},{$sort:{'count':1}});

// 查詢counted欄位標記為Processing...的文章
db.news.find({'source':'NYT', 'counted':'Processing...'}).size();

// 查詢已清洗資料筆數
db.news.find({'source':'NYT', 'counted':'true'}).size();

// 查詢尚未作wc的資料筆數
db.news.find({'source':'NYT', 'counted':{$exists:false}}).size();
db.news.find({'counted':{$exists:false}}).size();
db.news.find({'counted':'Processing...'}).size();

// 查詢Server連線狀況
db.serverStatus().connections

// 尋找重複兩次_id的文件，刪除其中一筆
db.art_keywords.aggregate({{$group:{_id:'$_id', resultIds:{$addToSet:'$_id'}, count:{$sum:1}}}, {$match:{count:{$gt:1}}}}, {allowDiskUse: true}).forEach(
	function(doc){
	  db.art_keywords.deleteOne({_id:{$in:doc.resultIds}});
	});

// 尋找相同url(or title)的文件，刪到剩一筆
db.news.aggregate([{$group:{_id:'$url', resultIds:{$addToSet:'$_id'}, count:{$sum:1}}}, {$match:{count:{$gt:1}}}], {allowDiskUse: true});
.forEach(
	function(doc){
	  doc.resultIds.shift();
	  db.news.remove({_id:{$in:doc.resultIds}});
	});
	
// 移除無content欄位文章
db.news.remove({'content':{$exists:false}}).size();

// 查詢content數<4的文章
db.news.find({'$where':'return Object.keys(this.content).length<4'});
db.news.find({'$where':'return Object.keys(this.content).length>50'});

db.word_dict.find({'IDF':{$exists:false}}).size()

// 查詢已提取關鍵字的筆數
db.art_keywords.find({'keywords':{$exists:true}}).size();
db.art_keywords.find({'keywords':{$exists:true}},{'_id':1, 'keywords':1});

// 查詢第1.2段相同的文章
db.news.aggregate({"$redact":{"$cond":{{"$eq": {"$content.1", "$content.2"}}, "$$KEEP", "$$PRUNE"}}})