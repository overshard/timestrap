<template>
  <div class="container">
    <div
      v-if="this.$perms.add_task"
      class="row py-2 mb-4 bg-light rounded">
      <div class="col-12">
        <button
          v-if="this.$perms.add_task"
          id="task-add"
          type="button"
          class="btn btn-primary btn-sm"
          @click="toggleModal">
          <icon
            :icon="['fas', 'plus']"
            class="mr-1"/>
          New Task
        </button>

        <button
          class="btn btn-secondary btn-sm pull-right ml-2"
          @click.prevent
          @click="refresh">
          <icon
            :icon="['fas', 'sync']"
            class="mr-1"/>
          Sync
        </button>
      </div>
    </div>

    <task-modal
      v-if="modal.show && (this.$perms.add_task || this.$perms.change_task)"
      id="task-modal"
      :config="modal"
      @close="toggleModal"/>

    <div
      v-if="this.$perms.view_task"
      class="rounded">
      <div class="task-head bg-secondary text-white row py-2">
        <div class="col-8 d-flex align-items-center">
          <icon
            :icon="['fas', 'tasks']"
            class="mr-2"/>
          <strong>Task Name</strong>
        </div>
        <div class="col-2 d-flex align-items-center">
          <icon
            :icon="['far', 'clock']"
            class="mr-2"/>
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
