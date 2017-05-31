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

    <div class="client-rows rounded">
        <div v-for="client in clients" class="row py-2 bg-faded rounded mb-2">
            <div class="col-6 d-flex align-items-center">
                <a class="client-view-projects text-primary font-weight-bold"
                   v-on:click="showProjects">
                    <i class="fa fa-chevron-circle-up small mr-2" aria-hidden="true"></i>
                    <span class="mb-1">{{ client.name }}</span>
                </a>
                <!--<span class="text-primary font-weight-bold">{{ client.name }}</span>-->
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
                <span class="mb-1">{{ client.total_duration }}</span>
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
                <span class="mb-1">{{ client.total_projects }}</span>
            </div>
            <div class="col-2">
                <button name="client-change"
                        class="btn btn-warning btn-sm w-100">
                    Edit
                </button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
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
        showProjects() {
            console.log(this);
        },
        submitClient() {
            console.log(this);
        }
    },
    mounted() {
        return this.getClients();
    }
}
</script>
