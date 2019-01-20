<template>
<card-modal
  :data="$data"
  :edit="editEntry"
  :create="createEntry"
  @close="$emit('close')">
  <template slot="modal-body">
    <div class="form-group row">
      <label for="entry-note" class="col-sm-4 col-form-label text-muted">
        Note
      </label>
      <div class="col-sm-8">
        <input
          class="form-control shadow-sm"
          id="entry-note"
          name="entry-note"
          ref="entry-note"
          v-model="note"
          placeholder="Empty"/>
      </div>
    </div>
    <div class="form-group row">
      <label for="entry-task" class="col-sm-4 col-form-label text-muted">
        Tasks
      </label>
      <div class="col-sm-8">
        <selector
          id="entry-task"
          v-model="task"
          :options="tasks"
          :selected="task"/>
      </div>
    </div>
    <div class="form-group row">
      <label for="entry-project" class="col-sm-4 col-form-label text-muted">
        Project
      </label>
      <div class="col-sm-8">
        <selector
          id="entry-project"
          v-model="project"
          :options="projects"
          :selected="project"/>
      </div>
    </div>
    <div class="form-group row">
      <label for="entry-user" class="col-sm-4 col-form-label text-muted">
        User
      </label>
      <div class="col-sm-8">
        <selector
          id="entry-user"
          v-model="user"
          :options="users"
          :selected="user"/>
      </div>
    </div>
    <div class="form-group row">
      <label for="entry-date" class="col-sm-4 col-form-label text-muted">
        Date
      </label>
      <div class="col-sm-8">
        <input
          class="form-control shadow-sm"
          id="entry-date"
          name="entry-date"
          v-model="date"
          placeholder="Empty"/>
      </div>
    </div>
    <div class="form-group row">
      <label for="entry-duration" class="col-sm-4 col-form-label text-muted">
        Duration
      </label>
      <div class="col-sm-8">
        <input
          class="form-control shadow-sm"
          id="entry-duration"
          name="entry-duration"
          v-model="duration"
          placeholder="Empty"/>
      </div>
    </div>
    <div class="form-group row">
      <label for="entry-datetime_start" class="col-sm-4 col-form-label text-muted">
        Start Date/Time
      </label>
      <div class="col-sm-8">
        <input
          class="form-control shadow-sm"
          id="entry-datetime_start"
          name="entry-datetime_start"
          v-model="datetime_start"
          placeholder="Empty"
          disabled/>
        <small class="form-text text-muted">
          Only available if started and stopped via the tracker.
        </small>
      </div>
    </div>
    <div class="form-group row">
      <label for="entry-datetime_end" class="col-sm-4 col-form-label text-muted">
        End Date/Time
      </label>
      <div class="col-sm-8">
        <input
          class="form-control shadow-sm"
          id="entry-datetime_end"
          name="entry-datetime_end"
          v-model="datetime_end"
          placeholder="Empty"
          disabled/>
        <small class="form-text text-muted">
          Only available if started and stopped via the tracker.
        </small>
      </div>
    </div>
  </template>
</card-modal>
</template>


<script>
import {mapActions, mapGetters} from 'vuex';

import Selector from '../selector.vue';
import CardModal from '../cards/card-modal.vue';


export default {
  components: {
    Selector,
    CardModal,
  },
  props: {
    entry: {
      type: Object,
    },
  },
  data() {
    return {
      id: this.entry ? this.entry.id : null,
      url: this.entry ? this.entry.url : null,
      task: this.entry ? this.entry.task : null,
      project: this.entry ? this.entry.project : null,
      user: this.entry ? this.entry.user : null,
      date: this.entry ? this.entry.date : null,
      duration: this.entry ? this.entry.duration : null,
      datetime_start: this.entry ? this.entry.datetime_start : null,
      datetime_end: this.entry ? this.entry.datetime_end : null,
      note: this.entry ? this.entry.note : null,
    }
  },
  computed: {
    ...mapGetters({
      projects: 'projects/getSelectProjects',
      tasks: 'tasks/getSelectTasks',
      users: 'users/getSelectUsers',
    }),
  },
  methods: {
    ...mapActions({
      editEntry: 'entries/editEntry',
      createEntry: 'entries/createEntry',
    }),
  },
  mounted() {
    this.$refs['entry-note'].focus();
  },
};
</script>
