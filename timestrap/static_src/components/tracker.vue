<template>
<div class="bg-light py-2">
    <div id="tracker" class="container">
        <div class="row">
            <div class="col-sm-2">
                <select2 id="entry-project" v-model="project" name="entry-project"
                         v-bind:options="projects" placeholder="Project"></select2>
            </div>
            <div class="col-sm-2">
                <select2 id="entry-task" v-model="task" name="entry-task"
                         v-bind:options="tasks" placeholder="Task"></select2>
            </div>
            <div class="col-sm-4">
                <input class="form-control form-control-sm w-100"
                       name="entry-note" placeholder="Note" type="text"
                       @keydown.enter="submitEntry" v-model="note" />
            </div>
            <div class="col-sm-2">
                <input class="form-control form-control-sm text-right font-weight-bold w-100"
                       name="entry-duration" placeholder="0:00" type="text"
                       @keydown.enter="submitEntry" v-model="duration" />
            </div>
            <div class="col-sm-2">
                <button class="btn btn-sm btn-success w-100"
                        v-on:click="toggle" v-block-during-fetch
                        v-if="!this.running && !this.duration">
                    <i class="fa fa-play" aria-hidden="true"></i>
                    Start
                </button>
                <button class="btn btn-sm btn-danger w-100"
                        v-on:click="toggle" v-block-during-fetch
                        v-if="this.running">
                    <i class="fa fa-stop" aria-hidden="true"></i>
                    Stop ({{ this.seconds }})
                </button>
                <button class="btn btn-sm btn-info w-100"
                        name="entry-add-submit"
                        v-on:click="submitEntry" v-block-during-fetch
                        v-if="!this.running && this.duration">
                    <i class="fa fa-plus" aria-hidden="true"></i>
                    Add
                </button>
            </div>
        </div>
    </div>
</div>
</template>


<script>
import {mapGetters, mapActions} from 'vuex';

import Select2 from './select2.vue';
import DurationFormatter from '../mixins/durationformatter';


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
                user: timestrapConfig.USER.URL
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
    components: {
        Select2,
    },
};
</script>
