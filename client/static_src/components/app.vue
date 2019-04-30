<template>
<div id="app">
  <transition name="fade">
    <div v-if="!doneLoading" id="loading" class="progress">
      <div
        :style="'width:' + loadingPercent + '%;'"
        class="progress-bar bg-primary"/>
    </div>
  </transition>

  <toast></toast>

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
          <icon :icon="['fas', 'clock']" class="fa-fw mr-1"/>
          Timesheet
        </router-link>
      </li>
      <li v-if="$perms.view_project" class="nav-item">
        <router-link
          id="nav-projects"
          :to="projects"
          class="nav-link">
          <icon :icon="['fas', 'briefcase']" class="fa-fw mr-1"/>
          Projects
        </router-link>
      </li>
      <li v-if="$perms.view_client" class="nav-item">
        <router-link
          id="nav-clients"
          :to="clients"
          class="nav-link">
          <icon :icon="['fas', 'address-book']" class="fa-fw mr-1"/>
          Clients
        </router-link>
      </li>
      <li v-if="$perms.view_task" class="nav-item">
        <router-link
          id="nav-tasks"
          :to="tasks"
          class="nav-link">
          <icon :icon="['fas', 'tasks']" class="fa-fw mr-1"/>
          Tasks
        </router-link>
      </li>
      <li v-if="$perms.view_entry" class="nav-item">
        <router-link
          id="nav-reports"
          :to="reports"
          class="nav-link">
          <icon :icon="['fas', 'book']" class="fa-fw mr-1"/>
          Reports
        </router-link>
      </li>
    </ul>
    <ul class="navbar-nav">
      <li class="nav-item">
        <a
          v-if="isStaff"
          id="nav-user-admin"
          class="nav-link"
          :href="admin"
          target="_blank">
          <icon :icon="['fas', 'tools']" class="fa-fw mr-1"/>
          Admin
        </a>
      </li>
      <li class="nav-item">
        <a
          id="nav-user-api"
          class="nav-link"
          :href="api"
          target="_blank">
          <icon :icon="['fas', 'tape']" class="fa-fw mr-1"/>
          API Browser
        </a>
      </li>
      <li class="nav-item">
        <a
          id="nav-user-logout"
          class="nav-link"
          :href="logout">
          <icon :icon="['fas', 'sign-out-alt']" class="fa-fw mr-1"/>
          Logout
        </a>
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
  background-color: rgb(27, 22, 16) !important;
}

.bg-light {
  background-color: rgb(247, 246, 243) !important;
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

// Fix chrome focus highlight
input:focus {
  outline: none !important;
}

// Github icon
#github {
  position: fixed;
  bottom: 5px;
  right: 15px;
  font-size: 2em;
}

// Remove arrow on the ellipsis icons on rows
.btn-icon:after {
  display: none;
}

.navbar {
  position: fixed;
  left: 0;
  width: 200px;
  top: 0;
  bottom: 0;
  padding: 0;
  padding-bottom: .25rem;
  flex-direction: column;

  .navbar-brand {
    display: flex;
    align-items: center;
    padding-left: 1rem;
    padding-right: 1rem;
    font-weight: bold;
    margin-right: 0;
    width: 200px;
    height: 54px;
  }

  .navbar-nav {
    flex-direction: column !important;
  }

  .nav-link,
  .navbar-text {
    width: 200px;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }

  .nav-link.active {
    background: #222;
  }
}

.page {
  width: calc(100% - 200px);
  margin-left: 200px;
}
</style>
