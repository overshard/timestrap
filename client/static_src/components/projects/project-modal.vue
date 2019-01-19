<template>
<card-modal
  :data="$data"
  :edit="editProject"
  :create="createProject"
  @close="$emit('close')">
  <template slot="modal-body">
    <div class="form-group row">
      <div class="col">
        <input
          id="project-name"
          name="project-name"
          ref="project-name"
          v-model="name"
          class="form-control-plaintext form-control-title"
          placeholder="Unnamed"
          required/>
      </div>
    </div>
    <div class="form-group row">
      <label for="project-client" class="col-sm-4 col-form-label text-muted">
        Client
      </label>
      <div class="col-sm-8">
        <select2
          id="project-client"
          v-model="client"
          :options="clients"
          :selected="client"
          placeholder="Empty"/>
      </div>
    </div>
    <div class="form-group row">
      <label for="project-estimate" class="col-sm-4 col-form-label text-muted">
        Estimate
      </label>
      <div class="col-sm-8">
        <input
          class="form-control shadow-sm"
          id="project-estimate"
          name="project-estimate"
          v-model="estimate"
          placeholder="Empty"/>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-4 text-muted">
        Archive
      </div>
      <div class="col-sm-8">
        <div class="custom-control custom-switch">
          <input
            type="checkbox"
            class="custom-control-input"
            id="project-archive"
            name="project-archive"
            v-model="archive">
          <label class="custom-control-label text-muted" for="project-archive"/>
        </div>
      </div>
    </div>
  </template>
</card-modal>
</template>


<script>
import {mapActions, mapGetters} from 'vuex';

import Select2 from '../select2.vue';
import CardModal from '../cards/card-modal.vue';


export default {
  components: {
    Select2,
    CardModal,
  },
  props: {
    project: {
      type: Object,
    },
  },
  data() {
    return {
      id: this.project ? this.project.id : null,
      url: this.project ? this.project.url : null,
      name: this.project ? this.project.name : null,
      client: this.project ? this.project.client : null,
      estimate: this.project ? this.project.estimate : null,
      archive: this.project ? this.project.archive : null,
    }
  },
  computed: {
    ...mapGetters({
      clients: 'clients/getSelectClients',
    }),
  },
  methods: {
    ...mapActions({
      editProject: 'projects/editProject',
      createProject: 'projects/createProject',
    }),
  },
  mounted() {
    this.$refs['project-name'].focus();
  },
};
</script>
