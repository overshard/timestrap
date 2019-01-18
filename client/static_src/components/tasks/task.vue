<template>
  <div :id="'task-' + task.id" class="col-md-4 col-lg-3 mb-4">
    <div class="task card shadow-sm">
      <div class="card-body">
        <div class="float-right">
          <template v-if="this.$perms.change_task || this.$perms.delete_task">
            <button
              id="task-menu"
              class="btn btn-faded btn-sm btn-icon dropdown-toggle"
              type="button"
              data-toggle="dropdown">
              <icon :icon="['fas', 'ellipsis-v']"/>
            </button>
            <div class="dropdown-menu dropdown-menu-right">
              <a
                v-if="this.$perms.change_task"
                id="task-menu-change"
                class="dropdown-item"
                href="#"
                @click.prevent
                @click.exact="toggleEditModal(task)">
                Edit
              </a>
              <a
                v-if="this.$perms.delete_task"
                id="task-menu-delete"
                class="dropdown-item"
                href="#"
                @click.prevent
                @click.exact="deleteTask(index)">
                Delete
              </a>
            </div>
          </template>
        </div>
        <div class="card-title h5">
          <icon :icon="['fas', 'tasks']" class="my-2 text-muted d-block"/>
          {{ task.name }}
        </div>
        <div class="card-subtitle h6 mb-2 text-muted">
          <template v-if="task.hourly_rate">
            ${{ task.hourly_rate }}
          </template>
          <template v-else>
            Not set
          </template>
        </div>
      </div>
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
  .task.card {
    height: 17rem;
  }
</style>
