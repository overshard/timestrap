<template>
  <div
    v-if="!client.archive"
    :id="'client-' + client.id">
    <div class="client row py-2 bg-secondary text-white">
      <div :class="['col-sm-4', 'd-flex', 'align-items-center']">
        <icon
          :icon="['fas', 'address-book']"
          class="mr-2"/>
        <span class="font-weight-bold text-uppercase client-name">{{ client.name }}</span>
      </div>
      <div class="col-sm-2 d-flex align-items-center">
        <icon
          :icon="['fas', 'clock']"
          class="mr-2"/>
        <strong>Total Time</strong>
      </div>
      <div class="col-sm-2 d-flex align-items-center">
        <icon
          :icon="['fas', 'list']"
          class="mr-2"/>
        <strong>Entries</strong>
      </div>
      <div class="col-sm-3 d-flex align-items-center">
        <icon
          :icon="['fas', 'percentage']"
          class="mr-2"/>
        <strong>Progress</strong>
      </div>
      <div class="col-sm-1 d-flex align-self-center justify-content-end">
        <template v-if="this.$perms.change_client || this.$perms.delete_client">
          <button
            id="client-menu"
            class="btn btn-faded btn-sm btn-icon dropdown-toggle"
            type="button"
            data-toggle="dropdown">
            <icon
              :icon="['fas', 'ellipsis-v']"/>
          </button>
          <div class="dropdown-menu dropdown-menu-right">
            <a
              v-if="this.$perms.change_client"
              id="client-menu-change"
              class="dropdown-item"
              href="#"
              @click.prevent
              @click="toggleClientModal(client)">Edit</a>
            <a
              v-if="this.$perms.delete_client"
              id="client-menu-delete"
              class="dropdown-item"
              href="#"
              @click.prevent
              @click="deleteClient(index)">Delete</a>
            <a
              v-if="this.$perms.change_client"
              id="client-menu-archive"
              class="dropdown-item"
              href="#"
              @click.prevent
              @click="archiveClient(index)">Archive</a>
          </div>
        </template>
      </div>
    </div>

    <template v-if="this.$perms.view_project">
      <project
        v-for="(project, project_index) in projects(client.url, search)"
        :project="project"
        :index="project_index"
        :key="project.id"
        :toggle-project-modal="toggleProjectModal"/>
    </template>

  </div>
</template>


<script>
import {mapActions, mapGetters} from 'vuex';

import Project from './project.vue';


export default {
  components: {
    Project,
  },
  props: [
    'client',
    'index',
    'toggleClientModal',
    'toggleProjectModal',
    'removeProject',
    'search',
  ],
  computed: {
    ...mapGetters({
      projects: 'clients/getClientProjectsSearch',
    }),
  },
  methods: {
    ...mapActions({
      deleteClient: 'clients/deleteClient',
      archiveClient: 'clients/archiveClient',
    }),
  },
};
</script>
