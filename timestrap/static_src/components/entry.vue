<template>
<div class="entry row py-2 bg-faded small">
    <template v-if="edit && global.perms.change_entry">
        <div class="col-sm-3">
            <select2 id="entry-project"
                     v-model="project"
                     v-bind:options="projects"
                     v-bind:selected="project"
                     @select2-select="selectProjectOption"></select2>
        </div>
        <div v-bind:class="['col-sm-' + [global.perms.change_entry ? '5' : '7']]">
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
        <div class="col-sm-2" v-if="global.perms.change_entry">
            <button name="entry-save"
                    class="btn btn-success btn-sm w-100"
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
        <div v-bind:class="['d-flex', 'flex-column', 'align-self-end', 'tasks', [editable ? 'col-sm-5' : 'col-sm-7']]">
            <div class="text-muted small"
                 v-if="task">
                {{ task_details.name }}
            </div>
            {{ note }}
        </div>
        <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration">
            {{ duration }}
        </div>
        <template v-if="editable">
            <div class="col-sm-2 d-flex align-self-center justify-content-end">
                <template v-if="global.perms.change_entry || global.perms.delete_entry">
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
                           v-if="global.perms.change_entry"
                           v-on:click.prevent
                           v-on:click="editEntry">
                            Edit
                        </a>
                        <a class="dropdown-item restart"
                           href="#"
                           v-if="global.perms.change_entry"
                           v-on:click.prevent
                           v-on:click="restartEntry">
                            Restart
                        </a>
                        <a class="dropdown-item entry-menu-delete"
                           href="#"
                           v-if="global.perms.delete_entry"
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
const Select2 = require('./select2.vue');

export default {
    props: ['entry', 'editable'],
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
            duration: durationToString(this.entry.duration),
            projects: {}
        };
    },
    methods: {
        editEntry() {
            quickFetch(timestrapConfig.API_URLS.CLIENTS).then(data => {
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
            toggleButtonBusy(e.target);
            let body = {
                user: this.user,
                project: this.project,
                note: this.note,
                duration: this.duration
            };
            console.log(this.duration);
            quickFetch(this.url, 'put', body).then(data => {
                if (data.id) {
                    this.edit = false;
                    this.project = data.project;
                    this.project_details = data.project_details;
                    this.task = data.task;
                    this.task_details = data.task_details;
                    this.duration = durationToString(data.duration);
                }
                toggleButtonBusy(e.target);
            }).catch(error => console.log(error));
        },
        deleteEntry() {
            quickFetch(this.url, 'delete').then(function(response) {
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
            this.bus.$emit('timerToggle', stringToDuration(this.duration));
        },
        selectProjectOption(project) {
            this.project = project;
        }
    },
    components: {
        Select2
    }
};
</script>
