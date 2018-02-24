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

    <div class="row chartjs-wrapper bg-light rounded my-4 pt-4 pb-2">
        <canvas id="chartjs-1" class="chartjs"></canvas>
    </div>

    <div v-if="this.$perms.view_entry" id="entry-rows">
        <div class="mb-4" v-for="(entryBlock, blockIndex) in entries">
            <div class="row inset-row">
                <div class="col-12">
                    <h2 class="display-4 text-muted">
                        {{ moment(entryBlock.date) }}
                    </h2>
                </div>
            </div>
            <div class="rounded">
                <entry v-for="(entry, entryIndex) in entryBlock.entries"
                       v-on:delete-entry="deleteEntry(blockIndex, entryIndex)"
                       v-bind:entry="entry"
                       v-bind:index="entryIndex"
                       v-bind:key="entry.id"
                       v-bind:editable="editable"
                       v-bind:toggleEditModal="toggleModal"></entry>
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
const Datepicker = require('./datepicker.vue');
const DurationFormatter = require('../mixins/durationformatter');
const Entry = require('./entry.vue');
const Pager = require('./pager.vue');
const Select2 = require('./select2.vue');
const EntryModal = require('./entry-modal.vue');

export default {
    mixins: [
        DurationFormatter,
    ],
    data() {
        return {
            entries: null,

            subtotal: null,
            total: null,

            next: null,
            previous: null,

            editable: true,
            modal_config: {
                index: null,
                entry: null,
                show: false,
            },
            renderedChart: false,
        };
    },
    methods: {
        getEntries(url) {
            let userEntries = timestrapConfig.API_URLS.ENTRIES + '?user=' + timestrapConfig.USER.ID;
            url = (typeof url !== 'undefined') ? url : userEntries;

            let entriesFetch = this.$quickFetch(url);

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

                this.subtotal = this.durationToString(data.subtotal_duration);
                this.total = this.durationToString(data.total_duration);

                let chartDates = [];
                let chartDurations = [];
                let entryBlock;
                for (entryBlock in this.entries) {
                    chartDates.push(this.moment(this.entries[entryBlock].date));
                    let entry;
                    let totalTime = 0;
                    for (entry in this.entries[entryBlock].entries) {
                        totalTime = totalTime + this.entries[entryBlock].entries[entry].duration;
                    }
                    totalTime = Math.round(totalTime * 10) / 10;
                    chartDurations.push(totalTime);
                }

                if (this.renderedChart) this.renderedChart.destroy();
                this.renderedChart = new Chart(document.getElementById('chartjs-1'), {
                    type: 'bar',
                    data: {
                        labels: chartDates,
                        datasets: [{
                            backgroundColor: '#17a2b8',
                            data: chartDurations
                        }]
                    },
                    options: {
                        maintainAspectRatio: false,
                        legend: {
                            display: false
                        },
                        scales: {
                            yAxes: [{
                                ticks: { beginAtZero: true }
                            }]
                        }
                    }
                });

                window.scrollTo(0, 0);
            });
        },
        deleteEntry(blockIndex, entryIndex) {
            this.refresh();
        },
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
        },
        refresh() {
            this.getEntries();
        }
    },
    mounted() {
        this.getEntries();
    },
    created() {
        this.bus.$on('refreshEntries', function() {
            this.refresh();
        }.bind(this));
    },
    destroyed() {
        this.renderedChart.destroy();
    },
    components: {
        Datepicker,
        Entry,
        Pager,
        Select2,
        EntryModal
    }
};
</script>
