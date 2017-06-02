<template>
<div class="row py-2 bg-faded">
    <div class="mb-1 col-6">{{ project.name }}</div>
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
    <div class="col-2">
        <button name="project-change"
                class="btn btn-warning btn-sm w-100">
            Edit
        </button>
    </div>
</div>
</template>

<script>
export default {
    props: ['project'],
    data() {
        return {};
    },
    methods: {
        editProject() {
            console.log(this);
        },
        saveProject() {
            console.log(this);
        }
    }
};
</script>
