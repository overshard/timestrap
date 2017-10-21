<template>
<modal>
    <h5 slot="header">
        {{ config.entry ? 'Edit Entry' : 'New Entry' }}
    </h5>

    <div slot="body">
        <div class="form-group">
            <label>Date</label>
            <datepicker name="entry-date"
                        type="text"
                        class="form-control form-control-sm date-input"
                        v-model="date"
                        v-bind:default="new Date()"
                        placeholder="Date"></datepicker>
        </div>
        <div class="form-group">
            <label>Projects</label>
            <select2 id="project-projects"
                        v-model="project"
                        v-bind:options="projects"
                        v-bind:selected="project"
                        placeholder="Projects"></select2>
        </div>
        <div class="form-group">
            <label>Tasks</label>
            <select2 id="project-tasks"
                        v-model="task"
                        v-bind:options="tasks"
                        v-bind:selected="task"
                        placeholder="Tasks"></select2>
        </div>
        <div class="form-group">
            <label>Note</label>
            <input name="project-note"
                    type="text"
                    class="form-control form-control-sm"
                    v-model.trim="entry_note"
                    placeholder="Entry Note"
                    required />
        </div>
        <div class="form-group">
            <label>Duration</label>
            <input name="project-duration"
                    type="text"
                    class="form-control form-control-sm"
                    placeholder="0:00"
                    v-model.number="entry_duration" />
        </div>
    </div>

    <div slot="footer">
        <button name="entry-modal-cancel"
                type="button"
                class="btn btn-secondary"
                @click="$emit('close')">
            Close
        </button>
        <button name="entry-modal-submit"
                type="submit"
                class="btn btn-primary"
                @click="submit">
            {{ config.entry ? 'Save Changes' : 'Add Entry' }}
        </button>
    </div>
</modal>
</template>

<script>
const Modal = require('./modal.vue');
const Select2 = require('./select2.vue');
const Datepicker = require('./datepicker.vue');

export default {
    props: ['config'],
    data() {
        return {
            projects: null,
            tasks: null,
            task: this.config.entry ? this.config.entry.task : null,
            project: this.config.entry ? this.config.entry.project : null,
            entry_date: this.config.entry ? this.config.entry.date : null,
            entry_note: this.config.entry ? this.config.entry.note : null,
            entry_duration: this.config.entry ? this.config.entry.duration : null
        };
    },
    methods: {
        submit() {
            let body = {
                note: this.entry_note,
                duration: this.entry_duration,
                date: this.entry_date,
                project: this.project,
                task: this.task
            };
            let url = timestrapConfig.API_URLS.ENTRIES;
            let method = 'post';
            if (this.config.entry) {
                url = this.config.entry.url;
                method = 'put';
            }
            this.$quickFetch(url, method, body).then(data => {
                this.$emit('updateEntry', data, this.config.index, this.config.client_index);
                this.task = null;
                this.project = null;
                this.entry_date = null;
                this.entry_note = null;
                this.entry_duration = null;
                this.$emit('close');
            }).catch(error => console.log(error));
        }
    },
    created() {
        this.$quickFetch(timestrapConfig.API_URLS.CLIENTS).then(data => {
            this.projects = data.map(function(client) {
                let projects = client.projects.map(function(project) {
                    return { id: project.url, text: project.name };
                });
                return { text: client.name, children: projects };
            });
        });
        this.$quickFetch(timestrapConfig.API_URLS.TASKS).then(data => {
            this.tasks = data.map(function(task) {
                return { id: task.url, text: task.name };
            });
        });
    },
    components: {
        Modal,
        Select2,
        Datepicker
    }
};
</script>
