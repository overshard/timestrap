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
            <div v-bind:class="['col-' + [this.$perms.change_task ? '4' : '6'], 'd-flex', 'align-items-center']">
                <span class="font-weight-bold text-uppercase client-name">{{ client.name }}</span>
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
                Total Time
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
                Entries
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-percent text-muted mr-2" aria-hidden="true"></i>
                Progress
            </div>
            <div class="col-sm-2 d-flex align-self-center justify-content-end">
                <template v-if="this.$perms.change_client || this.$perms.delete_client">
                    <button name="client-menu"
                            class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                            type="button"
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right"
                         aria-labelledby="entry-menu">
                        <a id="client-menu-change"
                           class="dropdown-item"
                           href="#"
                           v-if="this.$perms.change_client"
                           v-on:click.prevent
                           v-on:click="editClient">
                            Edit
                        </a>
                        <a id="client-menu-delete"
                           class="dropdown-item"
                           href="#"
                           v-if="this.$perms.delete_client"
                           v-on:click.prevent
                           v-on:click="deleteClient">
                            Delete
                        </a>
                        <a id="client-menu-archive"
                           class="dropdown-item"
                           href="#"
                           v-if="this.$perms.change_client"
                           v-on:click.prevent
                           v-on:click="archiveClient">
                            Archive
                        </a>
                    </div>
                </template>
            </div>
        </template>
    </div>

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
        deleteClient() {
            this.$quickFetch(this.client.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    $.growl.notice({ message: 'Client deleted!' });
                    this.$emit('delete-client');
                } else {
                    $.growl.error({ message: 'Client delete failed ):' });
                }
            }.bind(this));
        },
        archiveClient() {
            const body = {
                name: this.client.name,
                archive: true
            };
            this.$quickFetch(this.client.url, 'put', body).then(data => {
                if (data.id) {
                    $.growl.notice({ message: 'Client archived!' });
                    this.$emit('archive-client');
                }
            }).catch(error => console.log(error));
        }
    },
    components: {
        Project
    }
};
</script>
