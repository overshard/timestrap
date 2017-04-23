function appendQuery(url) {
    let location = window.location.href;
    location = location.split('?');

    if (location.length === 2 && !url.includes(location[1])) {
        if (url.split('?').length === 2) {
            url = url + '&' + location[1];
        } else {
            url = url + '?' + location[1];
        }
    }

    return url;
}
