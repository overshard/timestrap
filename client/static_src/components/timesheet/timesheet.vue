<template>
  <div class="container">
    <div class="row py-2 mb-4 bg-light rounded">
      <div class="col-12">
        <router-link
          to="/reports/"
          class="btn btn-primary btn-sm">
          <i
            class="fa fa-book"
            aria-hidden="true"/>
          Create Reports
        </router-link>

        <button
          class="btn btn-secondary btn-sm pull-right ml-2"
          @click.prevent
          @click="getEntries">
          <i
            class="fa fa-refresh"
            aria-hidden="true"/>
          Refresh
        </button>
      </div>
    </div>

    <entry-modal
      v-if="modal.show && (this.$perms.add_entry || this.$perms.change_entry)"
      id="entry-modal"
      :config="modal"
      @close="toggleModal"/>

    <chart :entries="entries"/>

    <div
      v-if="this.$perms.view_entry"
      id="entry-rows">
      <div
        v-for="(entryBlock, blockIndex) in entries"
        :index="blockIndex"
        :key="entryBlock.id"
        class="mb-4">
        <div class="row inset-row">
          <div class="col-12">
            <h2 class="display-4 text-muted">
              {{ $moment(entryBlock.date).format('MMMM Do') }}
            </h2>
          </div>
        </div>
        <div class="rounded">
          <template v-if="entryBlock.entries.length > 0">
            <entry
              v-for="(entry, entryIndex) in entryBlock.entries"
              :entry="entry"
              :index="entryIndex"
              :key="entry.id"
              :editable="editable"
              :toggle-edit-modal="toggleModal"
              @delete-entry="deleteEntry(blockIndex, entryIndex)"/>
          </template>
          <template v-else>
            <div class="entry row py-3 bg-light small">
              <div class="col">
                <strong>No entries</strong> for this day.
              </div>
            </div>
          </template>
        </div>
      </div>

      <div class="row bg-success text-white py-2 mb-4 rounded">
        <div class="ml-auto col-sm-2 text-right">
          <strong>Subtotal</strong>
        </div>
        <div class="col-sm-3">
          <i
            class="fa fa-clock-o mr-2"
            aria-hidden="true"/>
          <strong>{{ $moment.duration(total, 'hours').format('d[d] h[h] m[m]') }}</strong>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import {mapGetters, mapActions, mapState} from 'vuex';

import Datepicker from '../datepicker.vue';
import Entry from '../entry.vue';
import Pager from '../pager.vue';
import Select2 from '../select2.vue';
import EntryModal from './entry-modal.vue';
import Chart from './chart.vue';


export default {
  components: {
    Datepicker,
    Entry,
    Pager,
    Select2,
    EntryModal,
    Chart,
  },
  data() {
    return {
      editable: true,
      modal: {
        entry: null,
        show: false,
      },
    };
  },
  computed: {
    ...mapState({
      total: state => state.entries.total,
      subtotal: state => state.entries.subtotal,
    }),
    ...mapGetters({
      entries: 'entries/getEntriesByDay',
    }),
  },
  methods: {
    ...mapActions('entries', [
      'getEntries',
    ]),
    toggleModal(entry) {
      if (entry) this.modal.entry = entry;
      else this.modal.entry = null;
      this.modal.show = !this.modal.show;
    },
  },
};
</script>
