<template>
<div class="container">
    <div class="row py-2 mb-4 bg-faded rounded"
         v-if="this.$perms.add_client || this.$perms.add_project">
        <div class="col-12">
            <button name="client-add"
                    type="button"
                    class="btn btn-primary btn-sm"
                    data-toggle="modal"
                    data-target="#new-client-modal"
                    v-if="this.$perms.add_client">
                <i class="fa fa-plus mr-1" aria-hidden="true"></i>
                New Client
            </button>
            <button name="project-add"
                    type="button"
                    class="btn btn-primary btn-sm"
                    @click="toggleProjectModal"
                    v-if="this.$perms.add_project">
                <i class="fa fa-plus mr-1" aria-hidden="true"></i>
                New Project
            </button>
        </div>
    </div>

    <new-client @appendClient="appendClient"
                v-if="this.$perms.add_client"></new-client>

    <project-modal id="project-modal"
                   v-if="project_modal_config.show && (this.$perms.add_project || this.$perms.change_project)"
                   @updateProject="updateProject"
                   @close="toggleProjectModal"
                   v-bind:config="project_modal_config"></project-modal>

    <div v-if="this.$perms.view_client" id="client-rows">
        <client v-for="(client, index) in clients"
                v-bind:client="client"
                v-bind:index="index"
                v-bind:key="client.id"
                v-bind:removeProject="removeProject"
                v-bind:toggleProjectEditModal="toggleProjectModal"></client>
    </div>

</div>
</template>

<script>
const Client = require('./client.vue');
const NewClient = require('./new-client.vue');
const ProjectModal = require('./project-modal.vue');

export default {
    data() {
        return {
            clients: null,
            project_modal_config: {
                index: null,
                project: null,
                client_index: null,
                show: false
            }
        };
    },
    methods: {
        getClients(url) {
            url = (typeof url !== 'undefined') ? url : timestrapConfig.API_URLS.CLIENTS;
            this.$quickFetch(url).then(data => {
                this.clients = data;
            }).catch(error => console.log(error));
        },
        appendClient(client) {
            this.clients.unshift(client);
        },
        toggleProjectModal(project, index, client_index) {
            if (project && (index || index === 0) && (client_index || client_index === 0)) {
                this.project_modal_config.project = project;
                this.project_modal_config.index = index;
                this.project_modal_config.client_index = client_index;
            }
            else {
                this.project_modal_config.project = null;
                this.project_modal_config.index = null;
                this.project_modal_config.client_index = null;
            }
            this.project_modal_config.show = !this.project_modal_config.show;
        },
        updateProject(project, index, client_index) {
            if (project && (index || index === 0) && (client_index || client_index === 0)) {
                this.$set(this.clients[client_index].projects, index, project);
            }
            else {
                for (const [client_index, client] of this.clients.entries()) {
                    if (client.url == project.client) {
                        this.clients[client_index].projects.unshift(project);
                        break;
                    }
                }
            }
            this.project_modal_config.index = null;
            this.project_modal_config.project = null;
            this.project_modal_config.client_index = null;
        },
        removeProject(client_index, index) {
            this.$delete(this.clients[client_index].projects, index);
        },
    },
    mounted() {
        return this.getClients();
    },
    components: {
        Client,
        NewClient,
        ProjectModal
    }
};
</script>
