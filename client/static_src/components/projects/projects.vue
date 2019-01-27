<template>
<cards
  :number-of-elements="projects(search).length"
  :view_perm="$perms.view_project"
  @search="search = $event">
  <template slot="cards-title">
    <icon :icon="['fas', 'briefcase']" class="fa-sm mr-2"/>
    Projects
  </template>

  <template slot="cards-list">
    <project
      v-for="(project, index) in projects(search)"
      :key="project.id"
      :project="project"
      :index="index"
      @modal="modalToggle(project)"/>
  </template>

  <template slot="cards-new">
    <project @modal="modalToggle()"/>
  </template>

  <project-modal
    slot="cards-modal"
    v-if="modalShow"
    :project="modalProject"
    @close="modalShow = false"/>
</cards>
</template>


<script>
import {mapGetters, mapActions} from 'vuex';

import Cards from '../cards/cards.vue';
import Project from './project.vue';
import ProjectModal from './project-modal.vue';


export default {
  components: {
    Cards,
    Project,
    ProjectModal,
  },
  data() {
    return {
      search: '',
      modalProject: null,
      modalShow: false,
    };
  },
  computed: {
    ...mapGetters({
      projects: 'projects/getSearchProjects',
    }),
  },
  methods: {
    modalToggle: function(project) {
      if (typeof(project) !== 'undefined') this.modalProject = project;
      else this.modalProject = null;
      this.modalShow = !this.modalShow;
    },
  }
};
</script>
