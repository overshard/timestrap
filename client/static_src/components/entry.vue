<template>
  <div
    :id="'entry-' + entry.id"
    class="entry row py-2 bg-light small">
    <div class="col-sm-3 client-project">
      <div class="small">
        <i class="fa fa-address-book text-muted mr-2"/>
        {{ entry.project_details.client_details.name }}
      </div>
      <i class="fa fa-briefcase text-muted mr-1"/>
      {{ entry.project_details.name }}
    </div>
    <div :class="['d-flex', 'flex-column', 'align-self-end', 'tasks', 'col-sm-6']">
      <div
        v-if="entry.task"
        class="small">
        <i class="fa fa-tasks text-muted mr-2"/>
        {{ entry.task_details.name }}
      </div>
      <div
        v-if="entry.note"
        class="entry-note">
        <i class="fa fa-comment text-muted mr-1"/>
        {{ entry.note }}
      </div>
    </div>
    <div class="col-sm-1 align-self-center display-4 duration">
      <i class="fa fa-clock-o text-muted mr-2"/>
      {{ durationString }}
    </div>
    <div class="col-sm-1 align-self-center datetimes flex-column">
      <div class="datetime-start small">
        <i class="fa fa-hourglass-start text-muted mr-1"/>
        {{ formatDateTime(entry.datetime_start) }}
      </div>
      <div class="datetime-end small">
        <i class="fa fa-hourglass-end text-muted mr-1"/>
        {{ formatDateTime(entry.datetime_end) }}
      </div>
    </div>
    <div
      v-if="editable"
      class="col-sm-2 d-flex align-self-center justify-content-end">
      <template v-if="this.$perms.change_entry || this.$perms.delete_entry">
        <button
          id="entry-menu"
          type="button"
          data-toggle="dropdown"
          class="btn btn-faded btn-sm btn-icon dropdown-toggle">
          <i class="fa fa-ellipsis-v"/>
        </button>
        <div class="dropdown-menu dropdown-menu-right">
          <a
            v-if="this.$perms.change_entry"
            id="entry-menu-change"
            class="dropdown-item"
            href="#"
            @click.prevent
            @click="toggleEditModal(entry)">
            Edit
          </a>
          <a
            v-if="this.$perms.delete_entry"
            id="entry-menu-delete"
            class="dropdown-item"
            href="#"
            @click.prevent
            @click="deleteEntry(index)">
            Delete
          </a>
        </div>
      </template>
    </div>
    <div
      v-else
      class="col-sm-2">
      <div class="small">
        <i class="fa fa-user-circle text-muted mr-2"/>
        {{ entry.user_details.username }}
      </div>
      <i class="fa fa-calendar-o text-muted mr-1"/>
      {{ $moment(entry.date).format('LL') }}
    </div>
  </div>
</template>


<script>
import {mapActions} from 'vuex';

import DurationFormatter from '../mixins/durationformatter';
import Select2 from './select2.vue';


export default {
  components: {
    Select2,
  },
  mixins: [
    DurationFormatter,
  ],
  props: [
    'entry',
    'index',
    'editable',
    'toggleEditModal',
  ],
  computed: {
    durationString() {
      return this.durationToString(this.entry.duration);
    },
  },
  methods: {
    ...mapActions({
      deleteEntry: 'entries/deleteEntry',
    }),
    formatDateTime(datetime) {
      if (datetime) return this.$moment(datetime).format('h:mm a');
      else return '-';
    },
  },
};
</script>


<style lang="scss">
#entry-rows {
  .row:not(.inset-row) {
    border-top: 1px solid #eceeef;

    &:first-child {
      border-top-right-radius: .25rem;
      border-top-left-radius: .25rem;
    }

    &:nth-of-type(2n+1) {
      background-color: #fbf3e5 !important;
    }

    &:last-child {
      border-bottom-right-radius: .25rem;
      border-bottom-left-radius: .25rem;
      border-bottom: 1px solid #eceeef;
    }

    // Fix for override of striping-row-color above
    &.bg-success {
      background-color: #28a745 !important;
    }
  }

  .duration {
    display: flex;
  }

  .datetimes {
    display: none;
  }

  .entry-note {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .entry:hover,
  .entry:focus {
    .duration {
      display: none;
    }

    .datetimes {
      display: flex;
    }

    .tasks .small {
      display: none;
    }

    .tasks {
      align-self: flex-start !important;

      .entry-note {
        overflow: show !important;
        white-space: normal !important;
      }
    }
  }

  .duration.display-4 {
    font-size: 1.5rem;
  }

  .note {
    line-height: 1.3;
    margin-bottom: 3px;
  }

  .username {
    overflow-x: hidden;
  }

  .fa-clock-o {
    line-height: 1.3em;
  }

  .client-project {
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .inset-row {
    margin-bottom: -.75rem;

    .display-4 {
      font-size: 2rem;
    }
  }
}
</style>
