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
          class="btn btn-secondary btn-sm float-right ml-2"
          @click.prevent
          @click="refresh">
          <icon
            :icon="['fas', 'sync']"
            class="mr-1"/>
          Sync
        </button>

        <input
          id="task-search"
          v-model="search"
          placeholder="Filter Tasks"
          class="form-control form-control-sm float-right w-25"
          type="text">
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
            :icon="['fas', 'hand-holding-usd']"
            class="mr-2"/>
          <strong>Hourly Rate</strong>
        </div>
        <div class="col-2"/>
      </div>
      <template v-if="tasks(search).length !== 0">
        <task
          v-for="(task, index) in tasks(search)"
          :task="task"
          :index="index"
          :key="task.id"
          :toggle-edit-modal="toggleModal"/>
      </template>
      <template v-else>
        <div
          class="task row bg-light py-2 px-3">
          No tasks added or meet your filter.
        </div>
      </template>
    </div>
  </div>
</template>


<script>
import {mapGetters, mapActions} from 'vuex';

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
      search: '',
    };
  },
  computed: {
    ...mapGetters({
      tasks: 'tasks/getSearchTasks',
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
