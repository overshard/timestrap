// TODO: Cleanup routes into a single function
riot.compile(function() {
    let currentPage = null;
    route('/entries..', function() {
        if (currentPage) {
            currentPage.unmount(true);
        }
        currentPage = riot.mount('div#main', 'entries')[0];
    });
    route('/clients..', function() {
        if (currentPage) {
            currentPage.unmount(true);
        }
        currentPage = riot.mount('div#main', 'clients')[0];
    });
    route('/reports..', function() {
        if (currentPage) {
            currentPage.unmount(true);
        }
        currentPage = riot.mount('div#main', 'reports')[0];
    });
    route.base('/');
    route.start(true);
    $('.routable').each(function(i, e) {
        $(this).on('click', function(e) {
            e.preventDefault();
            route($(this).attr('href'));
        });
    });
});