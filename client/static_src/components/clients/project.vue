<template>
  <div
    v-if="!project.archive"
    class="project row py-1 bg-light">
    <div :class="['col-sm-4', 'mb-1', 'project-name']">
      <i class="fa fa-briefcase text-muted mr-1"/>
      {{ project.name }}
    </div>
    <div class="col-sm-2 d-flex align-items-center">
      <i class="fa fa-clock-o text-muted mr-2"/>
      <span class="mb-1">{{ project.total_duration }}</span>
    </div>
    <div class="col-sm-2 d-flex align-items-center">
      <i class="fa fa-list text-muted mr-2"/>
      <span class="mb-1">{{ project.total_entries }}</span>
    </div>
    <div
      v-if="project.percent_done !== null"
      class="col-sm-3 d-flex align-items-center">
      <div class="progress w-100">
        <div
          :class="['progress-bar', [project.percent_done > 100 ? 'bg-danger' : '']]"
          :style="{ width: project.percent_done + '%' }">
          {{ project.percent_done }}%
        </div>
      </div>
    </div>
    <div
      v-else
      class="col-sm-3 d-flex align-items-center">
      No Estimate
    </div>
    <div class="col-sm-1 d-flex align-self-center justify-content-end">
      <template v-if="this.$perms.change_project || this.$perms.delete_project">
        <button
          name="project-menu"
          class="btn btn-faded btn-sm btn-icon dropdown-toggle"
          type="button"
          data-toggle="dropdown">
          <i class="fa fa-ellipsis-v"/>
        </button>
        <div class="dropdown-menu dropdown-menu-right">
          <a
            v-if="this.$perms.change_project"
            id="project-menu-change"
            class="dropdown-item"
            href="#"
            @click.prevent
            @click="toggleProjectModal(project)">Edit</a>
          <a
            v-if="this.$perms.delete_project"
            id="project-menu-delete"
            class="dropdown-item"
            href="#"
            @click.prevent
            @click="deleteProject(index)">Delete</a>
            <!-- <a id="project-menu-archive"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.change_project"
                   v-on:click.prevent
                   v-on:click="archiveProject">Archive</a> -->
        </div>
      </template>
    </div>
  </div>
</template>


<script>
import {mapActions} from 'vuex';


export default {
  props: [
    'project',
    'index',
    'key',
    'toggleProjectModal',
  ],
  methods: {
    ...mapActions({
      deleteProject: 'clients/deleteProject',
    }),
  },
};
</script>
