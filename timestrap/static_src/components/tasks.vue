<template>
<div class="container">
    <div v-if="this.$perms.add_task" class="row py-2 mb-4 bg-faded rounded">
        <div class="col-12">
            <button name="task-add"
                    type="button"
                    class="btn btn-primary btn-sm"
                    data-toggle="modal"
                    data-target="#new-task-modal"
                    v-if="this.$perms.add_task">
                <i class="fa fa-plus mr-1" aria-hidden="true"></i>
                New Task
            </button>
        </div>
    </div>

    <new-task @appendTask="appendTask" v-if="this.$perms.add_task"></new-task>

    <div v-if="this.$perms.view_task" id="task-rows" class="rounded">
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
const NewTask = require('./new-task.vue');

export default {
    data() {
        return {
            tasks: null
        };
    },
    methods: {
        getTasks(url) {
            url = (typeof url !== 'undefined') ? url : timestrapConfig.API_URLS.TASKS;

            this.$quickFetch(url).then(data => {
                this.tasks = data;
            }).catch(error => console.log(error));
        },
        appendTask(task) {
            this.tasks.unshift(task);
        }
    },
    mounted() {
        return this.getTasks();
    },
    components: {
        Task,
        NewTask
    }
};
</script>
