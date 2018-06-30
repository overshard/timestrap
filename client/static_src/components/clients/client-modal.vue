<template>
  <modal>
    <h5 slot="header">
      <i class="fa fa-address-book mr-1"/>
      {{ id ? 'Edit: ' + name : 'New Client' }}
    </h5>

    <div slot="body">
      <form
        @submit.prevent
        @keyup.enter="submit">
        <div class="form-group">
          <label>Client Name</label>
          <input
            id="client-modal-name"
            v-model.trim="name"
            placeholder="Client Name"
            type="text"
            class="form-control form-control-sm"
            required >
        </div>
      </form>
    </div>

    <div slot="footer">
      <button
        id="client-modal-close"
        type="button"
        class="btn btn-secondary"
        @click="$emit('close')">
        Close
      </button>
      <button
        id="client-modal-submit"
        type="submit"
        class="btn btn-primary"
        @click="submit">
        {{ id ? 'Save Changes' : 'Add Client' }}
      </button>
    </div>
  </modal>
</template>


<script>
import {mapActions} from 'vuex';

import Modal from '../modal.vue';


export default {
  components: {
    Modal,
  },
  props: [
    'config',
  ],
  data() {
    return {
      id: this.config.client ? this.config.client.id : null,
      url: this.config.client ? this.config.client.url : null,
      name: this.config.client ? this.config.client.name : null,
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
};
</script>
