<template>
<cards
  :number-of-elements="clients(search).length"
  :view_perm="$perms.view_client"
  @search="search = $event">
  <template slot="cards-title">
    <icon :icon="['fas', 'address-book']" class="fa-sm mr-2"/>
    Clients
  </template>

  <template slot="cards-list">
    <client
      v-for="(client, index) in clients(search)"
      :key="client.id"
      :client="client"
      :index="index"
      @modal="modalToggle(client)"/>
  </template>

  <template slot="cards-new">
    <client @modal="modalToggle()"/>
  </template>

  <client-modal
    slot="cards-modal"
    v-if="modalShow"
    :client="modalClient"
    @close="modalShow = false"/>
</cards>
</template>


<script>
import {mapGetters, mapActions} from 'vuex';

import Cards from '../cards/cards.vue';
import Client from './client.vue';
import ClientModal from './client-modal.vue';


export default {
  components: {
    Cards,
    Client,
    ClientModal,
  },
  data() {
    return {
      search: '',
      modalClient: null,
      modalShow: false,
    };
  },
  computed: {
    ...mapGetters({
      clients: 'clients/getSearchClients',
    }),
  },
  methods: {
    modalToggle: function(client) {
      if (typeof(client) !== 'undefined') this.modalClient = client;
      else this.modalClient = null;
      this.modalShow = !this.modalShow;
    },
  }
};
</script>
