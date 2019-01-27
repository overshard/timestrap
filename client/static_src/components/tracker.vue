<template>
<div class="bg-light py-2">
  <form
    id="tracker"
    class="container-fluid"
    @submit.prevent="submitEntry">
    <div class="row">
      <div class="col-sm-4">
        <input
          id="tracker-note"
          v-model="note"
          class="form-control w-100 shadow-sm"
          placeholder="Note"
          type="text">
      </div>
      <div
        class="col-sm-2"
        @keyup.enter.prevent>
        <selector
          id="tracker-project"
          v-model="project"
          :options="projects"
          :selected="project"
          placeholder="Project"
          required/>
      </div>
      <div
        class="col-sm-2"
        @keyup.enter.prevent>
        <selector
          id="tracker-task"
          v-model="task"
          :options="tasks"
          :selected="task"
          placeholder="Task"
          required/>
      </div>
      <div class="col-sm-2">
        <input
          id="tracker-duration"
          v-model="duration"
          class="form-control text-right font-weight-bold w-100 shadow-sm"
          placeholder="0:00"
          type="text"
          required>
      </div>
      <div class="col-sm-2">
        <button
          v-if="!running && !duration"
          class="btn btn-success w-100"
          @click.prevent.exact="toggle">
          <icon :icon="['fas', 'play']" class="mr-1"/>
          Start
        </button>
        <button
          v-if="running"
          class="btn btn-danger w-100"
          @click.prevent.exact="toggle">
          <icon :icon="['fas', 'stop']" class="mr-1"/>
          Stop ({{ seconds }})
        </button>
        <button
          v-if="!running && duration"
          id="tracker-submit"
          class="btn btn-info w-100"
          type="submit">
          <icon :icon="['fas', 'plus']" class="mr-1"/>
          Add
        </button>
      </div>
    </div>
  </form>
</div>
</template>


<script>
import {mapGetters, mapActions} from 'vuex';

import Selector from './selector.vue';
import Datepicker from './datepicker.vue';


export default {
  components: {
    Selector,
    Datepicker,
  },
  data() {
    return {
      task: null,
      project: null,
      note: null,
      duration: null,
      datetimeStart: null,
      datetimeEnd: null,

      running: false,
      total: 0,
      seconds: '0',
    };
  },
  computed: {
    ...mapGetters({
      tasks: 'tasks/getSelectTasks',
      projects: 'projects/getSelectProjects',
      users: 'users/getSelectUsers',
    }),
  },
  methods: {
    ...mapActions({
      createEntry: 'entries/createEntry',
    }),
    submitEntry() {
      this.createEntry({
        task: this.task,
        project: this.project,
        note: this.note,
        duration: this.duration,
        datetime_start: this.datetimeStart,
        datetime_end: this.datetimeEnd,
        user: timestrapConfig.USER.URL,
        date: this.$moment().format('YYYY-MM-DD'),
      });
      this.reset();
      this.note = null;
    },
    reset() {
      this.duration = null;
      this.total = 0;
      this.seconds = '0';
    },
    tick() {
      this.total = Math.floor(
        (Date.now() - this.datetimeStart.valueOf()) / 1000
      );
      this.seconds = this.total % 3600 % 60;
      this.duration = this.$moment.duration(this.total, 'seconds').format('h:mm', {trim: false});
      document.title = this.duration + ' — ' + timestrapConfig.SITE.NAME;
    },
    toggle() {
      this.running = !this.running;
      if (this.running) {
        this.datetimeStart = new Date(Date.now());
        this.reset();
        this.interval = setInterval(this.tick, 1000, this);
      } else {
        this.datetimeEnd = new Date(Date.now());
        clearInterval(this.interval);
        if (this.total < 60) this.reset();
        document.title = 'Application — ' + timestrapConfig.SITE.NAME;
      }
    },
  },
};
</script>
