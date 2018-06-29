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
                    v-on:click.prevent v-on:click="refresh">
                <i class="fa fa-refresh" aria-hidden="true"></i>
                Refresh
            </button>
        </div>
    </div>

    <div v-show="loading" class="container text-center py-4">
        <i class="fa fa-spinner text-primary fa-spin display-3 text-center"></i>
    </div>

    <client-modal id="client-modal"
                   v-if="modalClient.show"
                   @close="toggleClientModal"
                   v-bind:config="modalClient"></client-modal>

    <project-modal id="project-modal"
                   v-if="modalProject.show"
                   @close="toggleProjectModal"
                   v-bind:config="modalProject"></project-modal>

    <div v-if="this.$perms.view_client" id="client-rows">
        <client v-for="(client, index) in clients" v-bind:client="client"
                v-bind:index="index" v-bind:key="client.id"
                v-bind:toggleClientModal="toggleClientModal"
                v-bind:toggleProjectModal="toggleProjectModal"></client>
    </div>
</div>
</template>


<script>
import {mapState, mapActions} from 'vuex';

import Client from './client.vue';
import ClientModal from './client-modal.vue';
import ProjectModal from './project-modal.vue';


export default {
    data() {
        return {
            modalClient: {
                client: null,
                show: false,
            },
            modalProject: {
                project: null,
                show: false,
            },
        };
    },
    computed: {
        ...mapState({
            loading: state => state.loading,
            clients: state => state.clients.allClients,
        }),
    },
    methods: {
        ...mapActions('clients', [
            'getClients',
        ]),
        toggleClientModal(client) {
            if (client) this.modalClient.client = client;
            else this.modalClient.client = null;
            this.modalClient.show = !this.modalClient.show;
        },
        toggleProjectModal(project) {
            if (project) this.modalProject.project = project;
            else this.modalProject.project = null;
            this.modalProject.show = !this.modalProject.show;
        },
        refresh() {
            this.getClients();
        }
    },
    components: {
        Client,
        ClientModal,
        ProjectModal,
    },
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
