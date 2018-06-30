<template>
  <div class="bg-light py-2">
    <form
      id="tracker"
      class="container"
      @submit.prevent>
      <div class="row">
        <div
          class="col-sm-2"
          @keyup.enter.prevent>
          <select2
            id="tracker-project"
            v-model="project"
            :options="projects"
            placeholder="Project"
            required/>
        </div>
        <div
          class="col-sm-2"
          @keyup.enter.prevent>
          <select2
            id="tracker-task"
            v-model="task"
            :options="tasks"
            placeholder="Task"
            required/>
        </div>
        <div class="col-sm-4">
          <input
            id="tracker-note"
            v-model="note"
            class="form-control form-control-sm w-100"
            name="entry-note"
            placeholder="Note"
            type="text">
        </div>
        <div class="col-sm-2">
          <input
            id="tracker-duration"
            v-model="duration"
            class="form-control form-control-sm text-right font-weight-bold w-100"
            placeholder="0:00"
            type="text"
            required>
        </div>
        <div class="col-sm-2">
          <button
            v-if="!running && !duration"
            class="btn btn-sm btn-success w-100"
            @click="toggle">
            <i class="fa fa-play"/>
            Start
          </button>
          <button
            v-if="running"
            class="btn btn-sm btn-danger w-100"
            @click="toggle">
            <i class="fa fa-stop"/>
            Stop ({{ seconds }})
          </button>
          <button
            v-if="!running && duration"
            id="tracker-submit"
            class="btn btn-sm btn-info w-100"
            type="submit"
            @click="submitEntry">
            <i class="fa fa-plus"/>
            Add
          </button>
        </div>
      </div>
    </form>
  </div>
</template>


<script>
import {mapGetters, mapActions} from 'vuex';

import Select2 from './select2.vue';
import DurationFormatter from '../mixins/durationformatter';


export default {
  components: {
    Select2,
  },
  mixins: [
    DurationFormatter,
  ],
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
      projects: 'clients/getSelectProjects',
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
      this.duration = this.secondsToString(this.total);
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
