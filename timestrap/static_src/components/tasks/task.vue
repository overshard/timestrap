<template>
<div class="task row bg-light py-1">
    <div v-bind:class="[[this.$perms.change_task ? 'col-8' : 'col-10'], 'd-flex', 'align-items-center']">
        <i class="fa fa-tasks text-muted mr-2" aria-hidden="true"></i>
        {{ task.name }}
    </div>
    <div class="col-2 d-flex align-items-center">
        <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
        <template v-if="task.hourly_rate">
            ${{ task.hourly_rate }}
        </template>
        <template v-else>
            Not set
        </template>
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end">
        <template v-if="this.$perms.change_task || this.$perms.delete_task">
            <button name="task-menu"
                    class="btn btn-faded btn-sm btn-icon dropdown-toggle"
                    type="button"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false">
                <i class="fa fa-ellipsis-v" aria-hidden="true"></i>
            </button>
            <div class="dropdown-menu dropdown-menu-right"
                    aria-labelledby="task-menu">
                <a id="task-menu-change"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.change_task"
                   v-on:click.prevent
                   v-on:click="toggleEditModal(task, index)">
                    Edit
                </a>
                <a id="task-menu-delete"
                   class="dropdown-item"
                   href="#"
                   v-if="this.$perms.delete_task"
                   v-on:click.prevent
                   v-on:click="deleteTask(index)">
                    Delete
                </a>
            </div>
        </template>
    </div>
</div>
</template>

<script>
export default {
    props: ['task', 'index', 'key', 'toggleEditModal'],
    data() {
        return {
            edit: false,
            name: this.task.name,
            hourly_rate: this.task.hourly_rate
        };
    },
    methods: {
        deleteTask() {
            this.$quickFetch(this.task.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    $.growl.notice({ message: 'Task deleted!' });
                    this.$emit('removeTask', this.index);
                } else {
                    $.growl.error({ message: 'Task delete failed ):' });
                }
            }.bind(this));
        }
    }
};
</script>
