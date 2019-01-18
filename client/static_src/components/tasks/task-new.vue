<template>
  <div class="col-md-4 col-lg-3 mb-4">
    <div
      id="task-add"
      :class="{ 'task': true, 'new': true, 'card': true, 'shadow-sm': true, 'edit': edit }"
      v-if="this.$perms.add_task"
      @click.exact="editMode()">
      <div class="card-body">
        <template v-if="!edit">
          <div class="btn btn-light btn-sm btn-icon shadow-sm text-muted float-right">
            <icon :icon="['fas', 'plus']"/>
          </div>
          <div class="card-title h5">
            New task
          </div>
        </template>
        <template v-else>
          <form
            class="card-text"
            @submit.prevent="submit()">
            <label for="task-name-new" class="card-label">
              <small class="text-muted font-weight-bold">Name</small>
            </label>
            <input
              id="task-name-new"
              name="task-name-new"
              v-model="task.name"
              class="form-control form-control-sm"
              placeholder="Name"
              required/>
            <label for="task-hourly-rate-new" class="card-label">
              <small class="text-muted font-weight-bold">Hourly Rate</small>
            </label>
            <input
              class="form-control form-control-sm"
              id="task-hourly-rate-new"
              name="task-hourly-rate-new"
              v-model="task.hourly_rate"
              placeholder="Hourly rate"/>
            <button
              id="task-submit-new"
              class="btn btn-sm btn-success mt-2"
              type="submit">
              Save
            </button>
            <button
              class="btn btn-sm btn-light mt-2"
              type="button"
              @click.exact="cancel()">
              Cancel
            </button>
          </form>
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
      canceled: false,
      task: {
        name: null,
        hourly_rate: null,
      },
    }
  },
  methods: {
    ...mapActions({
      createTask: 'tasks/createTask',
    }),
    editMode() {
      if (this.canceled == false) this.edit = true;
      else this.canceled = false;
    },
    cancel() {
      this.edit = false;
      this.canceled = true;
      this.task = {
        name: null,
        hourly_rate: null,
      };
    },
    submit() {
      this.createTask(this.task);
      this.cancel();
    },
  },
};
</script>


<style lang="scss">

.task.card.new {
  cursor: pointer;
  opacity: .7;
  transition: opacity 300ms, transform 300ms;

  &:hover, &.edit {
    opacity: 1;
  }
}
</style>
