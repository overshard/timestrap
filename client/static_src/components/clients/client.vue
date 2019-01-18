<template>
  <div
    v-if="!client.archive"
    :id="'client-' + client.id">
    <div class="client row mb-2">
      <div class="col">
        <span class="h4">
          <span class="client-name">
            {{ client.name }}
          </span>
        </span>
        <template v-if="this.$perms.change_client || this.$perms.delete_client">
          <button
            id="client-menu"
            class="btn btn-faded btn-sm btn-icon dropdown-toggle mb-2"
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
              @click.exact="toggleClientModal(client)">Edit</a>
            <a
              v-if="this.$perms.delete_client"
              id="client-menu-delete"
              class="dropdown-item"
              href="#"
              @click.prevent
              @click.exact="deleteClient(index)">Delete</a>
            <a
              v-if="this.$perms.change_client"
              id="client-menu-archive"
              class="dropdown-item"
              href="#"
              @click.prevent
              @click.exact="archiveClient(index)">Archive</a>
          </div>
        </template>
      </div>
    </div>

    <div class="row mb-4">
      <template v-if="this.$perms.view_project && projects(client.url, search).length !== 0">
        <project
          v-for="(project, project_index) in projects(client.url, search)"
          :project="project"
          :index="project_index"
          :key="project.id"
          :toggle-project-modal="toggleProjectModal"/>
      </template>
      <template v-else>
        <div class="col-md-4 col-lg-3 mb-4">
          <div class="client card shadow">
            <div class="card-body">
              <div class="card-title h5">
                <icon :icon="['fas', 'briefcase']" class="my-2 text-muted d-block"/>
                No projects
              </div>
              <div class="card-subtitle h6 text-muted mb-2">
                Try adding one
              </div>
              <div class="card-text">
                No projects added or match your filter
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
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
