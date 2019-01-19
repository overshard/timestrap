<template>
<cards :number-of-elements="tasks(search).length" @search="search = $event">
  <template slot="cards-title">
    <icon :icon="['fas', 'tasks']" class="text-muted mr-2"/>
    Tasks
  </template>

  <template slot="cards-list">
    <task
      v-for="(task, index) in tasks(search)"
      :key="task.id"
      :task="task"
      :index="index"
      @modal="modalToggle(task)"/>
    <task
      @modal="modalToggle()"/>
  </template>

  <task-modal
    slot="cards-modal"
    v-if="modalShow"
    :task="modalTask"
    @close="modalShow = false"/>
</cards>
</template>


<script>
import {mapGetters, mapActions} from 'vuex';

import Cards from '../cards/cards.vue';
import Task from './task.vue';
import TaskModal from './task-modal.vue';


export default {
  components: {
    Cards,
    Task,
    TaskModal,
  },
  data() {
    return {
      search: '',
      modalTask: null,
      modalShow: false,
    };
  },
  computed: {
    ...mapGetters({
      tasks: 'tasks/getSearchTasks',
    }),
  },
  methods: {
    modalToggle: function(task) {
      if (typeof(task) !== 'undefined') this.modalTask = task;
      else this.modalTask = null;
      this.modalShow = !this.modalShow;
    },
  }
};
</script>
