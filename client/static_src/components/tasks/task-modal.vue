<template>
<div class="modal">
  <div class="modal-dialog modal-dialog-centered">
    <form @submit.prevent="submit()" class="modal-content border-0 shadow">
      <div class="modal-body">
        <div class="form-group">
          <label for="task-name-edit">
            Name
          </label>
          <input
            id="task-name-edit"
            name="task-name-edit"
            v-model="taskMutable.name"
            class="form-control shadow-sm"
            placeholder="Empty"/>
        </div>
        <div class="form-group">
          <label for="task-hourly-rate-edit">
            Hourly Rate
          </label>
          <input
            class="form-control shadow-sm"
            id="task-hourly-rate-edit"
            name="task-hourly-rate-edit"
            v-model="taskMutable.hourly_rate"
            placeholder="Empty"/>
        </div>
      </div>
      <div class="modal-footer">
        <button
          id="task-submit-edit"
          class="btn btn-success mr-auto shadow-sm"
          type="submit">
          Save
        </button>
        <button
          id="task-close-edit"
          class="btn btn-light shadow-sm"
          data-dismiss="modal">
          Close
        </button>
      </div>
    </form>
  </div>
</div>
</template>


<script>
import $ from 'jquery';

import {mapActions} from 'vuex';


export default {
  data() {
    return {
      taskMutable: {}
    }
  },
  props: {
    task: {
      type: Object,
      default: {
        id: 'new',
        url: null,
        name: null,
        hourly_rate: null,
      },
    },
    index: {
      type: Number,
      default: null,
    },
  },
  methods: {
    ...mapActions({
      editTask: 'tasks/editTask',
      createTask: 'tasks/createTask',
    }),
    submit() {
      this.editTask(this.taskMutable);
      $(this.$el).modal('hide');
    },
  },
  mounted() {
    this.taskMutable = JSON.parse(JSON.stringify(this.task));
    $(this.$el).modal('show');
    const vm = this;
    $(vm.$el).on('hidden.bs.modal', function(e) {
      vm.$emit('closed');
    });
  },
};
</script>
