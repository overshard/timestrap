<template>
  <div>
    <div class="row mb-4">
      <div class="col-sm-8">
        <h1 class="display-3 mb-0">
          Clients
        </h1>
        <h2 class="display-4 text-muted mb-4">
          With their projects
        </h2>
      </div>
      <div class="col-sm-4 d-flex flex-column align-items-end justify-content-center">
        <input
          id="client-search"
          v-model="search"
          placeholder="Filter Projects"
          class="form-control form-control-sm mb-2"
          type="text">

        <div class="w-100 text-right">
          <button
            v-if="this.$perms.add_client"
            id="client-add"
            type="button"
            class="btn btn-primary btn-sm"
            @click="toggleClientModal">
            <icon
              :icon="['fas', 'plus']"
              class="mr-1"/>
            New Client
          </button>

          <button
            v-if="this.$perms.add_project"
            id="project-add"
            type="button"
            class="btn btn-primary btn-sm"
            @click="toggleProjectModal">
            <icon
              :icon="['fas', 'plus']"
              class="mr-1"/>
            New Project
          </button>
        </div>
      </div>
    </div>

    <client-modal
      v-if="modalClient.show"
      id="client-modal"
      :config="modalClient"
      @close="toggleClientModal"/>

    <project-modal
      v-if="modalProject.show"
      id="project-modal"
      :config="modalProject"
      @close="toggleProjectModal"/>

    <div
      v-if="this.$perms.view_client && clients.length !== 0"
      id="client-rows">
      <client
        v-for="(client, index) in clients"
        :client="client"
        :index="index"
        :key="client.id"
        :search="search"
        :toggle-client-modal="toggleClientModal"
        :toggle-project-modal="toggleProjectModal"/>
    </div>
    <template v-else>
      <div class="row">
        <div class="col-md-4 col-lg-3 mb-4">
          <div class="client card shadow">
            <div class="card-body">
              <div class="card-title h5">
                <icon :icon="['fas', 'briefcase']" class="my-2 text-muted d-block"/>
                No clients
              </div>
              <div class="card-subtitle h6 text-muted mb-2">
                Try adding one
              </div>
              <div class="card-text">
                No clients added or match your filter
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>


<script>
import {mapState, mapActions} from 'vuex';

import Client from './client.vue';
import ClientModal from './client-modal.vue';
import ProjectModal from './project-modal.vue';


export default {
  components: {
    Client,
    ClientModal,
    ProjectModal,
  },
  data() {
    return {
      modalClient: {
        client: null,
        show: false,
      },
      modalProject: {
        project: null,
        show: false,
      },
      search: '',
    };
  },
  computed: {
    ...mapState({
      clients: state => state.clients.allClients,
    }),
  },
  methods: {
    ...mapActions('clients', [
      'getClients',
    ]),
    toggleClientModal(client) {
      if (client) this.modalClient.client = client;
      else this.modalClient.client = null;
      this.modalClient.show = !this.modalClient.show;
    },
    toggleProjectModal(project) {
      if (project) this.modalProject.project = project;
      else this.modalProject.project = null;
      this.modalProject.show = !this.modalProject.show;
    },
  },
};
</script>


<style lang="scss">
  .client.card {
    height: 17rem;
  }
</style>
