<template>
<div class="entry row py-2 bg-faded small">
    <template v-if="edit">
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
                <template v-if="global.perms.change_entry">
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
                        v-on:click.prevent
                        v-on:click="editEntry">
                            Edit
                        </a>
                        <a class="dropdown-item entry-menu-delete"
                        href="#"
                        v-on:click.prevent
                        v-on:click="deleteEntry">
                            Delete
                        </a>
                    </div>
                </template>
            </div>
        </template>
    </template>

    <template v-else>
        <div class="col-sm-3">
            <projects-select :selected="project_details.url" @project-select="projectSelect"></projects-select>
        </div>
        <div class="col-sm-5">
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
        <div class="col-sm-2">
            <button name="entry-save"
                    class="btn btn-success btn-sm w-100"
                    v-on:click="saveEntry">
                Save
            </button>
        </div>
    </template>
</div>
</template>


<script>
const ProjectsSelect = require('./projects-select.vue');

export default {
    props: ['entry', 'editable'],
    data() {
        return {
            edit: true,
            url: this.entry.url,
            user: this.entry.user,
            project: this.entry.project,
            project_details: this.entry.project_details,
            task: this.entry.task,
            task_details: this.entry.task_details,
            note: this.entry.note,
            duration: durationToString(this.entry.duration)
        };
    },
    methods: {
        editEntry() {
            this.edit = false;
        },
        saveEntry() {
            let body = {
                user: this.user,
                project: this.project,
                note: this.note,
                duration: this.duration
            };
            quickFetch(this.url, 'put', body).then((data) => {
                if (data.id) {
                    this.edit = true;
                    this.project_details = data.project_details;
                    this.task_details = data.task;
                }
            }).catch(error => console.log(error));
        },
        deleteEntry(e) {
            quickFetch(this.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    console.log('got em');
                }
            });
        },
        projectSelect(project) {
            this.project = project;
        },
    },
    components: {
        ProjectsSelect
    }
};
</script>
