<template>
<div class="container">
    <div class="mb-4 clearfix">
        <pager :next="next"
               :previous="previous"
               @next-page="getTasks(next)"
               @previous-page="getTasks(previous)"></pager>
    </div>

    <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top">
        <div class="col-sm-8">
            Task
        </div>
        <div class="col-sm-2">
            Hourly Rate
        </div>
        <div class="col-sm-2">
        </div>
    </div>

    <form name="task-add"
          class="row mb-4 py-2 bg-faded rounded-bottom"
          v-on:submit.prevent="onSubmit"
          v-on:submit="submitTask">
        <div class="col-8">
            <input name="task-name"
                   type="text"
                   class="form-control form-control-sm"
                   v-model="name"
                   placeholder="New Task Name"
                   required>
        </div>
        <div class="col-2">
            <input name="task-hourly-rate"
                   type="text"
                   class="form-control form-control-sm"
                   v-model="hourly_rate"
                   placeholder="Hourly Rate"
                   required>
        </div>
        <div class="col-2">
            <button
                    name="task-add-submit"
                    type="submit"
                    class="btn btn-success btn-sm w-100"
                    v-on:click="submitTask">
                Add
            </button>
        </div>
    </form>

    <div class="task-rows rounded">
        <div v-for="task in tasks" class="row py-2 bg-faded rounded mb-2">
            <div class="col-8 d-flex align-items-center">
                <span class="font-weight-bold">{{ task.name }}</span>
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
                <span class="mb-1">${{ task.hourly_rate }}</span>
            </div>
            <div class="col-2">
                <button name="task-change"
                        class="btn btn-warning btn-sm w-100">
                    Edit
                </button>
            </div>
        </div>
    </div>
</div>
</template>


<script>
const Pager = require('./pager.vue');

export default {
    data() {
        return {
            tasks: null
        };
    },
    methods: {
        getTasks(url) {
            url = (typeof url !== 'undefined') ? url : timestrapConfig.API_URLS.TASKS;

            quickFetch(url).then(data => {
                this.tasks = data;
            }).catch(error => console.log(error));
        },
        submitTask() {
            console.log(this);
        },
    },
    mounted() {
        return this.getTasks();
    },
    components: {
        Pager
    }
};
</script>
