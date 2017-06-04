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

            <pager :next="next"
                   :previous="previous"
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
                <!-- TODO: userSelect -->
            </div>
            <div class="form-group">
                <!-- TODO: projectSelect -->
            </div>
            <div class="form-group">
                <!-- TODO: clientSelect -->
            </div>
        </div>
        <div class="col-sm-6">
            <div class="form-group">
                <!-- TODO: taskSelect -->
            </div>
            <div class="form-group">
                <div class="row">
                    <div class="col-md-6">
                        <!-- TODO: minDateInput -->
                    </div>
                    <div class="col-md-6">
                        <!-- TODO: maxDateInput -->
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
const Pager = require('./pager.vue');
const Entry = require('./entry.vue');
const TasksSelect = require('./tasks-select.vue');
const ProjectsSelect = require('./projects-select.vue');
const DatepickerInput = require('./datepicker-input.vue');

export default {
    data() {
        return {
            entries: null,
            subtotal: null,
            total: null,
            next: null,
            previous: null,
            exportFormat: 'csv',
            user: null,
            project: null,
            project__client: null,
            min_date: null,
            max_date: null,
            task: null,
            editable: false
        };
    },
    methods: {
        getEntries(url) {
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
        getReport() {
            const query = {
                user: this.user,
                project: this.project,
                project__client: this.client,
                min_date: this.min_date,
                max_date: this.max_date,
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
                min_date: this.min_date,
                max_date: this.max_date,
                task: this.task,
                exportFormat: this.exportFormat
            };
            document.location.href = timestrapConfig.CORE_URLS.REPORTS_EXPORT + '?' + $.param(query);
        },
        taskSelect(task) {
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
        return this.getEntries();
    },
    components: {
        Pager,
        TasksSelect,
        ProjectsSelect,
        Entry,
        DatepickerInput
    }
};
</script>
