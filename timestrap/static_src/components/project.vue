<template>
<div class="project row py-2 bg-faded">

    <template v-if="edit && global.perms.change_project">
    <div class="col-8">
        <input name="project-name"
               type="text"
               class="form-control form-control-sm"
               v-model.trim="name"
               v-on:keyup.enter="saveProject"
               required/>
    </div>
    <div class="col-2">
        <input name="project-estimate"
               type="text"
               class="form-control form-control-sm"
               placeholder="Estimate"
               v-model.number="estimate"
               v-on:keyup.enter="saveProject"
               required/>
    </div>
    <div class="col-2">
        <button name="project-save"
                class="btn btn-success btn-sm w-100"
                v-on:click="saveProject">
            Save
        </button>
    </div>
    </template>

    <template v-else>
    <div v-bind:class="['col-' + [global.perms.change_project ? '6' : '8'], 'mb-1']">{{ project.name }}</div>
    <div class="col-4 d-flex align-items-center" v-if="project.percent_done">
        <div class="progress w-100">
            <div v-if="project.percent_done"
                 v-bind:class="['progress-bar', [project.percent_done > 100 ? 'bg-danger' : '']]"
                 v-bind:style="{ width: project.percent_done + '%' }">
                {{ project.percent_done }}%
            </div>
        </div>
    </div>
    <div class="col-2 d-flex align-items-center" v-if="!project.percent_done">
        <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ project.total_duration }}</span>
    </div>
    <div class="col-2 d-flex align-items-center" v-if="!project.percent_done">
        <i class="fa fa-list text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">{{ project.total_entries }}</span>
    </div>
    <div class="col-2" v-if="global.perms.change_project">
        <button name="project-change"
                class="btn btn-warning btn-sm w-100"
                v-on:click="editProject">
            Edit
        </button>
    </div>
    </template>
</div>
</template>

<script>
export default {
    props: ['project'],
    data() {
        return {
            edit: false,
            estimate: this.project.estimate,
            name: this.project.name
        };
    },
    methods: {
        editProject() {
            this.edit = true;
        },
        saveProject() {
            let body = {
                client: this.project.client,
                estimate: this.estimate,
                name: this.name
            };
            quickFetch(this.project.url, 'put', body).then(data => {
                if (data.id) {
                    this.project.name = data.name;
                    this.project.estimate = data.estimate;
                    this.project.percent_done = data.percent_done;
                    this.edit = false;
                }
            }).catch(error => console.log(error));
        }
    }
};
</script>
