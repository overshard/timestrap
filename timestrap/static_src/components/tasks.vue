<template>
<div class="container">
    <div v-if="this.$perms.add_task" class="row py-2 mb-4 bg-faded rounded">
        <div class="col-12">
            <button name="task-add"
                    type="button"
                    class="btn btn-primary btn-sm"
                    @click="toggleModal"
                    v-if="this.$perms.add_task">
                <i class="fa fa-plus mr-1" aria-hidden="true"></i>
                New Task
            </button>
        </div>
    </div>

    <task-modal @appendTask="appendTask"
                @close="toggleModal"
                v-if="show_modal && (this.$perms.add_task || this.$perms.change_task)"></task-modal>

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
const TaskModal = require('./task-modal.vue');

export default {
    data() {
        return {
            tasks: null,
            show_modal: false
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
        },
        toggleModal() {
            this.show_modal = !this.show_modal;
        }
    },
    mounted() {
        return this.getTasks();
    },
    components: {
        Task,
        TaskModal
    }
};
</script>
