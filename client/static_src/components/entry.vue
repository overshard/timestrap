<template>
  <div
    :id="'entry-' + entry.id"
    class="entry row py-2 bg-light small">
    <div class="col-sm-3 client-project">
      <div class="small">
        <icon
          :icon="['fas', 'address-book']"
          class="mr-2 text-muted"/>
        {{ entry.project_details.client_details.name }}
      </div>
      <icon
        :icon="['fas', 'briefcase']"
        class="mr-1 text-muted"/>
      {{ entry.project_details.name }}
    </div>
    <div :class="['d-flex', 'flex-column', 'align-self-end', 'tasks', 'col-sm-5']">
      <div
        v-if="entry.task"
        class="small">
        <icon
          :icon="['fas', 'tasks']"
          class="mr-2 text-muted"/>
        {{ entry.task_details.name }}
      </div>
      <div
        v-if="entry.note"
        class="entry-note">
        <icon
          :icon="['fas', 'comment']"
          class="mr-1 text-muted"/>
        {{ entry.note }}
      </div>
    </div>
    <div class="col-sm-2 align-items-center display-4 duration">
      <icon
        :icon="['fas', 'clock']"
        class="mr-2 text-muted small mb-1"/>
      {{ $moment.duration(entry.duration, 'hours').format('h:mm', {trim: false}) }}
    </div>
    <div class="col-sm-2 align-self-center datetimes flex-column">
      <div class="datetime-start small">
        <icon
          :icon="['fas', 'hourglass-start']"
          class="mr-1 text-muted"/>
        {{ formatDateTime(entry.datetime_start) }}
      </div>
      <div class="datetime-end small">
        <icon
          :icon="['fas', 'hourglass-end']"
          class="mr-1 text-muted"/>
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
          <icon
            :icon="['fas', 'ellipsis-v']"/>
        </button>
        <div class="dropdown-menu dropdown-menu-right">
          <a
            v-if="this.$perms.change_entry"
            id="entry-menu-change"
            class="dropdown-item"
            href="#"
            @click.prevent="$emit('modal')">
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
        <icon
          :icon="['fas', 'user-circle']"
          class="mr-2 text-muted"/>
        {{ entry.user_details.username }}
      </div>
      <icon
        :icon="['fas', 'calendar']"
        class="mr-1 text-muted"/>
      {{ $moment(entry.date).format('LL') }}
    </div>
  </div>
</template>


<script>
import {mapActions} from 'vuex';

import Select2 from './select2.vue';


export default {
  components: {
    Select2,
  },
  props: [
    'entry',
    'index',
    'editable',
    'toggleEditModal',
  ],
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
    font-weight: lighter;
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
    font-size: 1.7rem;
  }

  .note {
    line-height: 1.3;
    margin-bottom: 3px;
  }

  .username {
    overflow-x: hidden;
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
