<template>
<modal>
    <h5 slot="header">
        <i class="fa fa-address-book mr-1" aria-hidden="true"></i>
        {{ config.client ? 'Edit: ' + config.client.name : 'New Client' }}
    </h5>

    <div slot="body">
        <div class="form-group">
            <label>Client Name</label>
            <input name="client-name"
                   placeholder="Client Name"
                   type="text"
                   class="form-control form-control-sm"
                   v-model.trim="name"
                   required />
        </div>
    </div>

    <div slot="footer">
        <button name="client-modal-cancel"
                type="button"
                class="btn btn-secondary"
                @click="$emit('close')">
            Close
        </button>
        <button name="client-modal-submit"
                type="submit"
                class="btn btn-primary"
                @click="submit">
            {{ config.client ? 'Save Changes' : 'Add Client' }}
        </button>
    </div>
</modal>
</template>

<script>
import Modal from '../modal.vue';

export default {
    props: ['config'],
    data() {
        return {
            name: this.config.client ? this.config.client.name : null
        };
    },
    methods: {
        submit() {
            let body = {
                name: this.name
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
                this.bus.$emit('updateProjects');
                this.$emit('close');
            }).catch(error => console.log(error));
        }
    },
    components: {
        Modal
    }
};
</script>
