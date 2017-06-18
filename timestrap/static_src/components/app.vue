<template>
<div id="app">
    <div class="navbar navbar-toggleable-md navbar-inverse bg-primary">
        <div class="container">
            <router-link class="navbar-brand" v-bind:to="timesheet">
                Timestrap
            </router-link>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav">
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
                    <li class="nav-item">
                        <router-link id="nav-app-reports" class="nav-link" v-bind:to="invoices">
                            <i class="fa fa-credit-card-alt mr-1" aria-hidden="true"></i>
                            Invoices
                        </router-link>
                    </li>
                </ul>
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item dropdown dropdown-menu-right">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown">
                            {{ username }}
                        </a>
                        <div class="dropdown-menu">
                            <a id="nav-admin-api" class="dropdown-item" target="_blank" v-bind:href="api">API Browser</a>
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
            </div>
        </div>
    </div>
    <div class="bg-faded py-2">
        <div class="container">
            <div class="row">
                <div class="col-sm-8">
                    <timer></timer>
                </div>
                <div class="col-sm-4 text-right">
                    <form v-on:submit.prevent v-on:submit="submitSearch">
                        <input class="form-control form-control-sm" type="text" placeholder="Search by project, client, or entry" v-model="search" />
                    </form>
                </div>
            </div>
        </div>
    </div>
    <div class="container my-4">
        <router-view v-bind:id="['component-' + $route.name]" class="view"></router-view>
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
            invoices: timestrapConfig.CORE_URLS.INVOICES,
            username: timestrapConfig.USER.NAME,
            api: timestrapConfig.CORE_URLS.API,
            admin: timestrapConfig.CORE_URLS.ADMIN,
            logout: timestrapConfig.CORE_URLS.LOGOUT
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
    components: {
        Timer
    }
};
</script>
