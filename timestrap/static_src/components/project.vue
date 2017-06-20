<template>
<div class="project row py-1 bg-faded" v-if="!project.archive">

    <template v-if="edit && this.$perms.change_project">
    <div class="col-8">
        <input name="project-name"
               type="text"
               class="form-control form-control-sm"
               v-model.trim="name"
               v-on:keyup.enter="saveProject"
               required />
    </div>
    <div class="col-2">
        <input name="project-estimate"
               type="text"
               class="form-control form-control-sm"
               placeholder="Estimate"
               v-model.number="estimate"
               v-on:keyup.enter="saveProject"
               required />
    </div>
    <div class="col-2">
        <button name="project-save"
                class="btn btn-success btn-sm w-100"
                v-block-during-fetch
                v-on:click="saveProject">
            Save
        </button>
    </div>
    </template>

    <template v-else>
    <div v-bind:class="['col-' + [this.$perms.change_project ? '4' : '6'], 'mb-1', 'project-name']">
        {{ project.name }}
    </div>
    <div class="col-2 d-flex align-items-center">
        <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ project.total_duration }}</span>
    </div>
    <div class="col-2 d-flex align-items-center">
        <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ project.total_entries }}</span>
    </div>
    <div class="col-2 d-flex align-items-center" v-if="project.percent_done">
        <div class="progress w-100">
            <div v-if="project.percent_done"
                 v-bind:class="['progress-bar', [project.percent_done > 100 ? 'bg-danger' : '']]"
                 v-bind:style="{ width: project.percent_done + '%' }">
                {{ project.percent_done }}%
            </div>
        </div>
    </div>
    <div class="col-2 d-flex align-items-center" v-else>
        No Estimate
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end">
        <template v-if="this.$perms.change_project || this.$perms.delete_project">
            <button name="project-menu"
                    class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                    type="button"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false">
                <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
            </button>
            <div class="dropdown-menu dropdown-menu-right"
                    aria-labelledby="project-menu">
                <a id="project-menu-change"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.change_project"
                   v-on:click.prevent
                   v-on:click="editProject">
                    Edit
                </a>
                <a id="project-menu-delete"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.delete_project"
                   v-on:click.prevent
                   v-on:click="deleteProject">
                    Delete
                </a>
                <a id="project-menu-archive"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.change_project"
                   v-on:click.prevent
                   v-on:click="archiveProject">
                    Archive
                </a>
            </div>
        </template>
    </div>
    </template>
</div>
</template>

<script>
export default {
    props: ['project'],
    data() {
        return {
            edit: false,
            estimate: this.project.estimate,
            name: this.project.name
        };
    },
    methods: {
        editProject() {
            this.edit = true;
        },
        saveProject(e) {
            let body = {
                client: this.project.client,
                estimate: this.estimate,
                name: this.name
            };
            this.$quickFetch(this.project.url, 'put', body).then(data => {
                if (data.id) {
                    this.project.name = data.name;
                    this.project.estimate = data.estimate;
                    this.project.percent_done = data.percent_done;
                    this.edit = false;
                }
            }).catch(error => console.log(error));
        },
        deleteProject() {
            this.$quickFetch(this.project.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    $.growl.notice({ message: 'Project deleted!' });
                    this.$emit('delete-project');
                } else {
                    $.growl.error({ message: 'Project delete failed ):' });
                }
            }.bind(this));
        },
        archiveProject() {
            const body = {
                name: this.project.name,
                client: this.project.client,
                archive: true
            };
            this.$quickFetch(this.project.url, 'put', body).then(data => {
                if (data.id) {
                    $.growl.notice({ message: 'Project archived!' });
                    this.$emit('project-client');
                }
            }).catch(error => console.log(error));
        }
    }
};
</script>
