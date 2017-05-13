function readMyFile (){
	var file = new FileReader();
	file.readAsText("/stop-word-list.txt", "utf8");
	return file.result;
}

// function getAsText(readFile) {
// 	var file = new FileReader();
// 	file.readAsText(readFile, "UTF-8");
// }


// var text = getAsText("stop-word-list.txt")
console.log(readMyFile);
