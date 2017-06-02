<template>
<div class="container">
    <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top">
        <div class="col-sm-6">
            Client
        </div>
        <div class="col-sm-2">
            Total Time
        </div>
        <div class="col-sm-2">
            # Related
        </div>
        <div class="col-sm-2">
        </div>
    </div>

    <form name="client-add"
          class="row mb-4 py-2 bg-faded rounded-bottom"
          v-on:submit.prevent="onSubmit"
          v-on:submit="submitClient">
        <div class="col-10">
            <input name="client-name"
                   type="text"
                   class="form-control form-control-sm"
                   v-model="name"
                   placeholder="New Client Name"
                   required>
        </div>
        <div class="col-2">
            <button
                    name="client-add-submit"
                    type="submit"
                    class="btn btn-success btn-sm w-100"
                    v-on:click="submitClient">
                Add
            </button>
        </div>
    </form>

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
            quickFetch(url).then(data => {
                this.clients = data;
            }).catch(error => console.log(error));
        },
        submitClient() {
            console.log(this);
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
