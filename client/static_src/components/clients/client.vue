<template>
<card
  :index="index"
  @modal="$emit('modal')"
  @delete="deleteClient(index)">
  <template slot="card-body">
    <div class="card-title h5 font-weight-bold">
      {{ client.name }}
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
