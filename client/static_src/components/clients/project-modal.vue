<template>
<modal>
    <h5 slot="header">
        {{ this.id ? 'Edit: ' + this.name : 'New Project' }}
    </h5>

    <div slot="body">
        <div class="form-group">
            <div class="form-group">
                <label>Client</label>
                <select2 id="project-client"
                         v-model="client"
                         v-bind:options="clients"
                         placeholder="Clients"></select2>
            </div>
            <div class="form-group">
                <label>Name</label>
                <input name="project-name"
                       type="text"
                       class="form-control form-control-sm"
                       v-model.trim="name"
                       placeholder="Project Name"
                       required />
            </div>
            <div class="form-group">
                <label>Estimate</label>
                <input name="project-estimate"
                       type="text"
                       class="form-control form-control-sm"
                       placeholder="Cost Estimate"
                       v-model.number="estimate" />
            </div>
        </div>
    </div>

    <div slot="footer">
        <button name="project-modal-cancel"
                type="button"
                class="btn btn-secondary"
                @click="$emit('close')">
            Close
        </button>
        <button name="project-modal-submit"
                type="submit"
                class="btn btn-primary"
                @click="submit">
            {{ this.id ? 'Save Changes' : 'Add Project' }}
        </button>
    </div>
</modal>
</template>


<script>
import {mapActions, mapGetters} from 'vuex';

import Modal from '../modal.vue';
import Select2 from '../select2.vue';


export default {
    props: ['config'],
    data() {
        return {
            id: this.config.project ? this.config.project.id : null,
            url: this.config.project ? this.config.project.url : null,
            client: this.config.project ? this.config.project.client : null,
            name: this.config.project ? this.config.project.name : null,
            estimate: this.config.project ? this.config.project.estimate : null,
        };
    },
    computed: {
        ...mapGetters({
            clients: 'clients/getSelectClients',
        }),
    },
    methods: {
        ...mapActions({
            createProject: 'clients/createProject',
            editProject: 'clients/editProject',
        }),
        submit() {
            if (!this.id) this.createProject(this.$data);
            else this.editProject(this.$data);
            this.$emit('close');
        },
    },
    components: {Modal, Select2},
};
</script>
