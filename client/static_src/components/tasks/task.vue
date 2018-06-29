<template>
  <div class="task row bg-light py-1">
    <div :class="[[this.$perms.change_task ? 'col-8' : 'col-10'], 'd-flex', 'align-items-center']">
      <i class="fa fa-tasks text-muted mr-2"/>
      {{ task.name }}
    </div>
    <div class="col-2 d-flex align-items-center">
      <i class="fa fa-clock-o text-muted mr-2"/>
      <template v-if="task.hourly_rate">
        ${{ task.hourly_rate }}
      </template>
      <template v-else>
        Not set
      </template>
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end">
      <template v-if="this.$perms.change_task || this.$perms.delete_task">
        <button
          name="task-menu"
          class="btn btn-faded btn-sm btn-icon dropdown-toggle"
          type="button"
          data-toggle="dropdown">
          <i class="fa fa-ellipsis-v"/>
        </button>
        <div class="dropdown-menu dropdown-menu-right">
          <a
            v-if="this.$perms.change_task"
            id="task-menu-change"
            class="dropdown-item"
            href="#"
            @click.prevent
            @click="toggleEditModal(task)">
            Edit
          </a>
          <a
            v-if="this.$perms.delete_task"
            id="task-menu-delete"
            class="dropdown-item"
            href="#"
            @click.prevent
            @click="deleteTask(index)">
            Delete
          </a>
        </div>
      </template>
    </div>
  </div>
</template>


<script>
import {mapActions} from 'vuex';


export default {
  props: [
    'task',
    'index',
    'key',
    'toggleEditModal',
  ],
  methods: {
    ...mapActions({
      deleteTask: 'tasks/deleteTask',
    }),
  },
};
</script>
