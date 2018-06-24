<template>
<div class="container">
    <div v-if="this.$perms.add_task" class="row py-2 mb-4 bg-light rounded">
        <div class="col-12">
            <button name="task-add"
                    type="button"
                    class="btn btn-primary btn-sm"
                    @click="toggleModal"
                    v-if="this.$perms.add_task">
                <i class="fa fa-plus mr-1" aria-hidden="true"></i>
                New Task
            </button>

            <button class="btn btn-secondary btn-sm pull-right ml-2"
                    v-on:click.prevent
                    v-block-during-fetch
                    v-on:click="refresh">
                <i class="fa fa-refresh" aria-hidden="true"></i> Refresh
            </button>
        </div>
    </div>

    <div v-show="loading" class="container text-center py-4">
        <i class="fa fa-spinner text-primary fa-spin display-3 text-center"></i>
    </div>

    <task-modal id="task-modal"
                v-if="modal_config.show && (this.$perms.add_task || this.$perms.change_task)"
                @updateTask="updateTask"
                @close="toggleModal"
                v-bind:config="modal_config"></task-modal>

    <div v-if="this.$perms.view_task" id="task-rows" class="rounded">
        <div class="task-head bg-secondary text-white row py-2">
            <div class="col-8 d-flex align-items-center">
                <i class="fa fa-tasks mr-2" aria-hidden="true"></i>
                <strong>Task Name</strong>
            </div>
            <div class="col-2 d-flex align-items-center">
                <i class="fa fa-clock-o mr-2" aria-hidden="true"></i>
                <strong>Hourly Rate</strong>
            </div>
            <div class="col-2"></div>
        </div>
        <task v-for="(task, index) in tasks"
              @removeTask="removeTask"
              v-bind:task="task"
              v-bind:index="index"
              v-bind:key="task.id"
              v-bind:toggleEditModal="toggleModal"></task>
    </div>
</div>
</template>


<script>
import { mapState, mapActions } from 'vuex';

import Task from './task.vue';
import TaskModal from './task-modal.vue';

export default {
    data() {
        return {
            modal_config: {
                index: null,
                task: null,
                show: false,
            },
        };
    },
    computed: {
        ...mapState([
            'loading',
            'tasks',
        ]),
    },
    methods: {
        ...mapActions([
            'getTasks',
        ]),
        updateTask(task, index) {
            if (task && (index || index === 0)) {
                this.tasks[index] = task;
            }
            else {
                this.tasks.unshift(task);
            }
            this.modal_config.index = null;
            this.modal_config.task = null;
        },
        removeTask(index) {
            this.tasks.splice(1, index);
        },
        toggleModal(task, index) {
            if (task && (index || index === 0)) {
                this.modal_config.task = task;
                this.modal_config.index = index;
            } else {
                this.modal_config.task = null;
                this.modal_config.index = null;
            }
            this.modal_config.show = !this.modal_config.show;
        },
        refresh() {
            this.getTasks();
        }
    },
    mounted() {
        this.getTasks();
    },
    components: {
        Task,
        TaskModal,
    }
};
</script>


<style lang="scss">
#task-rows {
    .task {
        font-size: .9em;
        border-top: 1px solid #eee;

        &:not(.bg-secondary) {
            &:nth-of-type(2n+1) {
                background-color: #fbf3e5 !important;
            }
        }

        &:last-child {
            border-bottom: 1px solid #eee;
            margin-bottom: 1rem;
        }
    }
}
</style>
