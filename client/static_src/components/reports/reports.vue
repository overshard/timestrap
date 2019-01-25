<template>
<div class="container-fluid px-4">
  <div class="row mb-4">
    <div class="col-md-7">
      <h1 class="mb-0 font-weight-bold">
        <icon :icon="['fas', 'book']" class="text-muted mr-2"/>
        Reports
      </h1>
    </div>
    <div class="col-md-5 d-flex align-items-center justify-content-end">
      <template v-if="is_staff">
        <select
          v-model="exportFormat"
          class="export-select custom-select form-control-sm w-25 flex-fill mr-2">
          <option value="csv">csv</option>
          <option value="xls">xls</option>
          <option value="tsv">tsv</option>
          <option value="ods">ods</option>
          <option value="json">json</option>
          <option value="yaml">yaml</option>
          <option value="html">html</option>
        </select>
        <button
          id="export-report"
          class="btn btn-light flex-fill text-nowrap mr-2"
          @click="exportReport">
          <icon :icon="['fas', 'download']" class="mr-1"/>
          Export
        </button>
      </template>

      <popover class="flex-fill mr-2">
        <template slot="popover-button">
          <icon :icon="['fas', 'filter']" class="mr-1"/>
          Filter
        </template>
        <template slot="popover-content">
          <small class="text-muted mb-2 d-block">Filter by column, multiple filters are okay</small>
          <div class="row">
            <div class="col-sm-6">
              <div class="form-group">
                <label>User</label>
                <selector
                  id="report-filter-user"
                  v-model="user"
                  :options="users"
                  placeholder="User"
                  allowclear/>
              </div>
              <div class="form-group">
                <label>Client</label>
                <selector
                  id="report-filter-client"
                  v-model="client"
                  :options="clients"
                  placeholder="Client"
                  allowclear/>
              </div>
              <div class="form-group mb-0">
                <label>Project</label>
                <selector
                  id="report-filter-project"
                  v-model="project"
                  :options="projects"
                  placeholder="Project"
                  allowclear/>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group">
                <label>Task</label>
                <selector
                  id="report-filter-task"
                  v-model="task"
                  :options="tasks"
                  placeholder="Task"
                  allowclear/>
              </div>
              <div class="form-group">
                <label>Min. Date</label>
                <datepicker
                  id="report-filter-min-date"
                  v-model="minDate"
                  type="text"
                  class="form-control date-input"
                  placeholder="Min. date"
                  allowclear/>
              </div>
              <div class="form-group mb-0">
                <label>Max. Date</label>
                <datepicker
                  id="report-filter-max-date"
                  v-model="maxDate"
                  type="text"
                  class="form-control date-input"
                  placeholder="Max. date"
                  allowclear/>
              </div>
            </div>
          </div>
        </template>
      </popover>

      <popover class="flex-fill">
        <template slot="popover-button">
          <icon :icon="['fas', 'sort']" class="mr-1"/>
          Sort
        </template>
        <template slot="popover-content">
          <small class="text-muted mb-2 d-block">Sort by column and direction</small>
          <div class="row">
            <div class="col-md-6">
              <selector
                id="report-sort-by"
                v-model="orderBy"
                :options="orderByOptions"
                selected="date"
                placeholder="Order by"/>
            </div>
            <div class="col-md-6">
              <selector
                id="report-order-dir"
                v-model="orderDir"
                :options="orderDirOptions"
                selected="desc"
                placeholder="Order direction"/>
            </div>
          </div>
        </template>
      </popover>
    </div>
  </div>

  <template v-if="entries.length">
    <table v-if="this.$perms.view_entry" class="table table-striped table-responsive-md">
      <thead class="thead-dark">
        <tr>
          <th scope="col">
            <icon :icon="['fas', 'address-book']" class="mr-1"/>
            Client
          </th>
          <th scope="col">
            <icon :icon="['fas', 'briefcase']" class="mr-1"/>
            Project
          </th>
          <th scope="col">
            <icon :icon="['fas', 'tasks']" class="mr-1"/>
            Task
          </th>
          <th scope="col">
            <icon :icon="['fas', 'user-circle']" class="mr-1"/>
            User
          </th>
          <th scope="col">
            <icon :icon="['fas', 'calendar']" class="mr-1"/>
            Date
          </th>
          <th scope="col">
            <icon :icon="['fas', 'clock']" class="mr-1"/>
            Duration
          </th>
          <th scope="col">
            <icon :icon="['fas', 'comment']" class="mr-1"/>
            Note
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="entry in entries"
          :key="entry.id">
          <td>{{ entry.project_details.client_details.name }}</td>
          <td>{{ entry.project_details.name }}</td>
          <td>{{ entry.task ? entry.task_details.name : '' }}</td>
          <td>{{ entry.user_details.username }}</td>
          <td>{{ $moment(entry.date).format('LL') }}</td>
          <td class="text-right">{{ $moment.duration(entry.duration, 'hours').format('h[h] mm[m]') }}</td>
          <td class="entry__note">{{ entry.note }}</td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td class="text-right">
            <small class="text-muted text-uppercase">Count</small>
            {{ entries.length }}
          </td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td class="text-right">
            <small class="text-muted text-uppercase">Sum</small>
            {{ $moment.duration(total, 'hours').format('d[d] h[h] m[m]') }}
          </td>
          <td></td>
        </tr>
      </tfoot>
    </table>
  </template>
  <div v-else class="container">
    <div class="row">
      <div class="col text-center py-4">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</div>
</template>


<script>
import {mapGetters, mapState, mapActions, mapMutations} from 'vuex';
import $ from 'jquery';

import Datepicker from '../datepicker.vue';
import Popover from '../popover.vue';
import Entry from '../entry.vue';
import Selector from '../selector.vue';

import fetch from '../../fetch';


export default {
  components: {
    Datepicker,
    Popover,
    Entry,
    Selector,
  },
  data() {
    return {
      is_staff: timestrapConfig.USER.IS_STAFF,
      editable: false,
      next: null,
      previous: null,

      exportFormat: 'csv',

      orderByOptions: [
        {id: 'project__client__name', text: 'Client'},
        {id: 'date', text: 'Date'},
        {id: 'project__name', text: 'Project'},
        {id: 'task__name', text: 'Task'},
        {id: 'user__username', text: 'User'},
      ],
      orderDirOptions: [
        {id: 'asc', text: 'Ascending'},
        {id: 'desc', text: 'Descending'},
      ],

      orderBy: 'date',
      orderDir: 'desc',

      minDate: null,
      maxDate: null,
      user: null,
      client: null,
      project: null,
      task: null,
    };
  },
  watch: {
    orderBy() {
      this.setOrderBy(this.orderBy);
      this.$store.dispatch('reports/getReport');
    },
    orderDir() {
      this.setOrderDir(this.orderDir);
      this.$store.dispatch('reports/getReport');
    },
    user() {
      this.setUser(this.user);
      this.$store.dispatch('reports/getReport');
    },
    client() {
      this.setClient(this.client);
      this.$store.dispatch('reports/getReport');
    },
    project() {
      this.setClient(this.project);
      this.$store.dispatch('reports/getReport');
    },
    task() {
      this.setClient(this.task);
      this.$store.dispatch('reports/getReport');
    },
    minDate() {
      this.setMinDate(this.minDate);
      this.$store.dispatch('reports/getReport');
    },
    maxDate() {
      this.setMaxDate(this.maxDate);
      this.$store.dispatch('reports/getReport');
    },
  },
  computed: {
    ...mapState({
      entries: state => state.reports.all,
      total: state => state.reports.total,
      subtotal: state => state.reports.subtotal,
    }),
    ...mapGetters({
      tasks: 'tasks/getSelectTasks',
      projects: 'clients/getSelectProjects',
      clients: 'clients/getSelectClients',
      users: 'users/getSelectUsers',
    }),
  },
  mounted() {
    this.$store.dispatch('reports/getReport');
  },
  methods: {
    ...mapMutations('reports', [
      'setOrderBy',
      'setOrderDir',

      'setUser',
      'setClient',
      'setProject',
      'setTask',
      'setMinDate',
      'setMaxDate',
    ]),
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
        min_date: this.minDate,
        max_date: this.maxDate,
        task: this.task,
        exportFormat: this.exportFormat,
      };
      document.location.href = timestrapConfig.CORE_URLS.REPORTS_EXPORT + '?' + $.param(query);
    },
  },
};
</script>


<style lang="scss">
.entry__note {
  max-width: 20vw;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
