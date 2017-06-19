<template>
<div class="modal fade" id="new-project-modal">
    <div class="modal-dialog">
        <form name="project-add"
                class="modal-content"
                v-on:submit.prevent
                v-on:submit="submitProject">
            <div class="modal-header">
                <h5 class="modal-title">
                    New Project
                </h5>
            </div>
            <div class="modal-body">
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
                           v-model.trim="project_name"
                           placeholder="Project Name"
                           required />
                </div>
                <div class="form-group">
                    <label>Estimate</label>
                    <input name="project-estimate"
                           type="text"
                           class="form-control form-control-sm"
                           placeholder="Hours Estimate"
                           v-model.number="project_estimate" />
                </div>
            </div>
            <div class="modal-footer">
                <button name="project-add-cancel"
                        type="button"
                        class="btn btn-secondary"
                        data-dismiss="modal">
                    Close
                </button>
                <button name="project-add-submit" type="submit" class="btn btn-primary">
                    Add Project
                </button>
            </div>
        </form>
    </div>
</div>
</template>

<script>
const Select2 = require('./select2.vue');

export default {
    data() {
        return {
            clients: null,
            projects: null
        };
    },
    methods: {
        submitProject(e) {
            const body = {
                name: this.project_name,
                estimate: this.project_estimate,
                client: this.client
            };
            this.$quickFetch(timestrapConfig.API_URLS.PROJECTS, 'post', body).then(data => {
                if (data.id) {
                    $('#new-project-modal').modal('hide');
                    this.project_name = '';
                    this.project_estimate = '';
                    this.$emit('appendProject', data);
                }
            }).catch(error => console.log(error));
        }
    },
    created() {
        let clients = this.$quickFetch(timestrapConfig.API_URLS.CLIENTS);
        clients.then(data => {
            this.clients = data.map(function(client) {
                return { id: client.url, text: client.name };
            });
        });
    },
    components: {
        Select2
    }
};
</script>
