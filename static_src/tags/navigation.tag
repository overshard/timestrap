<navigation>
    <div class="navbar sticky-top navbar-toggleable-sm navbar-inverse bg-primary mb-4">
        <div class="container">
            <button class="navbar-toggler navbar-toggler-right"
                    type="button"
                    data-toggle="collapse"
                    data-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand" href={ timestrapConfig.CORE_URLS.ENTRIES }>
                Timestrap
            </a>
            <div id="nav" class="collapse navbar-collapse">
                <ul id="nav-app" class="navbar-nav mr-auto">
                    <virtual if={ timestrapConfig.USER }>
                        <virtual if={ perms && perms.view_entry }>
                            <li class="nav-item">
                                <a id="nav-app-entries"
                                   class="nav-link"
                                   href={ timestrapConfig.CORE_URLS.ENTRIES }>
                                    Timesheet
                                </a>
                            </li>
                        </virtual>
                        <virtual if={ perms && perms.view_client }>
                            <li class="nav-item">
                                <a id="nav-app-clients"
                                   class="nav-link"
                                   href={ timestrapConfig.CORE_URLS.CLIENTS }>
                                    Clients
                                </a>
                            </li>
                        </virtual>
                        <virtual if={ perms && perms.view_task }>
                            <li class="nav-item">
                                <a id="nav-app-tasks"
                                   class="nav-link"
                                   href={ timestrapConfig.CORE_URLS.TASKS }>
                                    Tasks
                                </a>
                            </li>
                        </virtual>
                        <li class="nav-item">
                            <a id="nav-app-reports"
                               class="nav-link"
                               href={ timestrapConfig.CORE_URLS.REPORTS }>
                                Reports
                            </a>
                        </li>
                    </virtual>
                </ul>
                <ul id="nav-admin" class="navbar-nav">
                    <virtual if={ timestrapConfig.USER }>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle"
                               data-toggle="dropdown">
                                { timestrapConfig.USER.NAME }
                            </a>
                            <div class="dropdown-menu dropdown-menu-right">
                                <a id="nav-admin-api"
                                   class="dropdown-item"
                                   href={ timestrapConfig.CORE_URLS.API }>
                                    API Browser
                                </a>
                                <a id="nav-admin-admin"
                                   class="dropdown-item"
                                   href={ timestrapConfig.CORE_URLS.ADMIN }>
                                    Admin
                                </a>
                                <a id="nav-admin-logout"
                                   class="dropdown-item"
                                   href={ timestrapConfig.CORE_URLS.LOGOUT }>
                                    Logout
                                </a>
                            </div>
                        </li>
                        <li class="nav-item" if={ user }>
                            <img src={ user.gravatar_url }
                                 width="32"
                                 height="32"
                                 class="rounded my-1 ml-2" />
                        </li>
                    </virtual>
                    <virtual if={ !timestrapConfig.USER }>
                        <li class="nav-item">
                            <a id="nav-admin-login"
                               class="nav-link"
                               href={ timestrapConfig.CORE_URLS.LOGIN }>
                                Login
                            </a>
                        </li>
                    </virtual>
                </ul>
            </div>
        </div>
    </div>

    <script type="es6">
        getPerms = function() {
            prefetch.PERMISSIONS.then(function(data) {
                let perms = Object;
                $.each(data.results, function(i, perm) {
                    perms[perm.codename] = perm;
                });
                this.update({
                    perms: perms
                });
            }.bind(this));
        }.bind(this);


        getUser = function() {
            prefetch.USER.then(function(data) {
                this.update({
                    user: data
                });
            }.bind(this));
        }.bind(this);


        this.on('mount', function() {
            if (timestrapConfig.USER) {
                getPerms();
                getUser();
            }
        }.bind(this));
    </script>
</navigation>
