<template>
<div class="entry row py-2 bg-light small">
    <div class="col-sm-3 client-project">
        <div class="small">
            <i class="fa fa-address-book text-muted mr-2" aria-hidden="true"></i>
            {{ project_details.client_details.name }}
        </div>
        <i class="fa fa-briefcase text-muted mr-1" aria-hidden="true"></i>
        {{ project_details.name }}
    </div>
    <div v-bind:class="['d-flex', 'flex-column', 'align-self-end', 'tasks', 'col-sm-6']">
        <div class="small" v-if="task">
            <i class="fa fa-tasks text-muted mr-2" aria-hidden="true"></i>
            {{ task_details.name }}
        </div>
        <div class="entry-note" v-if="note">
            <i class="fa fa-comment text-muted mr-1" aria-hidden="true"></i>
            {{ note }}
        </div>
    </div>
    <div class="col-sm-1 align-self-center display-4 duration">
        <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
        {{ durationString }}
    </div>
    <div class="col-sm-1 align-self-center datetimes flex-column">
        <div class="datetime-start small">
            <i class="fa fa-hourglass-start text-muted mr-1" aria-hidden="true"></i>
            {{ formatDateTime(datetime_start) }}
        </div>
        <div class="datetime-end small">
            <i class="fa fa-hourglass-end text-muted mr-1" aria-hidden="true"></i>
            {{ formatDateTime(datetime_end) }}
        </div>
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end"
         v-if="editable">
        <template v-if="this.$perms.change_entry || this.$perms.delete_entry">
            <button name="entry-menu"
                    type="button"
                    data-toggle="dropdown"
                    class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                    aria-haspopup="true"
                    aria-expanded="false">
                <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
            </button>
            <div class="dropdown-menu dropdown-menu-right"
                    aria-labelledby="entry-menu">
                <a id="entry-menu-change"
                    class="dropdown-item"
                    href="#"
                    v-if="this.$perms.change_entry"
                    v-on:click.prevent
                    v-on:click="toggleEditModal(entry)">
                    Edit
                </a>
                <a class="dropdown-item entry-menu-delete"
                    href="#"
                    v-if="this.$perms.delete_entry"
                    v-on:click.prevent
                    v-on:click="deleteEntry(index)">
                    Delete
                </a>
            </div>
        </template>
    </div>
    <div class="col-sm-2" v-else>
        <div class="small">
            <i class="fa fa-user-circle text-muted mr-2" aria-hidden="true"></i>
            {{ user_details.username }}
        </div>
        <i class="fa fa-calendar-o text-muted mr-1" aria-hidden="true"></i>
        {{ dateFormatted }}
    </div>
</div>
</template>


<script>
import {mapActions} from 'vuex';

import DurationFormatter from '../mixins/durationformatter';
import Select2 from './select2.vue';


export default {
    props: [
        'entry',
        'index',
        'editable',
        'toggleEditModal',
    ],
    mixins: [
        DurationFormatter,
    ],
    data() {
        return {
            url: this.entry.url,
            user: this.entry.user,
            user_details: this.entry.user_details,
            project: this.entry.project,
            project_details: this.entry.project_details,
            task: this.entry.task,
            task_details: this.entry.task_details,
            note: this.entry.note,
            duration: this.entry.duration,
            datetime_start: this.entry.datetime_start,
            datetime_end: this.entry.datetime_end,
            date: this.entry.date,
        };
    },
    computed: {
        durationString() {
            return this.durationToString(this.entry.duration);
        },
        dateFormatted() {
            return moment(this.date).format('LL');
        },
    },
    methods: {
        ...mapActions({
            deleteEntry: 'entries/deleteEntry',
        }),
        formatDateTime(datetime) {
            if (datetime) return moment(datetime).format('h:mm a');
            else return '-';
        }
    },
    components: {
        Select2,
    }
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
