<template>
<div class="container">
    <div class="row py-2 mb-4 bg-light rounded">
        <div class="col-12">
            <router-link to="/reports/" class="btn btn-primary btn-sm">
                <i class="fa fa-book" aria-hidden="true"></i>
                Create Reports
            </router-link>

            <button class="btn btn-secondary btn-sm pull-right ml-2"
                    v-on:click.prevent
                    v-on:click="refresh">
                <i class="fa fa-refresh" aria-hidden="true"></i> Refresh
            </button>

            <pager v-bind:next="next"
                   v-bind:previous="previous"
                   @next-page="getEntries(next)"
                   @previous-page="getEntries(previous)"></pager>
        </div>
    </div>

    <div class="row py-1 bg-dark text-white font-weight-bold rounded-top">
        <template v-if="advancedMode">
            <div class="col-sm-3 mb-2">
                Date
            </div>
            <div class="col-sm-3 mb-2">
                Task
            </div>
            <div class="col-sm-6">
            </div>
        </template>
        <div class="col-sm-3">
            Project
        </div>
        <div class="col-sm-5">
            Note
        </div>
        <div class="col-sm-2">
            Duration
        </div>
        <div class="col-sm-2 text-right">
            <a href="#"
               id="entry-advanced-fields"
               v-on:click.prevent
               v-on:click="advanced"
               class="btn btn-secondary btn-sm w-100">
                Advanced
            </a>
        </div>
    </div>


    <form id="entry-add"
          class="row mb-4 py-2 bg-light rounded-bottom"
          v-if="this.$perms.add_entry"
          v-on:submit.prevent
          v-on:submit="submitEntry">
        <template v-if="advancedMode">
            <div class="col-sm-3 mb-2">
                <datepicker name="entry-date"
                            type="text"
                            class="form-control form-control-sm date-input"
                            v-model="date"
                            v-bind:default="new Date()"
                            placeholder="Date"></datepicker>
            </div>
            <div class="col-sm-3">
                <select2 id="entry-task"
                        v-model="task"
                        v-bind:options="tasks"
                        placeholder="Tasks"></select2>
            </div>
            <div class="col-sm-6">
            </div>
        </template>
        <div class="col-sm-3">
            <select2 id="entry-project"
                     v-model="project"
                     v-bind:options="projects"
                     placeholder="Projects"></select2>
        </div>
        <div class="col-sm-5">
            <input name="entry-note"
                   type="text"
                   class="form-control form-control-sm"
                   v-model="note"
                   placeholder="Note" />
        </div>
        <div class="col-sm-2">
            <input name="entry-duration"
                   type="text"
                   class="form-control form-control-sm text-right font-weight-bold"
                   v-model="duration"
                   placeholder="0:00"
                   required />
        </div>
        <div class="col-sm-2">
            <button name="entry-add-submit"
                    type="submit"
                    class="btn btn-success btn-sm w-100"
                    v-block-during-fetch>
                Add
            </button>
        </div>
    </form>

    <div v-if="this.$perms.view_entry" id="entry-rows">
        <div class="mb-4" v-for="(entryBlock, blockIndex) in entries">
            <div class="row inset-row">
                <div class="col-12">
                    <h2 class="display-4 text-muted">
                        {{ moment(entryBlock.date) }}
                    </h2>
                </div>
            </div>
            <div class="rounded">
                <entry v-for="(entry, entryIndex) in entryBlock.entries"
                       v-on:delete-entry="deleteEntry(blockIndex, entryIndex)"
                       v-bind:entry="entry"
                       v-bind:index="entryIndex"
                       v-bind:key="entry.id"
                       v-bind:editable="editable">
                </entry>
            </div>
        </div>

        <div class="row bg-success text-white py-2 mb-4 rounded">
            <div class="ml-auto col-sm-2 text-right">
                Subtotal<br>
                <strong>Total</strong>
            </div>
            <div class="col-sm-2 text-right">
                {{ subtotal }}<br>
                <strong>{{ total }}</strong>
            </div>
        </div>
    </div>
</div>
</template>


<script>
const Datepicker = require('./datepicker.vue');
const DurationFormatter = require('../mixins/durationformatter');
const Entry = require('./entry.vue');
const Pager = require('./pager.vue');
const Select2 = require('./select2.vue');

export default {
    mixins: [ DurationFormatter ],
    data() {
        return {
            entries: null,
            clients: null,
            subtotal: null,
            total: null,
            next: null,
            previous: null,
            editable: true,
            tasks: {},
            projects: {},
            advancedMode: false
        };
    },
    methods: {
        getEntries(url) {
            let userEntries = timestrapConfig.API_URLS.ENTRIES + '?user=' + timestrapConfig.USER.ID;
            url = (typeof url !== 'undefined') ? url : userEntries;

            let entriesFetch = this.$quickFetch(url);

            entriesFetch.then(data => {
                this.next = data.next;
                this.previous = data.previous;

                let uniqueDates = [];
                $.each(data.results, function(i, entry) {
                    if ($.inArray(entry.date, uniqueDates) === -1) {
                        uniqueDates.push(entry.date);
                    }
                });

                this.entries = [];
                uniqueDates.forEach(date => {
                    let entryBlock = Object;
                    this.entries.push({
                        date: date,
                        entries: data.results.filter(entry => {
                            return entry.date === date;
                        })
                    });
                });

                this.subtotal = this.durationToString(data.subtotal_duration);
                this.total = this.durationToString(data.total_duration);
            });
        },
        submitEntry(e) {
            let body = {
                date: this.date,
                task: this.task,
                project: this.project,
                note: this.note,
                duration: this.duration,
                user: timestrapConfig.USER.URL
            };
            this.$quickFetch(timestrapConfig.API_URLS.ENTRIES, 'post', body).then(data => {
                $.growl.notice({ message: 'New entry added!' });
                let entryAdded = false;
                this.entries.map(entryBlock => {
                    if (entryBlock.date === data.date) {
                        entryBlock.entries.unshift(data);
                        entryAdded = true;
                    }
                    return entryBlock;
                });
                if (!entryAdded) {
                    this.entries.unshift({
                        date: data.date,
                        entries: [data]
                    });
                }
                this.note = '';
                this.duration = '';
            }).catch(error => console.log(error));
        },
        deleteEntry: function(blockIndex, entryIndex) {
            this.entries[blockIndex].entries.splice(entryIndex, 1);
            if (this.entries[blockIndex].entries.length == 0) {
                this.entries.splice(blockIndex, 1);
            }
        },
        loadSelect2Options() {
            if (this.$perms.view_task) {
                this.$quickFetch(timestrapConfig.API_URLS.TASKS).then(data => {
                    this.tasks = data.map(function(task) {
                        return { id: task.url, text: task.name };
                    });
                });
            }
            if (this.$perms.view_client && this.$perms.view_project) {
                this.$quickFetch(timestrapConfig.API_URLS.CLIENTS).then(data => {
                    this.projects = data.map(function(client) {
                        let projects = client.projects.map(function(project) {
                            return { id: project.url, text: project.name };
                        });
                        return { text: client.name, children: projects };
                    });
                });
            }
        },
        moment(date) {
            return moment(date).format('LL');
        },
        advanced() {
            this.advancedMode = !this.advancedMode;
        },
        refresh() {
            return this.getEntries();
        }
    },
    mounted() {
        this.loadSelect2Options();
        return this.getEntries();
    },
    components: {
        Datepicker,
        Entry,
        Pager,
        Select2
    }
};
</script>
