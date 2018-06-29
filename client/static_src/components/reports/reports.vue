<template>
<div class="container">
    <div class="row py-2 mb-4 bg-light rounded">
        <div class="col-6">
            <template v-if="is_staff">
                <button id="export-report"
                        class="btn btn-primary btn-sm mr-1"
                        v-on:click="exportReport">
                    <i class="fa fa-download" aria-hidden="true"></i>
                    Export Report
                </button>
                <select class="export-select custom-select form-control-sm w-25" v-model="exportFormat">
                    <option value="csv">csv</option>
                    <option value="xls">xls</option>
                    <option value="tsv">tsv</option>
                    <option value="ods">ods</option>
                    <option value="json">json</option>
                    <option value="yaml">yaml</option>
                    <option value="html">html</option>
                </select>
            </template>
        </div>
        <div class="col-6">
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

    <form name="report-filters"
          class="row mb-4 pt-3 pb-1 bg-light rounded report-filters"
          v-on:submit.prevent
          v-on:submit="getReport">
        <div class="col-sm-6">
            <div class="form-group">
                <label>User</label>
                <select2 id="report-filter-user"
                         v-model="user"
                         v-bind:options="users"
                         placeholder="User"
                         allowclear></select2>
            </div>
            <div class="form-group">
                <label>Client</label>
                <select2 id="report-filter-client"
                         v-model="client"
                         v-bind:options="clients"
                         placeholder="Client"
                         allowclear></select2>
            </div>
            <div class="form-group pb-4">
                <label>Project</label>
                <select2 id="report-filter-project"
                         v-model="project"
                         v-bind:options="projects"
                         placeholder="Project"
                         allowclear></select2>
            </div>
            <div class="form-group">
                <div class="row">
                    <div class="col-md-6">
                        <select2 id="report-sort-by"
                                 v-model="orderBy"
                                 v-bind:options="orderByOptions"
                                 selected="date"
                                 placeholder="Order by"></select2>
                    </div>
                    <div class="col-md-6">
                        <select2 id="report-order-dir"
                                 v-model="orderDir"
                                 v-bind:options="orderDirOptions"
                                 selected="desc"
                                 placeholder="Order direction"></select2>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="form-group">
                <label>Task</label>
                <select2 id="report-filter-task"
                         v-model="task"
                         v-bind:options="tasks"
                         placeholder="Task"
                         allowclear></select2>
            </div>
            <div class="form-group">
                <label>Min. Date</label>
                <datepicker id="report-filter-min-date"
                            type="text"
                            class="form-control form-control-sm date-input"
                            v-model="dateMin"
                            placeholder="Min. date"
                            allowclear></datepicker>
            </div>
            <div class="form-group pb-4">
                <label>Max. Date</label>
                <datepicker id="report-filter-max-date"
                            type="text"
                            class="form-control form-control-sm date-input"
                            v-model="dateMax"
                            placeholder="Max. date"
                            allowclear></datepicker>
            </div>
            <button id="generate-report"
                    type="submit"
                    class="btn btn-primary btn-sm w-100">
                Generate Report
            </button>
        </div>
    </form>

    <div v-show="loading" class="container text-center py-4">
        <i class="fa fa-spinner text-primary fa-spin display-3 text-center"></i>
    </div>

    <div v-if="this.$perms.view_entry" id="entry-rows">
        <div class="mb-4">
            <div class="entry-rows rounded">
                <entry v-for="(entry, index) in entries"
                    v-bind:entry="entry"
                    v-bind:index="index"
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

    <div class="row py-2 mb-4 bg-light rounded">
        <div class="col-12">
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
</div>
</template>


<script>
import {mapGetters} from 'vuex';

import Datepicker from '../datepicker.vue';
import DurationFormatter from '../../mixins/durationformatter';
import Entry from '../entry.vue';
import Pager from '../pager.vue';
import Select2 from '../select2.vue';

import fetch from '../../fetch';


export default {
    mixins: [
        DurationFormatter
    ],
    data() {
        return {
            loading: true,
            is_staff: timestrapConfig.USER.IS_STAFF,
            entries: null,
            subtotal: null,
            total: null,
            next: null,
            previous: null,
            exportFormat: 'csv',
            orderByOptions: [
                { id: 'project__client__name', text: 'Client' },
                { id: 'date', text: 'Date' },
                { id: 'project__name', text: 'Project' },
                { id: 'task__name', text: 'Task' },
                { id: 'user__username', text: 'User' }
            ],
            orderBy: 'date',
            orderDirOptions: [
                { id: 'asc', text: 'Ascending' },
                { id: 'desc', text: 'Descending' }
            ],
            orderDir: 'desc',
            project__client: null,
            dateMin: null,
            dateMax: null,
            editable: false,
            user: null,
            client: null,
            project: null,
            task: null,
        };
    },
    computed: {
        ...mapGetters({
            tasks: 'tasks/getSelectTasks',
            projects: 'clients/getSelectProjects',
            clients: 'clients/getSelectClients',
            users: 'users/getSelectUsers',
        }),
    },
    methods: {
        getEntries(url) {
            let userEntries = timestrapConfig.API_URLS.ENTRIES;
            url = (typeof url !== 'undefined') ? url : userEntries;

            fetch(url).then(response => {
                this.next = response.data.next;
                this.previous = response.data.previous;

                this.entries = response.data.results;

                this.subtotal = this.durationToString(response.data.subtotal_duration);
                this.total = this.durationToString(response.data.total_duration);

                window.scrollTo(0, 0);

                this.loading = false;
            });
        },
        getReport() {
            let ordering = (this.orderDir == 'desc' ? '-' : '') + this.orderBy;
            if (this.orderBy != 'date') {
                ordering += ',-date';
            }
            const query = {
                ordering: ordering,
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
            let ordering = (this.orderDir == 'desc' ? '-' : '') + this.orderBy;
            if (this.orderBy != 'date') {
                ordering += ',-date';
            }
            const query = {
                ordering: ordering,
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
        moment(date) {
            return moment(date).format('LL');
        },
        refresh() {
            return this.getEntries();
        }
    },
    mounted() {
        return this.getEntries();
    },
    created() {
        this.bus.$on('search', () => {
            const params = {
                search: this.$route.query.search
            };
            const url = timestrapConfig.API_URLS.ENTRIES + '?' + $.param(params);
            this.getEntries(url);
        });
    },
    components: {
        Datepicker,
        Entry,
        Pager,
        Select2
    }
};
</script>


<style lang="scss">
.report-filters {
    label {
        font-weight: bold;
        font-size: .7em;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
}
</style>
