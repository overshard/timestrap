<template>
<div class="container">
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
          v-on:submit.prevent
          v-on:submit="submitTask">
        <div class="col-8">
            <input name="task-name"
                   type="text"
                   class="form-control form-control-sm"
                   v-model.trim="name"
                   placeholder="New Task Name"
                   required/>
        </div>
        <div class="col-2">
            <input name="task-hourly-rate"
                   type="text"
                   class="form-control form-control-sm"
                   v-model.number="hourly_rate"
                   placeholder="Hourly Rate"
                   required/>
        </div>
        <div class="col-2">
            <button
                    name="task-add-submit"
                    type="submit"
                    class="btn btn-success btn-sm w-100">
                Add
            </button>
        </div>
    </form>

    <div class="task-rows rounded">
        <task v-for="(task, index) in tasks"
            v-bind:task="task"
            v-bind:index="index"
            v-bind:key="task.id">
        </task>
    </div>
</div>
</template>


<script>
const Task = require('./task.vue');

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
            let body = {
                name: this.name,
                hourly_rate: this.hourly_rate
            };
            quickFetch(timestrapConfig.API_URLS.TASKS, 'post', body).then(data => {
                this.name = '';
                this.hourly_rate = '';
                this.tasks.unshift(data);
            }).catch(error => console.log(error));
        },
    },
    mounted() {
        return this.getTasks();
    },
    components: {
        Task
    }
};
</script>
