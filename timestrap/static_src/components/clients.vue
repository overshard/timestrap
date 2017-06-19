<template>
<div class="container">
    <div class="row py-2 mb-4 bg-faded rounded"
         v-if="this.$perms.add_client || this.$perms.add_project">
        <div class="col-12">
            <button id="client-add"
                    type="button"
                    class="btn btn-primary btn-sm"
                    data-toggle="modal"
                    data-target="#new-client-modal"
                    v-if="this.$perms.add_client">
                <i class="fa fa-plus mr-1" aria-hidden="true"></i>
                New Client
            </button>
            <button id="project-add"
                    type="button"
                    class="btn btn-primary btn-sm"
                    data-toggle="modal"
                    data-target="#newProjectModal"
                    v-if="this.$perms.add_project">
                <i class="fa fa-plus mr-1" aria-hidden="true"></i>
                New Project
            </button>
        </div>
    </div>

    <new-client @appendClient="appendClient"
                v-if="this.$perms.add_client"></new-client>

    <new-project @appendProject="appendProject"
                 v-if="this.$perms.add_project"></new-project>

    <client v-for="(client, index) in clients"
            v-bind:client="client"
            v-bind:index="index"
            v-bind:key="client.id">
    </client>

</div>
</template>

<script>
const Client = require('./client.vue');
const NewClient = require('./new-client.vue');
const NewProject = require('./new-project.vue');

export default {
    data() {
        return {
            clients: null
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
        appendProject(project) {
            this.clients.map(client => {
                if (client.id === project.client_details.id) {
                    client.projects.unshift(project);
                }
                return client;
            });
        }
    },
    mounted() {
        return this.getClients();
    },
    components: {
        Client,
        NewClient,
        NewProject
    }
};
</script>
