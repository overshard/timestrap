<template>
<div class="row py-2 bg-faded rounded mb-2">

    <template v-if="edit">
    <div class="col-10">
        <input name="client-name"
               type="text"
               class="form-control form-control-sm"
               v-model.trim="name"
               v-on:keyup.enter="saveClient"/>
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
    <div class="col-6 d-flex align-items-center">
        <a class="client-view-projects text-primary font-weight-bold"
           v-on:click="toggleProjects">
            <i v-bind:class="['fa', 'small', 'mr-2', [showProjects ? 'fa-chevron-circle-down' : 'fa-chevron-circle-up']]"
               aria-hidden="true"></i>
            <span class="mb-1">{{ client.name }}</span>
        </a>
        <!--<span class="text-primary font-weight-bold">{{ client.name }}</span>-->
    </div>
    <div class="col-2 d-flex align-items-center">
        <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ client.total_duration }}</span>
    </div>
    <div class="col-2 d-flex align-items-center">
        <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ client.total_projects }}</span>
    </div>
    <div class="col-2">
        <button name="client-change"
                class="btn btn-warning btn-sm w-100"
                v-on:click="editClient">
            Edit
        </button>
    </div>
    </template>

    <div class="col-12" v-if="showProjects">
        <form name="project-add"
              v-if="showProjects"
              v-on:submit.prevent
              v-on:submit="submitProject">
            <div class="row bg-faded py-2">
                <div class="col-8">
                    <input name="project-name"
                           type="text"
                           class="form-control form-control-sm"
                           v-model="project_name"
                           placeholder="New Project Name"
                           required/>
                </div>
                <div class="col-2">
                    <input name="project-estimate"
                           type="text"
                           class="form-control form-control-sm"
                           placeholder="Estimate"
                           v-model="estimate"/>
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
            this.edit = true
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
            console.log(this);
        }
    },
    components: {
        Project
    }
};
</script>
