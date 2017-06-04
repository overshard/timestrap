<template>
<div class="client row py-2 bg-faded rounded mb-2">

    <template v-if="edit">
    <div class="col-10">
        <input name="client-name"
               type="text"
               class="form-control form-control-sm"
               v-model.trim="name"
               v-on:keyup.enter="saveClient"
               required/>
    </div>
    <div class="col-2">
        <button name="client-save"
                class="btn btn-success btn-sm w-100"
                v-on:click="saveClient">
            Save
        </button>
    </div>
    </template>

    <template v-else>
    <div :class="['col-' + [global.perms.change_task ? '6' : '8'], 'd-flex', 'align-items-center']">
        <a class="client-view-projects text-primary font-weight-bold"
           v-if="global.perms.view_project"
           v-on:click="toggleProjects">
            <i v-bind:class="['fa', 'small', 'mr-2', 'fa-chevron-circle-' + [showProjects ? 'down' : 'up']]"
               aria-hidden="true"></i>
            <span class="mb-1">{{ client.name }}</span>
        </a>
        <span class="text-primary font-weight-bold" v-else>{{ client.name }}</span>
    </div>
    <div class="col-2 d-flex align-items-center">
        <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ client.total_duration }}</span>
    </div>
    <div class="col-2 d-flex align-items-center">
        <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ client.total_projects }}</span>
    </div>
    <div class="col-2" v-if="global.perms.change_client">
        <button name="client-change"
                class="btn btn-warning btn-sm w-100"
                v-on:click="editClient">
            Edit
        </button>
    </div>
    </template>

    <div class="col-12" v-if="showProjects">
        <form name="project-add"
              v-if="global.perms.add_project"
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
                            class="btn btn-success btn-sm w-100">
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
            showProjects: false
        };
    },
    methods: {
        editClient() {
            this.edit = true;
        },
        saveClient() {
            let body = {
                name: this.name
            };
            quickFetch(this.client.url, 'put', body).then(data => {
                if (data.id) {
                    this.client.name = data.name;
                    this.edit = false;
                }
            }).catch(error => console.log(error));
        },
        toggleProjects() {
            this.showProjects = !this.showProjects;
        },
        submitProject() {
            let body = {
                name: this.project_name,
                estimate: this.project_estimate,
                client: this.client.url
            };
            quickFetch(timestrapConfig.API_URLS.PROJECTS, 'post', body).then(data => {
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
