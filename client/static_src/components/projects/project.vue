<template>
<card
  :index="index"
  @modal="$emit('modal')"
  @delete="deleteProject(index)">
  <template slot="card-body">
    <div class="card-title h5 font-weight-bold">
      {{ project.name }}
    </div>
    <div v-if="project.client_details" class="card-subtitle h6 text-muted mb-4">
      for <strong>{{ project.client_details.name }}</strong>
    </div>
    <div v-if="project.total_duration && project.total_entries" class="card-subtitle h6 mb-5">
      <icon :icon="['fas', 'clock']" class="mr-1 text-muted"/>
      {{ project.total_duration }}
      <icon :icon="['fas', 'list']" class="ml-3 mr-1 text-muted"/>
      {{ project.total_entries }}
    </div>
    <div v-if="project.percent_done" class="card-subtitle h6 w-100">
      <div class="progress w-100">
        <div
          :class="['progress-bar', [project.percent_done > 100 ? 'bg-danger' : '']]"
          :style="{ width: project.percent_done + '%' }">
          {{ project.percent_done }}%
        </div>
      </div>
    </div>
  </template>
</card>
</template>


<script>
import {mapActions} from 'vuex';

import Card from '../cards/card.vue';


export default {
  components: {
    Card,
  },
  props: {
    project: {
      type: Object,
      default: () => {
        return {
          id: null,
        }
      },
    },
    index: {
      type: Number,
      default: null,
    },
  },
  methods: {
    ...mapActions({
      deleteProject: 'projects/deleteProject',
    }),
  },
};
</script>
