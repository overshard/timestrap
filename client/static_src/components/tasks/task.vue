<template>
  <div
    :id="'task-' + task.id"
    class="task row bg-light py-1">
    <div :class="[[this.$perms.change_task ? 'col-8' : 'col-10'], 'd-flex', 'align-items-center']">
      <icon
        :icon="['fas', 'tasks']"
        class="mr-2 text-muted"/>
      {{ task.name }}
    </div>
    <div class="col-2 d-flex align-items-center">
      <icon
        :icon="['fas', 'hand-holding-usd']"
        class="mr-2 text-muted"/>
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
          id="task-menu"
          class="btn btn-faded btn-sm btn-icon dropdown-toggle"
          type="button"
          data-toggle="dropdown">
          <icon
            :icon="['fas', 'ellipsis-v']"/>
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
    'toggleEditModal',
  ],
  methods: {
    ...mapActions({
      deleteTask: 'tasks/deleteTask',
    }),
  },
};
</script>



<style lang="scss">
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
</style>
