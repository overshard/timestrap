<template>
  <div id="app">
    <div class="navbar navbar-expand-sm navbar-dark bg-primary">
      <div class="container">
        <router-link
          :to="timesheet"
          class="navbar-brand">
          {{ site.NAME }}
        </router-link>
        <button
          class="navbar-toggler navbar-toggler-right"
          type="button"
          data-toggle="collapse"
          data-target="#navbarCollapse">
          <span class="navbar-toggler-icon"/>
        </button>
        <div
          id="navbarCollapse"
          class="collapse navbar-collapse">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link
                id="nav-timesheet"
                :to="timesheet"
                class="nav-link">
                <i class="fa fa-clock-o mr-1"/>
                Timesheet
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                id="nav-clients"
                :to="clients"
                class="nav-link">
                <i class="fa fa-address-book mr-1"/>
                Clients
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                id="nav-tasks"
                :to="tasks"
                class="nav-link">
                <i class="fa fa-tasks mr-1"/>
                Tasks
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                id="nav-reports"
                :to="reports"
                class="nav-link">
                <i class="fa fa-book mr-1"/>
                Reports
              </router-link>
            </li>
          </ul>
          <ul class="navbar-nav ml-auto">
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                data-toggle="dropdown">
                <i class="fa fa-user-circle mr-2"/>
                {{ username }}
              </a>
              <div class="dropdown-menu dropdown-menu-right">
                <a
                  :href="api"
                  class="dropdown-item"
                  target="_blank">
                  API Browser
                </a>
                <a
                  v-if="isStaff"
                  id="nav-admin-admin"
                  :href="admin"
                  class="dropdown-item"
                  target="_blank">
                  Admin
                </a>
                <a
                  id="nav-admin-logout"
                  :href="logout"
                  class="dropdown-item">
                  Logout
                </a>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <tracker/>
    <div class="container my-4">
      <router-view :id="'view-' + $route.name"/>
    </div>
  </div>
</template>


<script>
import Tracker from './tracker.vue';


export default {
  components: {
    Tracker,
  },
  data() {
    return {
      timesheet: timestrapConfig.CORE_URLS.TIMESHEET,
      clients: timestrapConfig.CORE_URLS.CLIENTS,
      tasks: timestrapConfig.CORE_URLS.TASKS,
      reports: timestrapConfig.CORE_URLS.REPORTS,
      username: timestrapConfig.USER.NAME,
      api: timestrapConfig.CORE_URLS.API,
      admin: timestrapConfig.CORE_URLS.ADMIN,
      logout: timestrapConfig.CORE_URLS.LOGOUT,
      site: timestrapConfig.SITE,
      isStaff: timestrapConfig.USER.IS_STAFF,
    };
  },
  methods: {
    submitSearch() {
      this.$router.push({
        name: 'reports',
        query: {
          search: this.search,
        },
      });
      this.bus.$emit('search');
    },
  },
};
</script>


<style lang="scss">
// Fix bootstrap v4 not using pointer on some objects
a,
button {
  cursor: pointer;
}

// Fix bootstrap v4 making some field invalid before input
input:required {
  border-color: #ccc !important;
  box-shadow: none !important;
}

// Make current active nav item more visible
.navbar-dark .navbar-nav .active > .nav-link,
.navbar-dark .navbar-nav .nav-link.active,
.navbar-dark .navbar-nav .nav-link.show,
.navbar-dark .navbar-nav .show > .nav-link {
  font-weight: bold;
}

#github {
  position: fixed;
  bottom: 5px;
  right: 15px;
  font-size: 2em;

  a {
    color: #000;
  }
}

.btn,
.export-select {
  font-size: .7em;
  line-height: 1.8em;
  letter-spacing: 1px;
  font-weight: bold;
  text-transform: uppercase;
}

// Remove arrow on the ellipsis icons on rows
.btn-icon {
  &::after {
    display: none;
  }
}
</style>
