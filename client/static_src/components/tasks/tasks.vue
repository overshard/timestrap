<template>
  <div>
    <div class="row mb-4">
      <div class="col-md-7">
        <h1 class="mb-0">
          <icon :icon="['fas', 'tasks']" class="text-muted mr-2"/>
          Tasks
        </h1>
      </div>
      <div class="col-md-5 d-flex flex-column align-items-end justify-content-center">
        <input
          id="task-search"
          v-model="search"
          placeholder="Type to filter tasks..."
          class="form-control shadow-sm"
          type="text">
      </div>
    </div>

    <div v-if="this.$perms.view_task" class="row">
      <template v-if="this.$perms.view_task && tasks(search).length !== 0">
        <task
          v-for="(task, index) in tasks(search)"
          :task="task"
          :index="index"
          :key="task.id"/>
        <task/>
      </template>
      <template v-else>
        <div class="col-mb-4 col-lg-3 mb-4">
          <div class="task card shadow-sm border-danger">
            <div class="card-body">
              <div class="card-title h5">
                No tasks
              </div>
              <div class="card-subtitle h6 text-muted mb-2">
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


export default {
  components: {
    Task,
  },
  data() {
    return {
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
  },
};
</script>
