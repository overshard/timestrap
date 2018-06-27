<template>
<div class="container">
    <div class="row py-2 mb-4 bg-light rounded">
        <div class="col-12">
            <router-link to="/reports/" class="btn btn-primary btn-sm">
                <i class="fa fa-book" aria-hidden="true"></i>
                Create Reports
            </router-link>

            <button class="btn btn-secondary btn-sm pull-right ml-2"
                    v-block-during-fetch
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

    <entry-modal id="entry-modal"
                 v-if="modal_config.show && (this.$perms.add_entry || this.$perms.change_entry)"
                 @close="toggleModal"
                 @refresh="refresh"
                 v-bind:config="modal_config"></entry-modal>

    <chart v-bind:entries="entries"></chart>

    <div v-if="this.$perms.view_entry" id="entry-rows">
        <div class="mb-4"
             v-for="(entryBlock, blockIndex) in entries"
             v-bind:item="entryBlock"
             v-bind:index="blockIndex"
             v-bind:key="entryBlock.id">
            <div class="row inset-row">
                <div class="col-12">
                    <h2 class="display-4 text-muted">
                        {{ moment(entryBlock.date) }}
                    </h2>
                </div>
            </div>
            <div class="rounded">
                <template v-if="entryBlock.entries.length > 0">
                <entry v-for="(entry, entryIndex) in entryBlock.entries"
                       v-on:delete-entry="deleteEntry(blockIndex, entryIndex)"
                       v-bind:entry="entry"
                       v-bind:index="entryIndex"
                       v-bind:key="entry.id"
                       v-bind:editable="editable"
                       v-bind:toggleEditModal="toggleModal"></entry>
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
                Subtotal
                <br>
                <strong>Total</strong>
            </div>
            <div class="col-sm-3">
                <i class="fa fa-clock-o mr-2" aria-hidden="true"></i>
                {{ subtotal }}
                <br>
                <i class="fa fa-clock-o mr-2" aria-hidden="true"></i>
                <strong>{{ total }}</strong>
            </div>
        </div>
    </div>

    <div class="row py-2 mb-4 bg-light rounded">
        <div class="col-12">
            <button class="btn btn-secondary btn-sm pull-right ml-2"
                    v-block-during-fetch
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
import {mapGetters, mapActions, mapState} from 'vuex';

import Datepicker from '../datepicker.vue';
import DurationFormatter from '../../mixins/durationformatter';
import Entry from '../entry.vue';
import Pager from '../pager.vue';
import Select2 from '../select2.vue';
import EntryModal from './entry-modal.vue';
import Chart from './chart.vue';


export default {
    mixins: [
        DurationFormatter,
    ],
    data() {
        return {
            next: null,
            previous: null,

            editable: true,
            modal_config: {
                index: null,
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
        toggleModal(entry, index) {
            if (entry && (index || index === 0)) {
                this.modal_config.entry = entry;
                this.modal_config.index = index;
            } else {
                this.modal_config.entry = null;
                this.modal_config.index = null;
            }
            this.modal_config.show = !this.modal_config.show;
        },
        moment(date) {
            return moment(date).format('MMMM Do');
        }
    },
    components: {
        Datepicker,
        Entry,
        Pager,
        Select2,
        EntryModal,
        Chart,
    }
};
</script>
