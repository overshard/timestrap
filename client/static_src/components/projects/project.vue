<template>
<card
  :index="index"
  @modal="$emit('modal')"
  @delete="deleteProject(project)">
  <template slot="card-body">
    <div class="d-flex flex-column h-100">
      <div class="card-title h5 font-weight-bold">
        {{ project.name }}
      </div>
      <div v-if="project.client" class="card-subtitle h6 text-muted mb-4">
        for <strong>{{ getClient(project.client).name }}</strong>
      </div>
      <div v-if="project.total_duration && project.total_entries" class="card-subtitle h6 mb-5 flex-grow-1">
        <icon :icon="['fas', 'list']" class="mr-1 text-muted"/>
        {{ project.total_entries }}
        <icon :icon="['fas', 'clock']" class="ml-3 mr-1 text-muted"/>
        {{ project.total_duration }}
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
    </div>
  </template>
</card>
</template>


<script>
import {mapActions, mapGetters} from 'vuex';

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
  computed: {
    ...mapGetters({
      getClient: 'clients/getClient',
    }),
  },
  methods: {
    ...mapActions({
      deleteProject: 'projects/deleteProject',
    }),
  },
};
</script>
