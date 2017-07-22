<template>
<div class="entry row py-2 bg-faded small">
    <template v-if="edit && this.$perms.change_entry">
        <div class="col-sm-3">
            <select2 id="entry-project"
                     v-model="project"
                     v-bind:options="projects"
                     v-bind:selected="project"></select2>
        </div>
        <div v-bind:class="['col-sm-' + [this.$perms.change_entry ? '5' : '7']]">
            <input name="entry-note"
                   type="text"
                   class="form-control form-control-sm"
                   ref="note"
                   placeholder="Note"
                   v-model="note" />
        </div>
        <div class="col-sm-2">
            <input name="entry-duration"
                   type="text"
                   class="form-control form-control-sm text-right font-weight-bold"
                   ref="duration"
                   placeholder="0:00"
                   v-model="duration" />
        </div>
        <div class="col-sm-2" v-if="this.$perms.change_entry">
            <button name="entry-save"
                    class="btn btn-success btn-sm w-100"
                    v-block-during-fetch
                    v-on:click="saveEntry">
                Save
            </button>
        </div>
    </template>

    <template v-else>
        <div class="col-sm-3 client-project">
            <div class="text-muted small">
                {{ project_details.client_details.name }}
            </div>
            {{ project_details.name }}
        </div>
        <div v-bind:class="['d-flex', 'flex-column', 'align-self-end', 'tasks', 'col-sm-5']">
            <div class="text-muted small"
                 v-if="task">
                {{ task_details.name }}
            </div>
            {{ note }}
        </div>
        <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration">
            {{ duration }}
        </div>
        <div v-bind:class="[[editable ? 'hidden-xl-down' : 'col-sm-2'], 'd-flex', 'align-self-center', 'justify-content-end',]">
            <template v-if="invoiced">
                <i class="fa fa-check-square-o" aria-hidden="true"></i>
            </template>
            <template v-else>
                <i class="fa fa-square-o" aria-hidden="true"></i>
            </template>
        </div>
        <template v-if="editable">
            <div class="col-sm-2 d-flex align-self-center justify-content-end">
                <template v-if="this.$perms.change_entry || this.$perms.delete_entry">
                    <button name="entry-menu"
                            class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                            type="button"
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right"
                         aria-labelledby="entry-menu">
                        <a class="dropdown-item entry-menu-change"
                           href="#"
                           v-if="this.$perms.change_entry"
                           v-on:click.prevent
                           v-on:click="editEntry">
                            Edit
                        </a>
                        <a class="dropdown-item entry-menu-restart"
                           href="#"
                           v-if="this.$perms.change_entry"
                           v-on:click.prevent
                           v-on:click="restartEntry">
                            Restart
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
        </template>
    </template>
</div>
</template>


<script>
const DurationFormatter = require('../mixins/durationformatter');
const Select2 = require('./select2.vue');

export default {
    props: ['entry', 'editable'],
    mixins: [ DurationFormatter ],
    data() {
        return {
            edit: false,
            url: this.entry.url,
            user: this.entry.user,
            project: this.entry.project,
            project_details: this.entry.project_details,
            task: this.entry.task,
            task_details: this.entry.task_details,
            note: this.entry.note,
            invoiced: this.entry.is_invoiced,
            duration: this.durationToString(this.entry.duration),
            projects: {}
        };
    },
    methods: {
        editEntry() {
            this.$quickFetch(timestrapConfig.API_URLS.CLIENTS).then(data => {
                this.projects = data.map(function(client) {
                    let projects = client.projects.map(function(project) {
                        return { id: project.url, text: project.name };
                    });
                    return { text: client.name, children: projects };
                });
                this.edit = true;
            }).catch(error => console.log(error));
        },
        saveEntry(e) {
            let body = {
                user: this.user,
                project: this.project,
                note: this.note,
                duration: this.duration
            };
            this.$quickFetch(this.url, 'put', body).then(data => {
                if (data.id) {
                    this.edit = false;
                    this.project = data.project;
                    this.project_details = data.project_details;
                    this.task = data.task;
                    this.task_details = data.task_details;
                    this.duration = this.durationToString(data.duration);
                }
            }).catch(error => console.log(error));
        },
        deleteEntry() {
            this.$quickFetch(this.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    $.growl.notice({ message: 'Entry deleted!' });
                    this.$emit('delete-entry');
                }
                else {
                    $.growl.error({ message: 'Entry delete failed ):' });
                }
            }.bind(this));
        },
        restartEntry() {
            this.bus.$emit('timerToggle', this.entry);
        }
    },
    components: {
        Select2
    }
};
</script>
