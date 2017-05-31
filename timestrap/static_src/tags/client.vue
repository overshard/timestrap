<template>
<div class="row py-2 bg-faded rounded mb-2">
    <div class="col-6 d-flex align-items-center">
        <a class="client-view-projects text-primary font-weight-bold"
           v-on:click="showProjects">
            <i class="fa fa-chevron-circle-up small mr-2" aria-hidden="true"></i>
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
</div>
</template>

<script>
export default {
    props: ['client'],
    data() {
        return {
        };
    },
    methods: {
        showProjects() {
            console.log(this);
        }
    },
    mounted() {
    }
}
</script>
