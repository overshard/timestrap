<template>
<div class="bg-light py-2">
    <div id="tracker" class="container">
        <div class="row">
            <div class="col-sm-2">
                <select2 id="entry-project" v-model="project" name="entry-project"
                         v-bind:options="projects" placeholder="Project"></select2>
            </div>
            <div class="col-sm-2">
                <select2 id="entry-task" v-model="task" v-bind:options="tasks"
                         placeholder="Task" name="entry-task"></select2>
            </div>
            <div class="col-sm-4">
                <input class="form-control form-control-sm w-100"
                       name="entry-note" placeholder="Note" type="text"
                       v-model="note" />
            </div>
            <div class="col-sm-2">
                <input class="form-control form-control-sm text-right font-weight-bold w-100"
                       name="entry-duration" placeholder="0:00" type="text"
                       v-model="duration" />
            </div>
            <div class="col-sm-2">
                <button class="btn btn-sm btn-success w-100"
                        v-on:click="toggle" v-block-during-fetch
                        v-if="!this.running && !this.duration"
                        v-bind:disabled="submitted">
                    <i class="fa fa-play" aria-hidden="true"></i>
                    Start
                </button>
                <button class="btn btn-sm btn-danger w-100"
                        v-on:click="toggle" v-block-during-fetch
                        v-if="this.running" v-bind:disabled="submitted">
                    <i class="fa fa-stop" aria-hidden="true"></i>
                    Stop ({{ this.seconds }})
                </button>
                <button class="btn btn-sm btn-info w-100"
                        name="entry-add-submit"
                        v-on:click="submitEntry" v-block-during-fetch
                        v-if="!this.running && this.duration"
                        v-bind:disabled="submitted">
                    <i class="fa fa-plus" aria-hidden="true"></i>
                    Add
                </button>
            </div>
        </div>
    </div>
</div>
</template>


<script>
const Select2 = require('./select2.vue');
const DurationFormatter = require('../mixins/durationformatter');

export default {
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

            tasks: {},
            projects: {},

            running: false,
            total: 0,
            seconds: '0',

            submitted: false,
        };
    },
    methods: {
        submitEntry(e) {
            if (!this.project) {
                return $.growl.error({ message: 'Need to select a project.' });
            } else if (!this.duration) {
                return $.growl.error({ message: 'Need to add a duration.' });
            }
            let body = {
                task: this.task,
                project: this.project,
                note: this.note,
                duration: this.duration,
                datetime_start: this.datetimeStart,
                datetime_end: this.datetimeEnd,
                user: timestrapConfig.USER.URL
            };
            this.submitted = true;
            this.$quickFetch(timestrapConfig.API_URLS.ENTRIES, 'post', body).then(data => {
                $.growl.notice({ message: 'New entry added!' });
                this.reset();
                this.note = null;
                this.bus.$emit('refreshEntries');
                this.submitted = false;
            }).catch(error => console.log(error));
        },
        reset() {
            this.duration = null;

            this.total = 0;
            this.seconds = '0';
        },
        tick() {
            ++this.total;
            this.seconds = this.total % 3600 % 60;
            this.duration = this.secondsToString(this.total);
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
                if (this.total < 60) {
                    this.reset();
                }
            }
        },
    },
    mounted() {
        this.$quickFetch(timestrapConfig.API_URLS.TASKS).then(data => {
            this.tasks = data.map(function(task) {
                return { id: task.url, text: task.name };
            });
        });
        this.$quickFetch(timestrapConfig.API_URLS.CLIENTS).then(data => {
            this.projects = data.map(function(client) {
                let projects = client.projects.map(function(project) {
                    return { id: project.url, text: project.name };
                });
                return { text: client.name, children: projects };
            });
        });
    },
    components: {
        Select2,
    }
};
</script>
