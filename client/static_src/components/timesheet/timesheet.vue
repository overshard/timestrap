<template>
<div
  v-if="$perms.view_entry"
  class="container-fluid">
  <entry-modal
    v-if="modalShow"
    :entry="modalEntry"
    @close="modalShow = false"/>

  <chart :entries="entries"/>

  <div id="entry-rows">
    <div
      v-for="(entryBlock, blockIndex) in entries"
      :index="blockIndex"
      :key="entryBlock.id">
      <div class="row inset-row">
        <div class="col-6">
          <h2 class="display-4">
            {{ $moment(entryBlock.date).format('ddd[,] MMMM Do') }}
          </h2>
        </div>
        <div class="col-6 d-flex align-items-center justify-content-end h4 mb-0">
          <span class="badge badge-success mb-0">
            {{ $moment.duration(entryBlock.duration, 'hours').format('h[h] m[m]') }}
          </span>
        </div>
      </div>
      <div>
        <template v-if="entryBlock.entries.length > 0">
          <entry
            v-for="(entry, entryIndex) in entryBlock.entries"
            :entry="entry"
            :index="entryIndex"
            :key="entry.id"
            :editable="editable"
            @modal="modalToggle(entry)"
            @delete-entry="deleteEntry(entry)"/>
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

    <div class="row bg-success text-white py-2">
      <div class="ml-auto col-sm-2 text-right">
        Subtotal<br>
        <strong>Total</strong>
      </div>
      <div class="col-sm-4">
        <icon
          :icon="['fas', 'clock']"
          class="mr-1"/>
        {{ $moment.duration(subtotal, 'hours').format('d[d] h[h] m[m]') }}<br>
        <icon
          :icon="['fas', 'clock']"
          class="mr-1"/>
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
import EntryModal from './entry-modal.vue';
import Chart from './chart.vue';


export default {
  components: {
    Datepicker,
    Entry,
    EntryModal,
    Chart,
  },
  data() {
    return {
      editable: true,
      modalEntry: null,
      modalShow: false,
    };
  },
  computed: {
    ...mapState({
      total: state => state.entries.total,
    }),
    ...mapGetters({
      entries: 'entries/getEntriesByDay',
      subtotal: 'entries/getEntriesByDayTotal',
    }),
  },
  methods: {
    ...mapActions('entries', [
      'fetchEntries',
    ]),
    modalToggle: function(entry) {
      if (typeof(entry) !== 'undefined') this.modalEntry = entry;
      else this.modalEntry = null;
      this.modalShow = !this.modalShow;
    },
  },
};
</script>
