<template>
<card
  :index="index"
  @modal="$emit('modal')"
  @delete="deleteTask(index)">
  <template slot="card-body">
    <div class="card-title h5">
      {{ task.name }}
    </div>
    <div v-if="task.hourly_rate" class="card-subtitle h6 mb-2 badge badge-pill badge-secondary">
      ${{ task.hourly_rate }}/hr
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
    task: {
      type: Object,
      default: () => {
        return {
          id: null,
          url: null,
          name: null,
          hourly_rate: null,
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
      deleteTask: 'tasks/deleteTask',
    }),
  },
};
</script>
