<template>
<div id="app">
    <div class="navbar sticky-top navbar-toggleable-sm navbar-inverse bg-primary mb-4">
        <div class="container">
            <button class="navbar-toggler navbar-toggler-right"
                    type="button"
                    data-toggle="collapse"
                    data-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <router-link class="navbar-brand" :to="timesheet">
                Timestrap
            </router-link>
            <div id="nav" class="collapse navbar-collapse">
                <ul id="nav-app" class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="timesheet">
                            Timesheet
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="clients">
                            Clients
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="tasks">
                            Tasks
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <a id="nav-app-reports"
                            class="nav-link">
                            Reports
                        </a>
                    </li>
                </ul>
                <ul id="nav-admin" class="navbar-nav">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle"
                            data-toggle="dropdown">
                            {{ username }}
                        </a>
                        <div class="dropdown-menu dropdown-menu-right">
                            <a id="nav-admin-api"
                                class="dropdown-item">
                                API Browser
                            </a>
                            <a id="nav-admin-admin"
                                class="dropdown-item">
                                Admin
                            </a>
                            <a id="nav-admin-logout"
                                class="dropdown-item">
                                Logout
                            </a>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    <router-view class="view"></router-view>
</div>
</template>

<script>
export default {
    data () {
        return {
            timesheet: timestrapConfig.CORE_URLS.TIMESHEET,
            clients: timestrapConfig.CORE_URLS.CLIENTS,
            tasks: timestrapConfig.CORE_URLS.TASKS,
            reports: timestrapConfig.CORE_URLS.REPORTS,
            username: timestrapConfig.USER.NAME
        };
    }
};
</script>
