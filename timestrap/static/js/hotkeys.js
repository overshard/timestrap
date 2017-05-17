// TODO: Pull locations from django's url system
// TODO: Also don't use hotkeys 1, 2, 3 + alt, some systems use that to tab
$(document).keypress(function(e) {
    if (e.altKey) {
        switch (e.which) {
            case 49:
                window.location = '/clients/';
                break;
            case 50:
                window.location = '/entries/';
                break;
            case 51:
                window.location = '/reports';
                break;
        }
    }
});