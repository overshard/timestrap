<template>
<card-modal
  :data="$data"
  :edit="editClient"
  :create="createClient"
  @close="$emit('close')">
  <template slot="modal-body">
    <div class="form-group">
      <label for="client-name">
        Name
      </label>
      <input
        id="client-name"
        name="client-name"
        v-model="name"
        class="form-control shadow-sm"
        placeholder="Empty"
        required/>
    </div>
  </template>
</card-modal>
</template>


<script>
import {mapActions} from 'vuex';

import CardModal from '../cards/card-modal.vue';


export default {
  components: {
    CardModal,
  },
  props: {
    client: {
      type: Object,
    },
  },
  data() {
    return {
      id: this.client ? this.client.id : null,
      url: this.client ? this.client.url : null,
      name: this.client ? this.client.name : null,
      hourly_rate: this.client ? this.client.hourly_rate : null,
    }
  },
  methods: {
    ...mapActions({
      editClient: 'clients/editClient',
      createClient: 'clients/createClient',
    }),
  },
};
</script>
