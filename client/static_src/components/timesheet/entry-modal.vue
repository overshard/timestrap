<template>
  <modal>
    <h5 slot="header">
      {{ config.entry ? 'Edit Entry' : 'New Entry' }}
    </h5>

    <div slot="body">
      <div class="form-group">
        <label>Date</label>
        <datepicker
          v-model="date"
          :default="date"
          name="entry-date"
          type="text"
          class="form-control form-control-sm date-input"
          placeholder="Date"/>
      </div>
      <div class="form-group">
        <label>User</label>
        <select2
          id="entry-user"
          v-model="user"
          :options="users"
          :selected="user"
          placeholder="Users"/>
      </div>
      <div class="form-group">
        <label>Projects</label>
        <select2
          id="entry-projects"
          v-model="project"
          :options="projects"
          :selected="project"
          placeholder="Projects"/>
      </div>
      <div class="form-group">
        <label>Tasks</label>
        <select2
          id="entry-tasks"
          v-model="task"
          :options="tasks"
          :selected="task"
          placeholder="Tasks"/>
      </div>
      <div class="form-group">
        <label>Note</label>
        <input
          v-model.trim="note"
          name="entry-note"
          type="text"
          class="form-control form-control-sm"
          placeholder="Entry Note"
          required >
      </div>
      <div class="form-group">
        <label>Duration</label>
        <input
          v-model="duration"
          name="entry-duration"
          type="text"
          class="form-control form-control-sm"
          placeholder="0:00" >
      </div>
    </div>

    <div slot="footer">
      <button
        name="entry-modal-cancel"
        type="button"
        class="btn btn-secondary"
        @click="$emit('close')">
        Close
      </button>
      <button
        name="entry-modal-submit"
        type="submit"
        class="btn btn-primary"
        @click="submit">
        {{ config.entry ? 'Save Changes' : 'Add Entry' }}
      </button>
    </div>
  </modal>
</template>

<script>
import {mapGetters, mapActions} from 'vuex';

import Modal from '../modal.vue';
import Select2 from '../select2.vue';
import Datepicker from '../datepicker.vue';
import DurationFormatter from '../../mixins/durationformatter';


export default {
  components: {
    Modal,
    Select2,
    Datepicker,
  },
  mixins: [
    DurationFormatter,
  ],
  props: [
    'config',
  ],
  data() {
    return {
      id: this.config.entry ? this.config.entry.id : null,
      url: this.config.entry ? this.config.entry.url : null,
      user: this.config.entry ? this.config.entry.user : null,
      task: this.config.entry ? this.config.entry.task : null,
      project: this.config.entry ? this.config.entry.project : null,
      date: this.config.entry ? this.config.entry.date : null,
      note: this.config.entry ? this.config.entry.note : null,
      duration: this.config.entry ? this.durationToString(this.config.entry.duration) : null,
    };
  },
  computed: {
    ...mapGetters({
      tasks: 'tasks/getSelectTasks',
      projects: 'clients/getSelectProjects',
      users: 'users/getSelectUsers',
    }),
  },
  methods: {
    ...mapActions({
      createEntry: 'entries/createEntry',
      editEntry: 'entries/editEntry',
    }),
    submit() {
      if (!this.id) this.createEntry(this.$data);
      else this.editEntry(this.$data);
      this.$emit('close');
    },
  },
};
</script>
