db = connect("10.120.28.55:27017/news");

var showCursorItems = function(cursor){
	while (cursor.hasNext) {
   		printjson(cursor.next());
	}
}


cursor = db.art_keywords.find({'keywords':{$exists:false}});
showCursorItems(cursor);

// var c = db.news.find({'counted':'true'},{'_id':1, 'wordset':1}).limit(10);
// c.forEach(
// 		function(this)
// 			{
// 				db.art_wordset.insertOne({'_id':this._id},{'wordset':this.wordset});
// 			}
// 		);