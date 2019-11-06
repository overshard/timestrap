<template>
<card
  :index="index"
  :delete_perm="$perms.delete_task"
  :change_perm="$perms.change_task"
  :add_perm="$perms.add_task"
  @edit="$emit('modal')"
  @detail="showEntries"
  @delete="deleteTask(task)">
  <template slot="card-body">
    <div class="card-title h5 font-weight-bold mb-4">
      {{ task.name }}
    </div>
    <div v-if="task.hourly_rate" class="card-subtitle h6">
      <icon :icon="['fas', 'hand-holding-usd']" class="mr-1 text-muted"/>
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

    showEntries(){
      if(!this.task.id){
        this.$emit('modal');
        return;
      }
      this.$store.commit("reports/reset");
      this.$store.commit("reports/setTask", this.task.url);
      this.$router.push("/reports");
    }
  },
};
</script>
