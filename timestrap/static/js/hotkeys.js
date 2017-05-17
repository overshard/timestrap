// TODO: Pull locations from django's url system
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