<template>
<div class="container">
    <div class="row py-2 mb-4 bg-light rounded"
         v-if="this.$perms.add_client || this.$perms.add_project">
        <div class="col-12">
            <button name="client-add"
                    type="button"
                    class="btn btn-primary btn-sm"
                    @click="toggleClientModal"
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

            <button class="btn btn-secondary btn-sm pull-right ml-2"
                    v-on:click.prevent
                    v-block-during-fetch
                    v-on:click="refresh">
                <i class="fa fa-refresh" aria-hidden="true"></i> Refresh
            </button>
        </div>
    </div>

    <client-modal id="client-modal"
                   v-if="modal_config.client.show"
                   @updateClient="updateClient"
                   @close="toggleClientModal"
                   v-bind:config="modal_config.client"></client-modal>

    <project-modal id="project-modal"
                   v-if="modal_config.project.show"
                   @updateProject="updateProject"
                   @close="toggleProjectModal"
                   v-bind:config="modal_config.project"></project-modal>

    <div v-if="this.$perms.view_client" id="client-rows">
        <client v-for="(client, index) in clients"
                v-bind:client="client"
                v-bind:index="index"
                v-bind:key="client.id"
                v-bind:toggleEditModal="toggleClientModal"
                @removeClient="removeClient"
                v-bind:toggleProjectEditModal="toggleProjectModal"
                v-bind:removeProject="removeProject"></client>
    </div>

</div>
</template>

<script>
import Client from './client.vue';
import ClientModal from './client-modal.vue';
import ProjectModal from './project-modal.vue';

export default {
    data() {
        return {
            clients: null,
            modal_config: {
                project: {
                    index: null,
                    project: null,
                    client_index: null,
                    show: false
                },
                client: {
                    index: null,
                    client: null,
                    show: false
                }
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
        toggleClientModal(client, index) {
            if (client && (index || index === 0)) {
                this.modal_config.client.client = client;
                this.modal_config.client.index = index;
            }
            else {
                this.modal_config.client.client = null;
                this.modal_config.client.index = null;
            }
            this.modal_config.client.show = !this.modal_config.client.show;
        },
        updateClient(client, index) {
            if (client && (index || index === 0)) {
                this.clients[index] = client;
            }
            else {
                this.clients.unshift(client);
            }
        },
        removeClient(index) {
            this.$delete(this.clients, index);
        },
        toggleProjectModal(project, index, client_index) {
            if (project && (index || index === 0) && (client_index || client_index === 0)) {
                this.modal_config.project.project = project;
                this.modal_config.project.index = index;
                this.modal_config.project.client_index = client_index;
            }
            else {
                this.modal_config.project.project = null;
                this.modal_config.project.index = null;
                this.modal_config.project.client_index = null;
            }
            this.modal_config.project.show = !this.modal_config.project.show;
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
        },
        removeProject(client_index, index) {
            this.$delete(this.clients[client_index].projects, index);
        },
        refresh() {
            return this.getClients();
        }
    },
    mounted() {
        return this.getClients();
    },
    components: {
        Client,
        ClientModal,
        ProjectModal
    }
};
</script>

<style lang="scss">
.client {
    font-size: .9em;

    .row {
        border-top: 1px solid #eee;

        &:not(.bg-secondary) {
            &:nth-of-type(2n+1) {
                background-color: #fbf3e5 !important;
            }
        }

        &:last-child {
            border-bottom: 1px solid #eee;
            margin-bottom: 1rem;
        }
    }
}

.project {
    background: #fff;
}
</style>
