<template>
  <div class="container">
    <div
      v-if="this.$perms.add_client || this.$perms.add_project"
      class="row py-2 mb-4 bg-light rounded">
      <div class="col-12">
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

        <button
          class="btn btn-secondary btn-sm float-right ml-2"
          @click.prevent
          @click="refresh">
          <icon
            :icon="['fas', 'sync']"
            class="mr-1"/>
          Sync
        </button>

        <input
          id="client-search"
          v-model="search"
          placeholder="Filter Projects"
          class="form-control form-control-sm float-right w-25"
          type="text">
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
      <div
        class="client row py-2 px-3 bg-secondary text-white font-weight-bold">
        No clients added.
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
    refresh() {
      this.getClients();
    },
  },
};
</script>
