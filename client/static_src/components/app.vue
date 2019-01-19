<template>
  <div id="app">
    <transition name="fade">
      <div
        v-if="!doneLoading"
        id="loading"
        class="progress bg-dark">
        <div
          :style="'width:' + loadingPercent + '%;'"
          class="progress-bar bg-primary"/>
      </div>
    </transition>

    <toast></toast>

    <div class="navbar navbar-expand-sm navbar-dark bg-dark">
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
                <icon
                  :icon="['fas', 'clock']"
                  class="mr-1"/>
                Timesheet
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                id="nav-projects"
                :to="projects"
                class="nav-link">
                <icon :icon="['fas', 'briefcase']" class="mr-1"/>
                Projects
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                id="nav-clients"
                :to="clients"
                class="nav-link">
                <icon
                  :icon="['fas', 'address-book']"
                  class="mr-1"/>
                Clients
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                id="nav-tasks"
                :to="tasks"
                class="nav-link">
                <icon
                  :icon="['fas', 'tasks']"
                  class="mr-1"/>
                Tasks
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                id="nav-reports"
                :to="reports"
                class="nav-link">
                <icon
                  :icon="['fas', 'book']"
                  class="mr-1"/>
                Reports
              </router-link>
            </li>
          </ul>
          <ul class="navbar-nav ml-auto">
            <li class="nav-item dropdown">
              <a
                id="nav-user"
                class="nav-link dropdown-toggle"
                data-toggle="dropdown">
                <icon
                  :icon="['fas', 'user-circle']"
                  class="mr-1"/>
                {{ username }}
              </a>
              <div class="dropdown-menu dropdown-menu-right">
                <a
                  id="nav-user-api"
                  :href="api"
                  class="dropdown-item"
                  target="_blank">
                  API Browser
                </a>
                <a
                  v-if="isStaff"
                  id="nav-user-admin"
                  :href="admin"
                  class="dropdown-item"
                  target="_blank">
                  Admin
                </a>
                <a
                  id="nav-user-logout"
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
    <div id="github">
      <a
        href="https://github.com/overshard/timestrap"
        target="_blank">
        <icon
          :icon="['fas', 'code-branch']"
          class="mr-1 text-muted"/>
      </a>
    </div>
  </div>
</template>


<script>
import {mapGetters} from 'vuex';

import Tracker from './tracker.vue';
import Toast from './toast.vue';


export default {
  components: {
    Tracker,
    Toast,
  },
  data() {
    return {
      timesheet: timestrapConfig.CORE_URLS.TIMESHEET,
      projects: timestrapConfig.CORE_URLS.PROJECTS,
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
  computed: {
    ...mapGetters([
      'loadingPercent',
      'doneLoading',
    ]),
  },
};
</script>


<style lang="scss">
body {
  background-color: rgb(255, 254, 252);
}

// Fix bootstrap v4 not using pointer on some objects
a,
button {
  cursor: pointer;
}

// Fix bootstrap v4 making some field invalid before input
input:required {
  border-color: #ccc !important;
}

#loading {
  height: 3px;
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;
  right: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity .5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
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

.bg-dark {
  background-color: rgb(19, 15, 11) !important;
}
</style>
