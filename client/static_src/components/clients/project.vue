<template>
  <div
    v-if="!project.archive"
    :id="'project-' + project.id"
    class="col-md-4 col-lg-3 mb-4">
    <div class="project card shadow">
      <div class="card-body d-flex flex-column">
        <div class="card-title">
          <div class="float-right">
            <template v-if="this.$perms.change_project || this.$perms.delete_project">
              <button
                id="project-menu"
                class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                type="button"
                data-toggle="dropdown">
                <icon
                  :icon="['fas', 'ellipsis-v']"/>
              </button>
              <div class="dropdown-menu dropdown-menu-right">
                <a
                  v-if="this.$perms.change_project"
                  id="project-menu-change"
                  class="dropdown-item"
                  href="#"
                  @click.prevent
                  @click.exact="toggleProjectModal(project)">Edit</a>
                <a
                  v-if="this.$perms.delete_project"
                  id="project-menu-delete"
                  class="dropdown-item"
                  href="#"
                  @click.prevent
                  @click.exact="deleteProject(index)">Delete</a>
                <a
                  v-if="this.$perms.change_project"
                  id="project-menu-archive"
                  class="dropdown-item"
                  href="#"
                  @click.prevent
                  @click.exact="archiveProject(index)">Archive</a>
              </div>
            </template>
          </div>
          <div class="h5 mb-3">
            <icon :icon="['fas', 'briefcase']" class="my-2 text-muted d-block"/>
            {{ project.name }}
          </div>
        </div>
        <div class="card-subtitle h6 text-muted mb-2">
          <icon :icon="['fas', 'clock']" class="mr-1 text-muted"/>
          {{ project.total_duration }}
          <icon :icon="['fas', 'list']" class="ml-3 mr-1 text-muted"/>
          {{ project.total_entries }}
        </div>
        <div v-if="project.percent_done !== null" class="card-subtitle h6 text-muted mt-auto">
          <div class="progress w-100">
            <div
              :class="['progress-bar', [project.percent_done > 100 ? 'bg-danger' : '']]"
              :style="{ width: project.percent_done + '%' }">
              {{ project.percent_done }}%
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import {mapActions} from 'vuex';


export default {
  props: [
    'project',
    'index',
    'toggleProjectModal',
  ],
  methods: {
    ...mapActions({
      deleteProject: 'clients/deleteProject',
      archiveProject: 'clients/archiveProject',
    }),
  },
};
</script>


<style lang="scss">
  .project.card {
    height: 17rem;
  }
</style>
