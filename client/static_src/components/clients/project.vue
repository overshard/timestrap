<template>
<div class="project row py-1 bg-light" v-if="!project.archive">
    <div v-bind:class="['col-sm-4', 'mb-1', 'project-name']">
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
    <div class="col-sm-3 d-flex align-items-center" v-if="project.percent_done !== null">
        <div class="progress w-100">
            <div v-bind:class="['progress-bar', [project.percent_done > 100 ? 'bg-danger' : '']]"
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
                   v-on:click="toggleProjectModal(project)">Edit</a>
                <a id="project-menu-delete"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.delete_project"
                   v-on:click.prevent
                   v-on:click="deleteProject(index)">Delete</a>
                <!-- <a id="project-menu-archive"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.change_project"
                   v-on:click.prevent
                   v-on:click="archiveProject">Archive</a> -->
            </div>
        </template>
    </div>
</div>
</template>


<script>
import {mapActions} from 'vuex';


export default {
    props: ['project', 'index', 'key', 'toggleProjectModal'],
    methods: {
        ...mapActions({
            deleteProject: 'clients/deleteProject',
        }),
    },
};
</script>
