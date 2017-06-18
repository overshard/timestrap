<template>
<div class="container">
    <div class="row py-2 mb-4 bg-faded rounded">
        <div class="col-12">
            <button type="button"
                    class="btn btn-primary btn-sm"
                    data-toggle="modal"
                    data-target="#newClientModal">
                <i class="fa fa-plus mr-1" aria-hidden="true"></i>
                New Client
            </button>
        </div>
    </div>

    <div class="modal fade" id="newClientModal">
        <div class="modal-dialog">
            <form name="client-add"
                  class="modal-content"
                  v-if="this.$perms.add_client"
                  v-on:submit.prevent
                  v-on:submit="submitClient">
                <div class="modal-header">
                    <h5 class="modal-title">
                        <i class="fa fa-address-book mr-1" aria-hidden="true"></i>
                        New Client
                    </h5>
                </div>
                <div class="modal-body">
                    <input name="client-name"
                            type="text"
                            class="form-control"
                            v-model.trim="name"
                            placeholder="Client Name"
                            required />
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">
                        Close
                    </button>
                    <button type="submit" class="btn btn-primary">
                        Add Client
                    </button>
                </div>
            </form>
        </div>
    </div>

    <client v-for="(client, index) in clients"
            v-bind:client="client"
            v-bind:index="index"
            v-bind:key="client.id">
    </client>

</div>
</template>

<script>
const Client = require('./client.vue');

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
        submitClient(e) {
            let body = {
                name: this.name
            };
            this.$quickFetch(timestrapConfig.API_URLS.CLIENTS, 'post', body).then(data => {
                $('#newClientModal').modal('hide');
                this.name = '';
                this.clients.unshift(data);
            }).catch(error => console.log(error));
        }
    },
    mounted() {
        return this.getClients();
    },
    components: {
        Client
    }
};
</script>
