<template>
<card-modal
  :data="$data"
  :edit="editTask"
  :create="createTask"
  @close="$emit('close')">
  <template slot="modal-body">
    <div class="form-group row">
      <div class="col">
        <input
          id="task-name"
          name="task-name"
          ref="task-name"
          v-model="name"
          class="form-control-plaintext form-control-title"
          placeholder="Unnamed"
          required>
      </div>
    </div>
    <div class="form-group row">
      <label for="task-hourly-rate" class="col-sm-4 col-form-label text-muted">
        Hourly Rate
      </label>
      <div class="col-sm-8">
        <input
          class="form-control shadow-sm"
          id="task-hourly-rate"
          name="task-hourly-rate"
          v-model="hourly_rate"
          placeholder="Empty">
      </div>
    </div>
  </template>
</card-modal>
</template>


<script>
import {mapActions} from 'vuex';

import CardModal from '../cards/card-modal.vue';


export default {
  components: {
    CardModal,
  },
  props: {
    task: {
      type: Object,
    },
  },
  data() {
    return {
      id: this.task ? this.task.id : null,
      url: this.task ? this.task.url : null,
      name: this.task ? this.task.name : null,
      hourly_rate: this.task ? this.task.hourly_rate : null,
    }
  },
  methods: {
    ...mapActions({
      editTask: 'tasks/editTask',
      createTask: 'tasks/createTask',
    }),
  },
  mounted() {
    this.$refs['task-name'].focus();
  },
};
</script>
