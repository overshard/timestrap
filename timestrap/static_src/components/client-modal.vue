<template>
<modal>
    <h5 slot="header">
        <i class="fa fa-address-book mr-1" aria-hidden="true"></i>
        {{ config.task ? 'Edit: ' + config.task.name : 'New Client' }}
    </h5>

    <div slot="body">
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

    <div slot="footer">
        <button name="task-modal-cancel"
                type="button"
                class="btn btn-secondary"
                @click="$emit('close')">
            Close
        </button>
        <button name="task-modal-submit"
                type="submit"
                class="btn btn-primary"
                @click="submit">
            {{ config.task ? 'Save Changes' : 'Add Client' }}
        </button>
    </div>
</modal>
</template>

<script>
const Modal = require('./modal.vue');

export default {
    props: ['config'],
    data() {
        return {
            name: this.config.client ? this.config.client.name : null,
            invoice_email: this.config.client ? this.config.client.invoice_email : null
        };
    },
    methods: {
        submit() {
            let body = {
                name: this.name,
                invoice_email: this.invoice_email
            };
            let url = timestrapConfig.API_URLS.CLIENTS;
            let method = 'post';
            if (this.config.client) {
                url = this.config.client.url;
                method = 'put';
            }
            this.$quickFetch(url, method, body).then(data => {
                this.$emit('updateClient', data, this.config.index);
                this.name = null;
                this.invoice_email = null;
                this.$emit('close');
            }).catch(error => console.log(error));
        }
    },
    components: {
        Modal
    }
};
</script>
