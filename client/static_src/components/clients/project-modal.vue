<template>
  <modal>
    <h5 slot="header">
      {{ id ? 'Edit: ' + name : 'New Project' }}
    </h5>

    <div slot="body">
      <form
        @submit.prevent
        @keyup.enter="submit">
        <div class="form-group">
          <div class="form-group">
            <label>Client</label>
            <select2
              id="project-modal-client"
              v-model="client"
              :options="clients"
              placeholder="Clients"/>
          </div>
          <div class="form-group">
            <label>Name</label>
            <input
              id="project-modal-name"
              v-model.trim="name"
              type="text"
              class="form-control form-control-sm"
              placeholder="Project Name"
              required>
          </div>
          <div class="form-group">
            <label>Estimate</label>
            <input
              id="project-modal-estimate"
              v-model.number="estimate"
              type="text"
              class="form-control form-control-sm"
              placeholder="Cost Estimate">
          </div>
        </div>
      </form>
    </div>

    <div slot="footer">
      <button
        id="project-modal-close"
        type="button"
        class="btn btn-secondary"
        @click="$emit('close')">
        Close
      </button>
      <button
        id="project-modal-submit"
        type="submit"
        class="btn btn-primary"
        @click="submit">
        {{ id ? 'Save Changes' : 'Add Project' }}
      </button>
    </div>
  </modal>
</template>


<script>
import {mapActions, mapGetters} from 'vuex';

import Modal from '../modal.vue';
import Select2 from '../select2.vue';


export default {
  components: {
    Modal,
    Select2,
  },
  props: [
    'config',
  ],
  data() {
    return {
      id: this.config.project ? this.config.project.id : null,
      url: this.config.project ? this.config.project.url : null,
      client: this.config.project ? this.config.project.client : null,
      name: this.config.project ? this.config.project.name : null,
      estimate: this.config.project ? this.config.project.estimate : null,
    };
  },
  computed: {
    ...mapGetters({
      clients: 'clients/getSelectClients',
    }),
  },
  methods: {
    ...mapActions({
      createProject: 'clients/createProject',
      editProject: 'clients/editProject',
    }),
    submit() {
      if (!this.id) this.createProject(this.$data);
      else this.editProject(this.$data);
      this.$emit('close');
    },
  },
};
</script>
