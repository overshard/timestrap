<template>
<div class="modal fade" id="newClientModal">
    <div class="modal-dialog">
        <form name="client-add"
                class="modal-content"
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
</template>

<script>
export default {
    data() {
        return {};
    },
    methods: {
        submitClient(e) {
            let body = {
                name: this.name
            };
            this.$quickFetch(timestrapConfig.API_URLS.CLIENTS, 'post', body).then(data => {
                $('#newClientModal').modal('hide');
                this.name = '';
                this.$emit('appendClient', data);
            }).catch(error => console.log(error));
        }
    }
};
</script>
