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
        {{ duration }}
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
                    v-on:click="toggleEditModal(entry, index)">
                    Edit
                </a>
                <a class="dropdown-item entry-menu-delete"
                    href="#"
                    v-if="this.$perms.delete_entry"
                    v-on:click.prevent
                    v-on:click="deleteEntry">
                    Delete
                </a>
            </div>
        </template>
    </div>
    <div class="col-sm-2 d-flex align-items-center justify-content-start"
         v-else>
         <i class="fa fa-user-circle text-muted mr-2" aria-hidden="true"></i>
         {{ user_details.username }}
    </div>
</div>
</template>


<script>
const DurationFormatter = require('../mixins/durationformatter');
const Select2 = require('./select2.vue');

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
            duration: this.durationToString(this.entry.duration),
            datetime_start: this.entry.datetime_start,
            datetime_end: this.entry.datetime_end,
        };
    },
    methods: {
        deleteEntry() {
            this.$quickFetch(this.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    $.growl.notice({ message: 'Entry deleted!' });
                    this.$emit('delete-entry');
                } else {
                    $.growl.error({ message: 'Entry delete failed.' });
                }
            }.bind(this));
        },
        formatDateTime(datetime) {
            if (datetime) {
                return moment(datetime).format('h:mm a');
            } else {
                return '-';
            }
        }
    },
    components: {
        Select2,
    }
};
</script>
