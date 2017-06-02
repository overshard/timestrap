<template>
<div class="row py-2 bg-faded rounded mb-2">
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
                class="btn btn-warning btn-sm w-100">
            Edit
        </button>
    </div>

    <div class="col-12" v-if="showProjects">
        <form name="project-add"
              v-if="showProjects"
              v-on:submit.prevent="onSubmit"
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
    </div>
</div>
</template>

<script>
export default {
    props: ['client'],
    data() {
        return {
            showProjects: false
        };
    },
    methods: {
        toggleProjects() {
            this.showProjects = !this.showProjects;
        },
        submitProject() {
            console.log(this);
        }
    },
    mounted() {
    }
};
</script>
