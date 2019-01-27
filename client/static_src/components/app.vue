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

  <div class="navbar-mobile">
    <div class="navbar-mobile-title">
      {{ $route.meta.title }}
    </div>
    <div class="navbar-mobile-toggle" data-toggle="collapse" data-target=".navbar">
      <icon :icon="['fas', 'bars']" class="mr-1"/>
    </div>
  </div>

  <div class="navbar navbar-dark bg-dark">
    <router-link :to="timesheet" class="navbar-brand">
      {{ site.NAME }}
    </router-link>
    <ul class="navbar-nav flex-grow-1">
      <li v-if="$perms.view_entry" class="nav-item">
        <router-link
          id="nav-timesheet"
          :to="timesheet"
          class="nav-link">
          <icon :icon="['fas', 'clock']" class="mr-1"/>
          Timesheet
        </router-link>
      </li>
      <li v-if="$perms.view_project" class="nav-item">
        <router-link
          id="nav-projects"
          :to="projects"
          class="nav-link">
          <icon :icon="['fas', 'briefcase']" class="mr-1"/>
          Projects
        </router-link>
      </li>
      <li v-if="$perms.view_client" class="nav-item">
        <router-link
          id="nav-clients"
          :to="clients"
          class="nav-link">
          <icon :icon="['fas', 'address-book']" class="mr-1"/>
          Clients
        </router-link>
      </li>
      <li v-if="$perms.view_task" class="nav-item">
        <router-link
          id="nav-tasks"
          :to="tasks"
          class="nav-link">
          <icon :icon="['fas', 'tasks']" class="mr-1"/>
          Tasks
        </router-link>
      </li>
      <li v-if="$perms.view_entry" class="nav-item">
        <router-link
          id="nav-reports"
          :to="reports"
          class="nav-link">
          <icon :icon="['fas', 'book']" class="mr-1"/>
          Reports
        </router-link>
      </li>
    </ul>
    <ul class="navbar-nav">
      <li class="nav-item dropup">
        <a
          id="nav-user"
          href="#"
          class="nav-link dropdown-toggle"
          data-toggle="dropdown">
          <icon :icon="['fas', 'user-circle']" class="mr-1"/>
          {{ username }}
        </a>
        <div class="dropdown-menu">
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

  <div class="page">
    <tracker/>

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
import $ from 'jquery';

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
  padding: 0;
}

.bg-dark {
  background-color: rgb(19, 15, 11) !important;
}

.bg-light {
  background-color: rgb(252, 248, 243) !important;
}

.text-muted {
  color: #99a4ae !important
}

// Loading styles
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

// Github icon
#github {
  position: fixed;
  bottom: 5px;
  right: 15px;
  font-size: 2em;
}

// Remove arrow on the ellipsis icons on rows
.btn-icon {
  &::after {
    display: none;
  }
}

.navbar {
  position: fixed;
  left: 0;
  width: 200px;
  top: 0;
  bottom: 0;
  padding: 1rem;
  padding: 0;
  flex-direction: column;
}

.navbar-brand {
  padding: 1rem 0;
  display: block;
  font-weight: bold;
  margin-right: 0;
  width: 200px;
  text-align: center;
}

.navbar-nav {
  flex-direction: column !important;
}

.nav-link {
  width: 200px;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
}

.nav-link.active {
  background: #222;
}

.navbar .dropdown-menu {
  width: 200px;
  border-radius: 0;
  border: 0;
  margin: 0;
}

.page {
  width: calc(100% - 200px);
  margin-left: 200px;
}

.navbar-mobile {
  display: none;
}

.navbar-mobile-toggle {
  cursor: pointer;
}

@media (max-width: 768px) {
  .navbar {
    display: none;
    z-index: 3;
  }

  .navbar.show {
    display: block;
  }

  .navbar-mobile {
    display: flex;
    background-color: black !important;
    color: white;
    padding: .5rem 1rem;
    font-size: 2rem;
    justify-content: center;
    align-items: center;
  }

  .navbar-mobile-title {
    font-size: 1.5rem;
    flex-grow: 1;
    text-align: center;
  }

  .page {
    width: 100%;
    margin-left: 0;
  }
}
</style>
