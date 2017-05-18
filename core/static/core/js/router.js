riot.compile(function() {
    // Route helpers
    let currentPage = null;
    function goRoute(newPage) {
        if (currentPage) currentPage.unmount(true);
        currentPage = riot.mount('div#main', newPage)[0];
    }
    function getRiotUrl(tag) {
        let configUrlName = tag.toUpperCase();
        let url = timestrapConfig.CORE_URLS[configUrlName]
        return url.substring(0, url.length-1) + '..';  // The `..` matches everything after
    }

    // Routes
    route(getRiotUrl('entries'), function() {
        goRoute('entries');
    });
    route(getRiotUrl('clients'), function() {
        goRoute('clients');
    });
    route(getRiotUrl('reports'), function() {
        goRoute('reports');
    });

    // Fix these routes to use the config url system or avoid the router
    route('/api..', function() {
        window.location = '/api/';
    });
    route('/admin..', function() {
        window.location = '/admin/';
    });
    route('/logout..', function() {
        window.location = '/logout/';
    });
    route('/', function() {
        window.location = '/';
    });

    // Routing start
    route.base('/');
    route.start(true);
});