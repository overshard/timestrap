<template>
<div class="container-fluid">
  <div class="row row-background">
    <div class="col-md-7">
      <h1 class="row-title">
        <icon :icon="['fas', 'book']" class="fa-sm mr-2"/>
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
          <span  v-bind:class="{active: isFiltered}">
            <icon :icon="['fas', 'filter']" class="mr-1"/>
            Filter
          </span>
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
                  :selected="user"
                  placeholder="User"
                  allowclear/>
              </div>
              <div class="form-group">
                <label>Client</label>
                <selector
                  id="report-filter-client"
                  v-model="client"
                  :options="clients"
                  :selected="client"
                  placeholder="Client"
                  allowclear/>
              </div>
              <div class="form-group mb-0">
                <label>Project</label>
                <selector
                  id="report-filter-project"
                  v-model="project"
                  :options="projects"
                  :selected="project"
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
                  :selected="task"
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

            <div class="clear col-sm-12">
              <button
                class="btn btn-info w-100 clear"
                @click.prevent.exact="clear">
                clear
              </button>
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
    <div class="row">
      <table class="table table-striped table-responsive-md table-sm small">
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
            :key="entry.id"
            :id="'entry-' + entry.id">
            <td>{{ entry.project ? getClient(getProject(entry.project).client).name : '' }}</td>
            <td>{{ entry.project ? getProject(entry.project).name : '' }}</td>
            <td>{{ entry.task ? getTask(entry.task).name : '' }}</td>
            <td>{{ entry.user ? getUser(entry.user).username : '' }}</td>
            <td>{{ $moment(entry.date).format('LL') }}</td>
            <td class="text-right">{{ $moment.duration(entry.duration, 'hours').format('h[h] mm[m]') }}</td>
            <td class="entry__note">{{ entry.note }}</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td>
              <small class="text-muted text-uppercase">Count</small>
              {{ entries.length }}
            </td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td class="text-right text-nowrap">
              <small class="text-muted text-uppercase">Sum</small>
              {{ $moment.duration(total, 'hours').format('d[d] h[h] m[m]') }}
            </td>
            <td></td>
          </tr>
        </tfoot>
      </table>
    </div>
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
      client: this.$store.state.reports.client,
      project: this.$store.state.reports.project,
      task: this.$store.state.reports.task,
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
      this.setProject(this.project);
      this.$store.dispatch('reports/getReport');
    },
    task() {
      this.setTask(this.task);
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
      projects: 'projects/getSelectProjects',
      clients: 'clients/getSelectClients',
      users: 'users/getSelectUsers',
      getTask: 'tasks/getTask',
      getProject: 'projects/getProject',
      getClient: 'clients/getClient',
      getUser: 'users/getUser',
      isFiltered: 'reports/isFiltered'
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
    clear(){
      this.minDate = null;
      this.maxDate = null;
      this.user = null;
      this.client = null;
      this.project = null;
      this.task = null;
    },
    exportReport() {
      let ordering = (this.orderDir === 'desc' ? '-' : '') + this.orderBy;
      if (this.orderBy !== 'date') {
        ordering += ',-date';
      }

      function urlToId(url) {
        if (url !== null) {
          let splitUrl = url.split('/');
          return splitUrl[splitUrl.length - 2];
        } else {
          return "";
        }
      }

      const query = {
        ordering: ordering,
        user: urlToId(this.user),
        project: urlToId(this.project),
        project__client: urlToId(this.client),
        task: urlToId(this.task),
        min_date: this.minDate,
        max_date: this.maxDate,
        export_format: this.exportFormat,
      };
      document.location.href = timestrapConfig.CORE_URLS.REPORTS_EXPORT + '?' + $.param(query);
    },
  },
};
</script>


<style lang="scss" scoped>
.row-background {
  background-image: url('/static/imgs/background.jpg');
  background-size: cover;
  background-position: center center;
  padding-top: 3rem;
  padding-bottom: 3rem;
}

.row-title {
  margin-bottom: 0;
  color: #fff;
  text-shadow: 1px 1px 0 #000;
  font-weight: bold;

  .fa-sm {
    filter: drop-shadow(1px 1px 0 #000);
  }
}

.entry__note {
  max-width: 20vw;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.clear{
  margin-top: .5rem;
}

.active{
  /*svg{*/
  /*  color: green;*/
  /*}*/
  font-weight: bold;
}

</style>
