<template>
<div class="modal fade" id="new-client-modal">
    <div class="modal-dialog">
        <form id="client-add"
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
                <div class="form-group">
                    <input name="client-name"
                           placeholder="Client Name"
                           type="text"
                           class="form-control"
                           v-model.trim="name"
                           required />
                </div>
                <div class="form-group">
                    <input name="client-email"
                           placeholder="Invoicing Email"
                           type="text"
                           class="form-control"
                           v-model.trim="invoice_email" />
                </div>
            </div>
            <div class="modal-footer">
                <button name="client-add-cancel"
                        type="button"
                        class="btn btn-secondary"
                        data-dismiss="modal">
                    Close
                </button>
                <button name="client-add-submit" type="submit" class="btn btn-primary">
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
                name: this.name,
                invoice_email: this.invoice_email
            };
            this.$quickFetch(timestrapConfig.API_URLS.CLIENTS, 'post', body).then(data => {
                $('#new-client-modal').modal('hide');
                this.name = '';
                this.$emit('appendClient', data);
            }).catch(error => console.log(error));
        }
    }
};
</script>
