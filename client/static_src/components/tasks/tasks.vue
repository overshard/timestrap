<template>
  <div class="container">
    <div
      v-if="this.$perms.add_task"
      class="row py-2 mb-4 bg-light rounded">
      <div class="col-12">
        <button
          v-if="this.$perms.add_task"
          name="task-add"
          type="button"
          class="btn btn-primary btn-sm"
          @click="toggleModal">
          <i class="fa fa-plus mr-1"/>
          New Task
        </button>

        <button
          class="btn btn-secondary btn-sm pull-right ml-2"
          @click.prevent
          @click="refresh">
          <i class="fa fa-refresh"/> Refresh
        </button>
      </div>
    </div>

    <div
      v-show="loading"
      class="container text-center py-4">
      <i class="fa fa-spinner text-primary fa-spin display-3 text-center"/>
    </div>

    <task-modal
      v-if="modal.show && (this.$perms.add_task || this.$perms.change_task)"
      id="task-modal"
      :config="modal"
      @close="toggleModal"/>

    <div
      v-if="this.$perms.view_task"
      id="task-rows"
      class="rounded">
      <div class="task-head bg-secondary text-white row py-2">
        <div class="col-8 d-flex align-items-center">
          <i class="fa fa-tasks mr-2"/>
          <strong>Task Name</strong>
        </div>
        <div class="col-2 d-flex align-items-center">
          <i class="fa fa-clock-o mr-2"/>
          <strong>Hourly Rate</strong>
        </div>
        <div class="col-2"/>
      </div>
      <task
        v-for="(task, index) in tasks"
        :task="task"
        :index="index"
        :key="task.id"
        :toggle-edit-modal="toggleModal"/>
    </div>
  </div>
</template>


<script>
import {mapState, mapActions} from 'vuex';

import Task from './task.vue';
import TaskModal from './task-modal.vue';

export default {
  components: {
    Task,
    TaskModal,
  },
  data() {
    return {
      modal: {
        task: null,
        show: false,
      },
    };
  },
  computed: {
    ...mapState({
      loading: state => state.loading,
      tasks: state => state.tasks.all,
    }),
  },
  methods: {
    ...mapActions('tasks', [
      'getTasks',
    ]),
    toggleModal(task) {
      if (task) this.modal.task = task;
      else this.modal.task = null;
      this.modal.show = !this.modal.show;
    },
    refresh() {
      this.getTasks();
    },
  },
};
</script>


<style lang="scss">
#task-rows {
  .task {
    font-size: .9em;
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
</style>
