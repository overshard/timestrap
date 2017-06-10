<template>
<div id="app">
    <div class="sidebar bg-primary">
        <div class="branding">
            <router-link class="display-4" v-bind:to="timesheet">
                Timestrap
            </router-link>
        </div>
        <div class="search">
            <div class="form-group">
                <form v-on:submit.prevent
                      v-on:submit="submitSearch">
                    <input v-model="search"
                           class="form-control rounded-0 border-0"
                           type="text"
                           placeholder="Search" />
                </form>
            </div>
        </div>
        <ul id="nav-app" class="nav flex-column">
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
            <li class="nav-item dropup">
                <a class="nav-link dropdown-toggle"
                    data-toggle="dropdown">
                    <img v-bind:src="global.user.gravatar_url"
                        width="30"
                        height="30"
                        class="mr-1" />
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
                        v-bind:href="admin">Admin</a>
                    <a id="nav-admin-logout"
                        class="dropdown-item"
                        target="_blank"
                        v-bind:href="logout">Logout</a>
                </div>
            </li>
        </ul>
        <timer />
    </div>
    <div class="content">
        <router-view v-bind:id="['component-' + $route.name]"
                        class="view"></router-view>
    </div>
</div>
</template>

<script>
const Timer = require('./timer.vue');

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
            logout: timestrapConfig.CORE_URLS.LOGOUT
        };
    },
    methods: {
        submitSearch() {
            // Use .push instead of .go to not reload entire page
            this.$router.go({
                name: 'reports',
                query: {
                    search: this.search
                }
            })
        }
    },
    components: {
        Timer
    }
};
</script>
