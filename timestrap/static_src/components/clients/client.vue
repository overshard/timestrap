<template>
<div class="client">
    <div class="row py-2 bg-secondary text-white">
        <div v-bind:class="['col-sm-4', 'd-flex', 'align-items-center']">
            <i class="fa fa-address-book mr-2" aria-hidden="true"></i>
            <span class="font-weight-bold text-uppercase client-name">{{ client.name }}</span>
        </div>
        <div class="col-sm-2 d-flex align-items-center">
            <i class="fa fa-clock-o mr-2" aria-hidden="true"></i>
            <strong>Total Time</strong>
        </div>
        <div class="col-sm-2 d-flex align-items-center">
            <i class="fa fa-list mr-2" aria-hidden="true"></i>
            <strong>Entries</strong>
        </div>
        <div class="col-sm-3 d-flex align-items-center">
            <i class="fa fa-percent mr-2" aria-hidden="true"></i>
            <strong>Progress</strong>
        </div>
        <div class="col-sm-1 d-flex align-self-center justify-content-end">
            <template v-if="this.$perms.change_client || this.$perms.delete_client">
                <button name="client-menu"
                        class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                        type="button"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
                </button>
                <div class="dropdown-menu dropdown-menu-right"
                        aria-labelledby="entry-menu">
                    <a id="client-menu-change"
                        class="dropdown-item"
                        href="#"
                        v-if="this.$perms.change_client"
                        v-on:click.prevent
                        v-on:click="toggleClientModal(client)">Edit</a>
                    <a id="client-menu-delete"
                        class="dropdown-item"
                        href="#"
                        v-if="this.$perms.delete_client"
                        v-on:click.prevent
                        v-on:click="deleteClient(index)">Delete</a>
                    <!-- <a id="client-menu-archive"
                        class="dropdown-item"
                        href="#"
                        v-if="this.$perms.change_client"
                        v-on:click.prevent
                        v-on:click="archiveClient">Archive</a> -->
                </div>
            </template>
        </div>
    </div>

    <template v-if="this.$perms.view_project">
        <project v-for="(project, project_index) in projects(client.url)" v-bind:project="project"
                 v-bind:index="project_index" v-bind:key="project.id"
                 v-bind:toggleProjectModal="toggleProjectModal"></project>
    </template>

</div>
</template>


<script>
import {mapActions, mapGetters} from 'vuex';

import Project from './project.vue';


export default {
    props: ['client', 'index', 'key', 'toggleClientModal', 'toggleProjectModal', 'removeProject'],
    computed: {
        ...mapGetters({
            projects: 'clients/getClientProjects'
        }),
    },
    methods: {
        ...mapActions({
            deleteClient: 'clients/deleteClient',
        }),
    },
    components: {
        Project,
    },
};
</script>
