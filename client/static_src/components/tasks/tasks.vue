<template>
  <div>
    <div class="row mb-4">
      <div class="col-sm-8">
        <h1 class="display-3 mb-0">
          Tasks
        </h1>
      </div>
      <div class="col-sm-4 d-flex flex-column align-items-end justify-content-center">
        <input
          id="task-search"
          v-model="search"
          placeholder="Filter Tasks"
          class="form-control"
          type="text">
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
        <div class="col-mb-4 col-lg-3 mb-4">
          <div class="task card shadow-sm border-danger">
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
      <div class="col-md-4 col-lg-3 mb-4">
        <div
          class="task new card shadow-sm border-info"
          v-if="this.$perms.add_task"
          @click="toggleModal">
          <div class="card-body">
            <icon :icon="['fas', 'plus']" class="my-2 text-muted float-right"/>
            <div class="card-title h5">
              <icon :icon="['fas', 'tasks']" class="my-2 text-muted d-block"/>
              New task
            </div>
          </div>
        </div>
      </div>
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
  .task.card.new {
    cursor: pointer;
  }
</style>
