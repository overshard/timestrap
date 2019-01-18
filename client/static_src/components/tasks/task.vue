<template>
  <div :id="'task-' + taskMutable.id" class="col-md-4 col-lg-3 mb-4">
    <div class="task card shadow-sm">
      <div class="card-body">
        <div v-if="!edit" class="float-right">
          <template v-if="this.$perms.change_task || this.$perms.delete_task">
            <button
              id="task-menu"
              class="btn btn-light btn-sm btn-icon shadow-sm dropdown-toggle text-muted"
              type="button"
              data-toggle="dropdown">
              <icon :icon="['fas', 'ellipsis-h']"/>
            </button>
            <div class="dropdown-menu dropdown-menu-right shadow">
              <button
                v-if="this.$perms.change_task"
                id="task-menu-change"
                class="dropdown-item"
                @click.prevent
                @click.exact="editMode()">
                Edit
              </button>
              <button
                v-if="this.$perms.delete_task"
                id="task-menu-delete"
                class="dropdown-item"
                @click.prevent
                @click.exact="deleteTask(index)">
                Delete
              </button>
            </div>
          </template>
        </div>
        <template v-if="!this.edit">
          <div class="card-title h5">
            {{ taskMutable.name }}
          </div>
          <div v-if="task.hourly_rate" class="card-subtitle h6 mb-2 text-muted">
            ${{ taskMutable.hourly_rate }}/hr
          </div>
        </template>
        <template v-else>
          <div class="card-text">
            <label for="task-name-edit" class="card-label">
              <small class="text-muted font-weight-bold">Name</small>
            </label>
            <input
              id="task-name-edit"
              name="task-name-edit"
              v-model="taskMutable.name"
              class="form-control form-control-sm"
              placeholder="Name"/>
            <label for="task-hourly-rate-edit" class="card-label">
              <small class="text-muted font-weight-bold">Hourly Rate</small>
            </label>
            <input
              class="form-control form-control-sm"
              id="task-hourly-rate-edit"
              name="task-hourly-rate-edit"
              v-model="taskMutable.hourly_rate"
              placeholder="Hourly rate"/>
          </div>
          <button
            id="task-submit-edit"
            class="btn btn-sm btn-success mt-2"
            type="submit"
            @click.exact="submit()">
            Save
          </button>
          <button
            class="btn btn-sm btn-light mt-2"
            type="button"
            @click.exact="cancel()">
            Cancel
          </button>
        </template>
      </div>
    </div>
  </div>
</template>


<script>
import {mapActions} from 'vuex';


export default {
  data() {
    return {
      edit: false,
      taskMutable: {}
    }
  },
  props: {
    task: {
      type: Object,
      default: {
        id: null,
        url: null,
        name: null,
        hourly_rate: null,
      },
    },
    index: {
      type: Number,
    },
  },
  methods: {
    ...mapActions({
      deleteTask: 'tasks/deleteTask',
      editTask: 'tasks/editTask',
    }),
    editMode() {
      this.edit = !this.edit;
    },
    submit() {
      this.edit = !this.edit;
      this.editTask(this.taskMutable);
    },
    cancel() {
      this.edit = !this.edit;
      this.taskMutable = JSON.parse(JSON.stringify(this.task));
    },
  },
  created() {
    this.taskMutable = JSON.parse(JSON.stringify(this.task));
  }
};
</script>


<style lang="scss">
.card-label {
  margin-bottom: 0;
  margin-top: .2rem;
}

.task.card {
  height: 17rem;
  transition: transform 300ms;
}
</style>
