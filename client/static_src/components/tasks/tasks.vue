<template>
  <div class="container">
    <div class="row mb-4">
      <div class="col-sm-8">
        <h1 class="display-3 mb-0">
          Tasks
        </h1>
        <h2 class="display-4 text-muted mb-4">
          What you do and how much you charge
        </h2>
      </div>
      <div class="col-sm-4 d-flex flex-column align-items-end justify-content-center">
        <input
          id="task-search"
          v-model="search"
          placeholder="Filter Tasks"
          class="form-control form-control-sm mb-2"
          type="text">

        <button
          v-if="this.$perms.add_task"
          id="task-add"
          type="button"
          class="btn btn-primary btn-sm"
          @click="toggleModal">
          <icon :icon="['fas', 'plus']" class="mr-1"/>
          New Task
        </button>
      </div>
    </div>

    <task-modal
      v-if="modal.show && (this.$perms.add_task || this.$perms.change_task)"
      id="task-modal"
      :config="modal"
      @close="toggleModal"/>

    <div v-if="this.$perms.view_task" class="row">
      <template v-if="this.$perms.view_task && tasks(search).length !== 0">
        <task
          v-for="(task, index) in tasks(search)"
          :task="task"
          :index="index"
          :key="task.id"
          :toggle-edit-modal="toggleModal"/>
      </template>
      <template v-else>
        <div class="col-sm-3 col-md-4 mb-4">
          <div class="task card shadow">
            <div class="card-body">
              <div class="card-title h5">
                <icon :icon="['fas', 'tasks']" class="my-2 text-muted d-block"/>
                No tasks
              </div>
              <div class="card-subtitle h6 text-muted mb-2">
                Try adding one
              </div>
              <div class="card-text">
                No tasks added or match your filter
              </div>
            </div>
          </div>
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
  },
};
</script>


<style lang="scss">
  .display-3 {
    font-size: 3.5rem;
  }
  .display-4 {
    font-size: 2rem;
  }
</style>
