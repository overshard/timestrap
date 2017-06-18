<template>
<div class="client">
    <div class="row py-2 bg-faded">
        <template v-if="edit">
            <div class="col-6">
                <input name="client-name"
                    type="text"
                    class="form-control form-control-sm"
                    v-model.trim="name"
                    v-on:keyup.enter="saveClient"
                    required />
            </div>
            <div class="col-4">
                <input name="client-email"
                    placeholder="Invoicing Email"
                    type="text"
                    class="form-control form-control-sm"
                    v-model.trim="invoice_email"
                    v-on:keyup.enter="saveClient" />
            </div>
            <div class="col-2">
                <button name="client-save"
                        class="btn btn-success btn-sm w-100"
                        v-block-during-fetch
                        v-on:click="saveClient">
                    Save
                </button>
            </div>
        </template>

        <template v-else>
            <div v-bind:class="['col-' + [this.$perms.change_task ? '6' : '8'], 'd-flex', 'align-items-center']">
                <a class="client-view-projects text-primary font-weight-bold"
                v-if="this.$perms.view_project"
                v-on:click="toggleProjects">
                    <span class="text-uppercase">{{ client.name }}</span>
                </a>
                <span class="text-primary font-weight-bold" v-else>{{ client.name }}</span>
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
                Total Time
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
                Entries
            </div>
            <div class="col-sm-2 d-flex align-self-center justify-content-end">
                <template v-if="this.$perms.change_client || this.$perms.delete_client">
                    <button name="entry-menu"
                            class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                            type="button"
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right"
                         aria-labelledby="entry-menu">
                        <a class="dropdown-item client-menu-change"
                           href="#"
                           v-if="this.$perms.change_entry"
                           v-on:click.prevent
                           v-on:click="editClient">
                            Edit
                        </a>
                        <a class="dropdown-item client-menu-new" href="#">
                            New Project
                        </a>
                    </div>
                </template>
            </div>
        </template>
    </div>

    <form name="project-add"
            v-if="this.$perms.add_project"
            v-on:submit.prevent
            v-on:submit="submitProject">
        <div class="row bg-faded py-2">
            <div class="col-8">
                <input name="project-name"
                        type="text"
                        class="form-control form-control-sm"
                        v-model.trim="project_name"
                        placeholder="New Project Name"
                        required/>
            </div>
            <div class="col-2">
                <input name="project-estimate"
                        type="text"
                        class="form-control form-control-sm"
                        placeholder="Estimate"
                        v-model.number="project_estimate"/>
            </div>
            <div class="col-2">
                <button name="project-add-submit"
                        type="submit"
                        class="btn btn-success btn-sm w-100"
                        v-block-during-fetch>
                    Add
                </button>
            </div>
        </div>
    </form>

    <project v-for="(project, index) in client.projects"
            v-bind:project="project"
            v-bind:index="index"
            v-bind:key="client.projects.id">
    </project>
</div>
</template>

<script>
const Project = require('./project.vue');

export default {
    props: ['client'],
    data() {
        return {
            edit: false,
            name: this.client.name,
            invoice_email: this.client.invoice_email
        };
    },
    methods: {
        editClient() {
            this.edit = true;
        },
        saveClient(e) {
            const body = {
                name: this.name,
                invoice_email: this.invoice_email
            };
            this.$quickFetch(this.client.url, 'put', body).then(data => {
                if (data.id) {
                    this.client.name = data.name;
                    this.client.invoice_email = data.invoice_email;
                    this.edit = false;
                }
            }).catch(error => console.log(error));
        },
        submitProject(e) {
            const body = {
                name: this.project_name,
                estimate: this.project_estimate,
                client: this.client.url
            };
            this.$quickFetch(timestrapConfig.API_URLS.PROJECTS, 'post', body).then(data => {
                if (data.id) {
                    this.project_name = '';
                    this.project_estimate = '';
                    this.client.projects.unshift(data);
                }
            }).catch(error => console.log(error));
        }
    },
    components: {
        Project
    }
};
</script>
