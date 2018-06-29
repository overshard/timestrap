<template>
  <modal>
    <h5 slot="header">
      {{ id ? 'Edit: ' + name : 'New Project' }}
    </h5>

    <div slot="body">
      <div class="form-group">
        <div class="form-group">
          <label>Client</label>
          <select2
            id="project-client"
            v-model="client"
            :options="clients"
            placeholder="Clients"/>
        </div>
        <div class="form-group">
          <label>Name</label>
          <input
            v-model.trim="name"
            name="project-name"
            type="text"
            class="form-control form-control-sm"
            placeholder="Project Name"
            required >
        </div>
        <div class="form-group">
          <label>Estimate</label>
          <input
            v-model.number="estimate"
            name="project-estimate"
            type="text"
            class="form-control form-control-sm"
            placeholder="Cost Estimate" >
        </div>
      </div>
    </div>

    <div slot="footer">
      <button
        name="project-modal-cancel"
        type="button"
        class="btn btn-secondary"
        @click="$emit('close')">
        Close
      </button>
      <button
        name="project-modal-submit"
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
