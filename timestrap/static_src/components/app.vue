<template>
<div id="app">
    <div class="navbar navbar-expand-sm navbar-dark bg-primary">
        <div class="container">
            <router-link class="navbar-brand" v-bind:to="timesheet">
                {{ site.NAME }}
            </router-link>
            <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarCollapse">
                <ul id="nav-app" class="navbar-nav">
                    <li class="nav-item">
                        <router-link id="nav-app-timesheet" class="nav-link" v-bind:to="timesheet">
                            <i class="fa fa-clock-o mr-1" aria-hidden="true"></i>
                            Timesheet
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link id="nav-app-clients" class="nav-link" v-bind:to="clients">
                            <i class="fa fa-address-book mr-1" aria-hidden="true"></i>
                            Clients
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link id="nav-app-tasks" class="nav-link" v-bind:to="tasks">
                            <i class="fa fa-tasks mr-1" aria-hidden="true"></i>
                            Tasks
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link id="nav-app-reports" class="nav-link" v-bind:to="reports">
                            <i class="fa fa-book mr-1" aria-hidden="true"></i>
                            Reports
                        </router-link>
                    </li>
                </ul>
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item dropdown dropdown-menu-right">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown">
                            {{ username }}
                        </a>
                        <div class="dropdown-menu">
                            <a id="nav-admin-api"
                               class="dropdown-item"
                               target="_blank"
                               v-bind:href="api">API Browser</a>
                            <a id="nav-admin-admin"
                               class="dropdown-item"
                               target="_blank"
                               v-if="this.$user.is_staff"
                               v-bind:href="admin">Admin</a>
                            <a id="nav-admin-logout"
                               class="dropdown-item"
                               v-bind:href="logout">Logout</a>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    <tracker></tracker>
    <div class="container my-4">
        <router-view v-bind:id="['component-' + $route.name]" class="view"></router-view>
    </div>
</div>
</template>


<script>
const Tracker = require('./tracker.vue');

export default {
    data () {
        return {
            timesheet: timestrapConfig.CORE_URLS.TIMESHEET,
            clients: timestrapConfig.CORE_URLS.CLIENTS,
            tasks: timestrapConfig.CORE_URLS.TASKS,
            reports: timestrapConfig.CORE_URLS.REPORTS,
            username: timestrapConfig.USER.NAME,
            api: timestrapConfig.CORE_URLS.API,
            admin: timestrapConfig.CORE_URLS.ADMIN,
            logout: timestrapConfig.CORE_URLS.LOGOUT,
            site: timestrapConfig.SITE
        };
    },
    methods: {
        submitSearch() {
            this.$router.push({
                name: 'reports',
                query: {
                    search: this.search
                }
            });
            this.bus.$emit('search');
        }
    },
    mounted() {
        moment.locale(timestrapConfig.SITE.LOCALE);
    },
    components: {
        Tracker
    }
};
</script>
