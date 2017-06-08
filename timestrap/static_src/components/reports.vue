<template>
<div class="container">
    <div class="row py-2 mb-4 bg-faded rounded">
        <div class="col-12">
            <button id="export-report" class="btn btn-primary btn-sm" v-on:click="exportReport">
                <i class="fa fa-download" aria-hidden="true"></i>
                Export Report
            </button>

            <select class="custom-select form-control-sm" v-model="exportFormat">
                <option value="csv">csv</option>
                <option value="xls">xls</option>
                <option value="xlsx">xlsx</option>
                <option value="tsv">tsv</option>
                <option value="ods">ods</option>
                <option value="json">json</option>
                <option value="yaml">yaml</option>
                <option value="html">html</option>
            </select>

            <pager v-bind:next="next"
                   v-bind:previous="previous"
                   @next-page="getEntries(next)"
                   @previous-page="getEntries(previous)"></pager>
        </div>
    </div>

    <form name="report-filters"
          class="row mb-4 pt-3 pb-1 bg-faded rounded"
          v-on:submit.prevent
          v-on:submit="getReport">
        <div class="col-sm-6">
            <div class="form-group">
                <select2 id="report-filter-user"
                         v-model="user"
                         v-bind:options="users"
                         placeholder="Users"
                         @select2-select="selectUserOption"></select2>
            </div>
            <div class="form-group">
                <select2 id="report-filter-project"
                         v-model="project"
                         v-bind:options="projects"
                         placeholder="Projects"
                         @select2-select="selectProjectOption"></select2>
            </div>
            <div class="form-group">
                <select2 id="report-filter-client"
                         v-model="client"
                         v-bind:options="clients"
                         placeholder="Clients"
                         @select2-select="selectClientOption"></select2>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="form-group">
                <select2 id="report-filter-task"
                         v-model="task"
                         v-bind:options="tasks"
                         placeholder="Tasks"
                         @select2-select="selectTaskOption"></select2>
            </div>
            <div class="form-group">
                <div class="row">
                    <div class="col-md-6">
                        <datepicker id="report-filter-min-date"
                                    type="text"
                                    class="form-control form-control-sm date-input"
                                    v-model="dateMin"
                                    placeholder="Min. date"
                                    @datepicker-select="dateMinSelect"></datepicker>
                    </div>
                    <div class="col-md-6">
                        <datepicker id="report-filter-max-date"
                                    type="text"
                                    class="form-control form-control-sm date-input"
                                    v-model="dateMax"
                                    placeholder="Max. date"
                                    @datepicker-select="dateMaxSelect"></datepicker>
                    </div>
                </div>
            </div>
            <button id="generate-report" type="submit" class="btn btn-primary btn-sm w-100">
                Generate Report
            </button>
        </div>
    </form>

    <div class="mb-4" v-for="entryBlock in entries">
        <div class="row inset-row">
            <div class="col-12">
                <h2 class="display-4 text-muted">
                    {{ moment(entryBlock.date) }}
                </h2>
            </div>
        </div>
        <div class="entry-rows rounded">
            <entry v-for="(entry, index) in entryBlock.entries"
                v-bind:entry="entry"
                v-bind:index="index"
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
const Datepicker = require('./datepicker.vue');
const Entry = require('./entry.vue');
const Pager = require('./pager.vue');
const Select2 = require('./select2.vue');

export default {
    data() {
        return {
            entries: null,
            subtotal: null,
            total: null,
            next: null,
            previous: null,
            exportFormat: 'csv',
            project__client: null,
            dateMin: null,
            dateMax: null,
            editable: false,
            user: null,
            users: {},
            client: null,
            clients: {},
            project: null,
            projects: {},
            task: null,
            tasks: {}
        };
    },
    methods: {
        getEntries(url) {
            toggleButtonBusy($('#generate-report'));
            toggleButtonBusy($('#export-report'));

            let userEntries = timestrapConfig.API_URLS.ENTRIES;
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
                    this.entries.push({
                        date: date,
                        entries: data.results.filter(entry => {
                            return entry.date === date;
                        })
                    });
                });

                this.subtotal = durationToString(data.subtotal_duration);
                this.total = durationToString(data.total_duration);

                toggleButtonBusy($('#generate-report'));
                toggleButtonBusy($('#export-report'));
            });
        },
        getReport() {
            const query = {
                user: this.user,
                project: this.project,
                project__client: this.client,
                min_date: this.dateMin,
                max_date: this.dateMax,
                task: this.task
            };
            const url = timestrapConfig.API_URLS.ENTRIES + '?' + $.param(query);
            this.getEntries(url);
        },
        exportReport() {
            const query = {
                user: this.user,
                project: this.project,
                project__client: this.client,
                min_date: this.dateMin,
                max_date: this.dateMax,
                task: this.task,
                exportFormat: this.exportFormat
            };
            document.location.href = timestrapConfig.CORE_URLS.REPORTS_EXPORT + '?' + $.param(query);
        },
        loadSelect2Options() {
            let users = quickFetch(timestrapConfig.API_URLS.USERS);
            let clients = quickFetch(timestrapConfig.API_URLS.CLIENTS);
            let tasks = quickFetch(timestrapConfig.API_URLS.TASKS);
            Promise.all([users, clients, tasks]).then(data => {
                this.users = data[0].map(function(user) {
                    return { id: user.id, text: user.username };
                });
                this.clients = data[1].map(function(client) {
                    return { id: client.id, text: client.name };
                });
                this.projects = data[1].map(function(client) {
                    let projects = client.projects.map(function(project) {
                        return { id: project.id, text: project.name };
                    });
                    return { text: client.name, children: projects };
                });
                this.tasks = data[2].map(function(task) {
                    return { id: task.id, text: task.name };
                });
            });
        },
        selectUserOption(user) {
            this.user = user;
        },
        selectClientOption(client) {
            this.client = client;
        },
        selectProjectOption(project) {
            this.project = project;
        },
        selectTaskOption(task) {
            this.task = task;
        },
        dateMinSelect(date) {
            this.dateMin = date;
        },
        dateMaxSelect(date) {
            this.dateMax = date;
        },
        moment(date) {
            return moment(date).format('LL');
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
