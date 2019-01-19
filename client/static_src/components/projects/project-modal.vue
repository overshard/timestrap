<template>
<card-modal
  :data="$data"
  :edit="editProject"
  :create="createProject"
  @close="$emit('close')">
  <template slot="modal-body">
    <div class="form-group">
      <label for="project-name">
        Name
      </label>
      <input
        id="project-name"
        name="project-name"
        v-model="name"
        class="form-control shadow-sm"
        placeholder="Empty"
        required/>
    </div>
    <div class="form-group">
      <label for="project-name">
        Client
      </label>
      <select2
        id="project-client"
        v-model="client"
        :options="clients"
        :selected="client"
        placeholder="Empty"/>
    </div>
    <div class="form-group">
      <label for="project-estimate">
        Estimate
      </label>
      <input
        class="form-control shadow-sm"
        id="project-estimate"
        name="project-estimate"
        v-model="estimate"
        placeholder="Empty"/>
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
};
</script>
