<template>
<div id="app" class="container-fluid">
    <div class="row">
        <div class="sidebar-row bg-primary col-3">
            <div class="sidebar">
                <router-link class="display-4" :to="timesheet">
                    Timestrap
                </router-link>
                <ul id="nav-app" class="nav flex-column">
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
                    <li class="nav-item dropup">
                        <a class="nav-link dropdown-toggle"
                            data-toggle="dropdown">
                            {{ username }}
                        </a>
                        <div class="dropdown-menu">
                            <a id="nav-admin-api"
                                class="dropdown-item"
                                :href="api">
                                API Browser
                            </a>
                            <a id="nav-admin-admin"
                                class="dropdown-item"
                                :href="admin">
                                Admin
                            </a>
                            <a id="nav-admin-logout"
                                class="dropdown-item"
                                :href="logout">
                                Logout
                            </a>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        <div class="col-9 my-3">
            <router-view class="view"></router-view>
        </div>
    </div>
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
            username: timestrapConfig.USER.NAME,
            api: timestrapConfig.CORE_URLS.API,
            admin: timestrapConfig.CORE_URLS.ADMIN,
            logout: timestrapConfig.CORE_URLS.LOGOUT
        };
    }
};
</script>
