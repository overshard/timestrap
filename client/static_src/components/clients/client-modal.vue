<template>
<modal>
    <h5 slot="header">
        <i class="fa fa-address-book mr-1" aria-hidden="true"></i>
        {{ this.id ? 'Edit: ' + config.client.name : 'New Client' }}
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
import {mapActions} from 'vuex';

import Modal from '../modal.vue';


export default {
    props: ['config'],
    data() {
        return {
            id: this.config.client ? this.config.client.id : null,
            url: this.config.client ? this.config.client.url : null,
            name: this.config.client ? this.config.client.name : null
        };
    },
    methods: {
        ...mapActions({
            createClient: 'clients/createClient',
            editClient: 'clients/editClient',
        }),
        submit() {
            if (!this.id) this.createClient(this.$data);
            else this.editClient(this.$data);
            this.$emit('close');
        },
    },
    components: {Modal},
};
</script>
