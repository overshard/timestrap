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
          <i class="fa fa-plus mr-1"/>
          New Client
        </button>
        <button
          v-if="this.$perms.add_project"
          id="project-add"
          type="button"
          class="btn btn-primary btn-sm"
          @click="toggleProjectModal">
          <i class="fa fa-plus mr-1"/>
          New Project
        </button>

        <button
          class="btn btn-secondary btn-sm pull-right ml-2"
          @click.prevent
          @click="refresh">
          <i class="fa fa-refresh"/>
          Refresh
        </button>
      </div>
    </div>

    <div
      v-show="loading"
      class="container text-center py-4">
      <i class="fa fa-spinner text-primary fa-spin display-3 text-center"/>
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
      v-if="this.$perms.view_client"
      id="client-rows">
      <client
        v-for="(client, index) in clients"
        :client="client"
        :index="index"
        :key="client.id"
        :toggle-client-modal="toggleClientModal"
        :toggle-project-modal="toggleProjectModal"/>
    </div>
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
    };
  },
  computed: {
    ...mapState({
      loading: state => state.loading,
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


<style lang="scss">
.client {
  font-size: .9em;

  .row {
    border-top: 1px solid #eee;

    &:not(.bg-secondary) {
      &:nth-of-type(2n+1) {
        background-color: #fbf3e5 !important;
      }
    }

    &:last-child {
      border-bottom: 1px solid #eee;
      margin-bottom: 1rem;
    }
  }
}

.project {
  background: #fff;
}
</style>
