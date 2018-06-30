<template>
  <modal>
    <h5 slot="header">
      {{ config.entry ? 'Edit Entry' : 'New Entry' }}
    </h5>

    <div slot="body">
      <form
        @submit.prevent
        @keyup.enter="submit">
        <div class="form-group">
          <label>Date</label>
          <datepicker
            id="entry-modal-date"
            v-model="date"
            :default="date"
            type="text"
            class="form-control form-control-sm date-input"
            placeholder="Date"
            @keyup.enter.prevent/>
        </div>
        <div class="form-group">
          <label>User</label>
          <select2
            id="entry-modal-user"
            v-model="user"
            :options="users"
            :selected="user"
            placeholder="Users"
            @keyup.enter.prevent/>
        </div>
        <div class="form-group">
          <label>Projects</label>
          <select2
            id="entry-modal-project"
            v-model="project"
            :options="projects"
            :selected="project"
            placeholder="Projects"/>
        </div>
        <div class="form-group">
          <label>Tasks</label>
          <select2
            id="entry-modal-task"
            v-model="task"
            :options="tasks"
            :selected="task"
            placeholder="Tasks"/>
        </div>
        <div class="form-group">
          <label>Note</label>
          <input
            id="entry-modal-note"
            v-model.trim="note"
            type="text"
            class="form-control form-control-sm"
            placeholder="Entry Note"
            required >
        </div>
        <div class="form-group">
          <label>Duration</label>
          <input
            id="entry-modal-duration"
            v-model="duration"
            type="text"
            class="form-control form-control-sm"
            placeholder="0:00" >
        </div>
      </form>
    </div>

    <div slot="footer">
      <button
        id="entry-modal-close"
        type="button"
        class="btn btn-secondary"
        @click="$emit('close')">
        Close
      </button>
      <button
        id="entry-modal-submit"
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


export default {
  components: {
    Modal,
    Select2,
    Datepicker,
  },
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
      duration: this.config.entry ? this.$moment.duration(this.config.entry.duration, 'hours').format('h:mm', {trim: false}) : null,
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
