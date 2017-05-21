// TODO: Also don't use hotkeys 1, 2, 3 + alt, some systems use that to tab
$(document).keypress(function(e) {
    if (e.altKey) {
        switch (e.which) {
        case 49:
            route(timestrapConfig.CORE_URLS.ENTRIES);
            break;
        case 50:
            route(timestrapConfig.CORE_URLS.CLIENTS);
            break;
        case 51:
            route(timestrapConfig.CORE_URLS.TASKS);
            break;
        case 52:
            route(timestrapConfig.CORE_URLS.REPORTS);
            break;
        }
    }
});
