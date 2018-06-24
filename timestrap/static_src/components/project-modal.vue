<template>
<modal>
    <h5 slot="header">
        {{ config.project ? 'Edit: ' + config.project.name : 'New Project' }}
    </h5>

    <div slot="body">
        <div class="form-group">
            <div class="form-group" v-if="!config.project">
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
                       v-model.trim="project_name"
                       placeholder="Project Name"
                       required />
            </div>
            <div class="form-group">
                <label>Estimate</label>
                <input name="project-estimate"
                       type="text"
                       class="form-control form-control-sm"
                       placeholder="Cost Estimate"
                       v-model.number="project_estimate" />
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
            {{ config.project ? 'Save Changes' : 'Add Project' }}
        </button>
    </div>
</modal>
</template>

<script>
import Modal from './modal.vue';
import Select2 from './select2.vue';

export default {
    props: ['config'],
    data() {
        return {
            clients: null,
            client: this.config.project ? this.config.project.client : null,
            project_name: this.config.project ? this.config.project.name : null,
            project_estimate: this.config.project ? this.config.project.estimate : null
        };
    },
    methods: {
        submit() {
            let body = {
                name: this.project_name,
                estimate: this.project_estimate,
                client: this.client
            };
            let url = timestrapConfig.API_URLS.PROJECTS;
            let method = 'post';
            if (this.config.project) {
                url = this.config.project.url;
                method = 'put';
            }
            this.$quickFetch(url, method, body).then(data => {
                this.$emit('updateProject', data, this.config.index, this.config.client_index);
                this.client = null;
                this.project_name = null;
                this.project_estimate = null;
                this.$emit('close');
            }).catch(error => console.log(error));
        }
    },
    created() {
        this.$quickFetch(timestrapConfig.API_URLS.CLIENTS).then(data => {
            this.clients = data.map(function(client) {
                return { id: client.url, text: client.name };
            });
        });
    },
    components: {
        Modal,
        Select2
    }
};
</script>
