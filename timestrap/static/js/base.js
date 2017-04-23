// Promote a user to the front of a list
function promote(userId, arr) {
	var newArr = arr;

    for (var i = 0; i < newArr.length; i++) {
        if (newArr[i].id === userId) {
            var a = newArr.splice(i, 1);
            newArr.unshift(a[0]);
            break;
        }
    }

	return newArr;
}
