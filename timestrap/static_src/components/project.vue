<template>
<div class="project row py-1 bg-light" v-if="!project.archive">
    <div v-bind:class="['col-sm-' + [this.$perms.change_project ? '4' : '6'], 'mb-1', 'project-name']">
        <i class="fa fa-briefcase text-muted mr-1" aria-hidden="true"></i>
        {{ project.name }}
    </div>
    <div class="col-sm-2 d-flex align-items-center">
        <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ project.total_duration }}</span>
    </div>
    <div class="col-sm-2 d-flex align-items-center">
        <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ project.total_entries }}</span>
    </div>
    <div class="col-sm-3 d-flex align-items-center" v-if="project.percent_done">
        <div class="progress w-100">
            <div v-if="project.percent_done"
                 v-bind:class="['progress-bar', [project.percent_done > 100 ? 'bg-danger' : '']]"
                 v-bind:style="{ width: project.percent_done + '%' }">
                {{ project.percent_done }}%
            </div>
        </div>
    </div>
    <div class="col-sm-3 d-flex align-items-center" v-else>
        No Estimate
    </div>
    <div class="col-sm-1 d-flex align-self-center justify-content-end">
        <template v-if="this.$perms.change_project || this.$perms.delete_project">
            <button name="project-menu"
                    class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                    type="button"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false">
                <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
            </button>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="project-menu">
                <a id="project-menu-change"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.change_project"
                   v-on:click.prevent
                   v-on:click="toggleEditModal(project, index, client_index)">Edit</a>
                <a id="project-menu-delete"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.delete_project"
                   v-on:click.prevent
                   v-on:click="deleteProject">Delete</a>
                <a id="project-menu-archive"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.change_project"
                   v-on:click.prevent
                   v-on:click="archiveProject">Archive</a>
            </div>
        </template>
    </div>
</div>
</template>

<script>
export default {
    props: ['project', 'index', 'client_index', 'key', 'toggleEditModal'],
    data() {
        return {
            estimate: this.project.estimate,
            name: this.project.name
        };
    },
    methods: {
        deleteProject() {
            this.$quickFetch(this.project.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    $.growl.notice({ message: 'Project deleted!' });
                    this.$emit('removeProject', this.client_index, this.index);
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
                    this.$emit('removeProject', this.client_index, this.index);
                }
            }).catch(error => console.log(error));
        }
    }
};
</script>
