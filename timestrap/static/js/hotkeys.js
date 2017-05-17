$(document).keypress(function(e) {
    console.log('keypress');
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