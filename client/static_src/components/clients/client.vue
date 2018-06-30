<template>
  <div
    :id="'client-' + client.id"
    class="client">
    <div class="row py-2 bg-secondary text-white">
      <div :class="['col-sm-4', 'd-flex', 'align-items-center']">
        <i class="fa fa-address-book mr-2"/>
        <span class="font-weight-bold text-uppercase client-name">{{ client.name }}</span>
      </div>
      <div class="col-sm-2 d-flex align-items-center">
        <i class="fa fa-clock-o mr-2"/>
        <strong>Total Time</strong>
      </div>
      <div class="col-sm-2 d-flex align-items-center">
        <i class="fa fa-list mr-2"/>
        <strong>Entries</strong>
      </div>
      <div class="col-sm-3 d-flex align-items-center">
        <i class="fa fa-percent mr-2"/>
        <strong>Progress</strong>
      </div>
      <div class="col-sm-1 d-flex align-self-center justify-content-end">
        <template v-if="this.$perms.change_client || this.$perms.delete_client">
          <button
            name="client-menu"
            class="btn btn-faded btn-sm btn-icon dropdown-toggle"
            type="button"
            data-toggle="dropdown">
            <i class="fa fa-ellipsis-v"/>
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
              <!-- <a id="client-menu-archive"
                        class="dropdown-item"
                        href="#"
                        v-if="this.$perms.change_client"
                        v-on:click.prevent
                        v-on:click="archiveClient">Archive</a> -->
          </div>
        </template>
      </div>
    </div>

    <template v-if="this.$perms.view_project">
      <project
        v-for="(project, project_index) in projects(client.url)"
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
    'key',
    'toggleClientModal',
    'toggleProjectModal',
    'removeProject',
  ],
  computed: {
    ...mapGetters({
      projects: 'clients/getClientProjects',
    }),
  },
  methods: {
    ...mapActions({
      deleteClient: 'clients/deleteClient',
    }),
  },
};
</script>
