<template>
<div class="row py-2 bg-faded rounded mb-2">

    <template v-if="edit">
    </template>

    <template v-else>
    <div class="col-8 d-flex align-items-center">
        <span class="font-weight-bold">{{ task.name }}</span>
    </div>
    <div class="col-2 d-flex align-items-center">
        <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">${{ task.hourly_rate }}</span>
    </div>
    <div class="col-2">
        <button name="task-change"
                class="btn btn-warning btn-sm w-100"
                v-on:click="editTask">
            Edit
        </button>
    </div>
    </template>
</div>
</template>

<script>
export default {
    props: ['task'],
    data() {
        return {
            edit: false,
            name: this.task.name,
            hourly_rate: this.task.hourly_rate
        };
    },
    methods: {
        editTask() {
            this.edit = true;
        },
        saveTask() {
            console.log(this);
        },
    }
};
</script>
