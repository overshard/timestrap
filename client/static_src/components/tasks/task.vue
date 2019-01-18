<template>
<div :id="'task-' + task.id" class="col-md-4 col-lg-3 mb-4">
  <template v-if="task.id != 'new'">
    <div class="task card shadow-sm" style="height: 15rem;">
      <div class="card-body">
        <div class="float-right">
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
                @click.exact="toggleModal()">
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

        <div class="card-title h5">
          {{ task.name }}
        </div>
        <div
          v-if="task.hourly_rate"
          class="card-subtitle h6 mb-2 badge badge-pill badge-secondary">
          ${{ task.hourly_rate }}/hr
        </div>
      </div>
    </div>
  </template>
  <template v-else>
    <div class="task card new" style="height: 15rem;">
      <div class="card-body d-flex justify-content-center align-items-center">
        <div class="text-muted">
          <icon :icon="['fas', 'plus']" class="mr-1"/>
          New
        </div>
      </div>
    </div>
  </template>

  <task-modal
    v-if="modal"
    v-on:closed="toggleModal"
    :task="task"
    :index="index"/>
</div>
</template>


<script>
import Vue from 'vue';
import {mapActions} from 'vuex';

import TaskModal from './task-modal.vue'


export default {
  components: {
    TaskModal,
  },
  data() {
    return {
      modal: false,
    }
  },
  props: {
    task: {
      type: Object,
      default: {
        id: 'new',
        url: null,
        name: null,
        hourly_rate: null,
      },
    },
    index: {
      type: Number,
      default: null,
    },
  },
  methods: {
    ...mapActions({
      deleteTask: 'tasks/deleteTask',
    }),
    toggleModal: function() {
      this.modal = !this.modal;
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
