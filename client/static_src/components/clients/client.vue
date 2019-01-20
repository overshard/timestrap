<template>
<card
  :index="index"
  @modal="$emit('modal')"
  @delete="deleteClient(client)">
  <template slot="card-body">
    <div class="card-title h5 font-weight-bold mb-4">
      {{ client.name }}
    </div>
    <div v-if="client.total_duration && client.total_projects" class="card-subtitle h6">
      <icon :icon="['fas', 'briefcase']" class="mr-1 text-muted"/>
      {{ client.total_projects }}
      <icon :icon="['fas', 'clock']" class="ml-3 mr-1 text-muted"/>
      {{ client.total_duration }}
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
    client: {
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
      deleteClient: 'clients/deleteClient',
    }),
  },
};
</script>
