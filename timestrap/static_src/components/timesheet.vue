<template>
<div class="container">
    <div class="row py-2 mb-4 bg-faded rounded">
        <div class="col-12">
            <router-link to="/reports/" class="btn btn-primary btn-sm">
                <i class="fa fa-book" aria-hidden="true"></i>
                Create Reports
            </router-link>
            <pager :next="next"
                   :previous="previous"
                   @next-page="getEntries(next)"
                   @previous-page="getEntries(previous)"></pager>
        </div>
    </div>

    <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top">
        <div class="col-sm-3 mb-2">
            Date
        </div>
        <div class="col-sm-3 mb-2">
            Task
        </div>
        <div class="col-sm-6">
        </div>
        <div class="col-sm-3">
            Project
        </div>
        <div class="col-sm-5">
            Note
        </div>
        <div class="col-sm-2">
            Duration
        </div>
        <div class="col-sm-2">
        </div>
    </div>


    <form name="entry-add"
          class="row mb-4 py-2 bg-faded rounded-bottom"
          v-if="global.perms.add_entry"
          v-on:submit.prevent
          v-on:submit="submitEntry">
        <div class="col-sm-3 mb-2">
            <datepicker-input @date-select="dateSelect"></datepicker-input>
        </div>
        <div class="col-sm-3">
            <select2 :options="tasks"
                     @select2-select="taskSelectOption"></select2>
        </div>
        <div class="col-sm-6">
        </div>
        <div class="col-sm-3">
            <projects-select @project-select="projectSelect"></projects-select>
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
                    class="btn btn-success btn-sm w-100">
                Add
            </button>
        </div>
    </form>

    <div class="mb-4" v-for="(entryBlock, blockIndex) in entries">
        <div class="row inset-row">
            <div class="col-12">
                <h2 class="display-4 text-muted">
                    {{ moment(entryBlock.date) }}
                </h2>
            </div>
        </div>
        <div class="entry-rows rounded">
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
        <div class="offset-sm-6 col-sm-2 text-right">
            Subtotal<br>
            <strong>Total</strong>
        </div>
        <div class="col-sm-2 text-right">
            {{ subtotal }}<br>
            <strong>{{ total }}</strong>
        </div>
    </div>
</div>
</template>


<script>
const Pager = require('./pager.vue');
const Entry = require('./entry.vue');
const TasksSelect = require('./tasks-select.vue');
const ProjectsSelect = require('./projects-select.vue');
const DatepickerInput = require('./datepicker-input.vue');
const Select2 = require('./select2.vue');

export default {
    data() {
        return {
            entries: null,
            clients: null,
            subtotal: null,
            total: null,
            next: null,
            previous: null,
            editable: true,
            tasks: {}
        };
    },
    methods: {
        getEntries(url) {
            let userEntries = timestrapConfig.API_URLS.ENTRIES + '?user=' + timestrapConfig.USER.ID;
            url = (typeof url !== 'undefined') ? url : userEntries;

            let entriesFetch = quickFetch(url);

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

                this.subtotal = durationToString(data.subtotal_duration);
                this.total = durationToString(data.total_duration);
            });
        },
        submitEntry() {
            let body = {
                date: this.date,
                task: this.task,
                project: this.project,
                note: this.note,
                duration: this.duration,
                user: timestrapConfig.USER.URL
            };
            quickFetch(timestrapConfig.API_URLS.ENTRIES, 'post', body).then(data => {
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
        },
        loadTaskOptions() {
            quickFetch(timestrapConfig.API_URLS.TASKS).then(data => {
                this.tasks = data.map(function(task){
                   return {id: task.url, text: task.name}
                });
            });
        },
        taskSelectOption(task) {
            this.task = task;
        },
        projectSelect(project) {
            this.project = project;
        },
        dateSelect(date) {
            this.date = date;
        },
        moment(date) {
            return moment(date).format('LL');
        }
    },
    mounted() {
        this.loadTaskOptions();
        return this.getEntries();
    },
    components: {
        Pager,
        TasksSelect,
        ProjectsSelect,
        Entry,
        DatepickerInput,
        Select2
    }
};
</script>
