// Globals
var currentPage = null;
var search = null;


// Route Helpers
function goRoute(newPage) {
    if (currentPage) currentPage.unmount(true);
    currentPage = riot.mount('div#main', newPage)[0];
}

function getRiotUrl(tag) {
    let configUrlName = tag.toUpperCase();
    let url = timestrapConfig.CORE_URLS[configUrlName];
    return url.substring(0, url.length-1) + '..';  // The `..` matches everything after
}

function skipRouter(routeName) {
    let routeNameUpper = routeName.toUpperCase();
    route(getRiotUrl(routeNameUpper), function() {
        window.location = timestrapConfig.CORE_URLS[routeNameUpper];
    });
}


// Routes
route(getRiotUrl('entries'), function() {
    goRoute('entries');
});
route(getRiotUrl('clients'), function() {
    goRoute('clients');
});
route(getRiotUrl('tasks'), function() {
    goRoute('tasks');
});
route(getRiotUrl('reports'), function() {
    let query = route.query();
    if (query.search) {
        search = query.search;
    }
    goRoute('reports');
});


// These routes aren't in our SPA
skipRouter('admin');
skipRouter('api');
skipRouter('logout');
// Fix for login redirect since it's not in the SPA but loads router.js
if (window.location.path !== timestrapConfig.CORE_URLS['login']) {
    skipRouter('login');
}


// Routing start
route.base('/');
route.start(true);
