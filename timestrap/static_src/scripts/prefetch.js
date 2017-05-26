// Grab all the base data on start so pages load faster
(function(window) {
    window.prefetch = window.prefetch || {};
    prefetch = {
        USER:        quickFetch(timestrapConfig.USER.URL),
        PERMISSIONS: quickFetch(timestrapConfig.API_URLS.PERMISSIONS)
        // USERS:       quickFetch(timestrapConfig.API_URLS.USERS),
        // PROJECTS:    quickFetch(timestrapConfig.API_URLS.PROJECTS),
        // CLIENTS:     quickFetch(timestrapConfig.API_URLS.CLIENTS),
        // TASKS:       quickFetch(timestrapConfig.API_URLS.TASKS),
    };
})(window);
