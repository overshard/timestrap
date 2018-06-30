<template>
  <modal>
    <h5 slot="header">
      <i class="fa fa-tasks mr-1"/>
      {{ id ? 'Edit: ' + name : 'New Task' }}
    </h5>

    <div slot="body">
      <form
        @submit.prevent
        @keyup.enter="submit">
        <div class="form-group">
          <label>Task Name</label>
          <input
            v-model.trim="name"
            id="task-modal-name"
            placeholder="Task Name"
            type="text"
            class="form-control form-control-sm"
            required >
        </div>
        <div class="form-group">
          <label>Hourly Rate</label>
          <input
            v-model.number="hourly_rate"
            id="task-modal-hourly-rate"
            placeholder="Hourly Rate"
            type="text"
            class="form-control form-control-sm"
            required >
        </div>
      </form>
    </div>

    <div slot="footer">
      <button
        id="task-modal-close"
        type="button"
        class="btn btn-secondary"
        @click="$emit('close')">
        Close
      </button>
      <button
        id="task-modal-submit"
        type="submit"
        class="btn btn-primary"
        @click="submit">
        {{ id ? 'Save Changes' : 'Add Task' }}
      </button>
    </div>
  </modal>
</template>


<script>
import {mapActions} from 'vuex';

import Modal from '../modal.vue';


export default {
  components: {
    Modal,
  },
  props: [
    'config',
  ],
  data() {
    return {
      id: this.config.task ? this.config.task.id : null,
      url: this.config.task ? this.config.task.url : null,
      name: this.config.task ? this.config.task.name : null,
      hourly_rate: this.config.task ? this.config.task.hourly_rate : null,
    };
  },
  methods: {
    ...mapActions({
      createTask: 'tasks/createTask',
      editTask: 'tasks/editTask',
    }),
    submit() {
      if (!this.id) this.createTask(this.$data);
      else this.editTask(this.$data);
      this.$emit('close');
    },
  },
};
</script>
