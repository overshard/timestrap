<template>
<div class="task row py-2 bg-faded">

    <template v-if="edit && this.$perms.change_task">
    <div class="col-8">
        <input name="task-name"
               type="text"
               class="form-control form-control-sm"
               v-model.trim="name"
               v-on:keyup.enter="saveTask"
               required/>
    </div>
    <div class="col-2">
        <input name="task-hourly-rate"
               type="text"
               class="form-control form-control-sm"
               v-model.number="hourly_rate"
               v-on:keyup.enter="saveTask"
               required/>
    </div>
    <div class="col-2">
        <button name="task-save"
                class="btn btn-success btn-sm w-100"
                v-block-during-fetch
                v-on:click="saveTask">
            Save
        </button>
    </div>
    </template>

    <template v-else>
        <div v-bind:class="[[this.$perms.change_task ? 'col-8' : 'col-10'], 'd-flex', 'align-items-center']">
            {{ task.name }}
        </div>
        <div class="col-2 d-flex align-items-center">
            ${{ task.hourly_rate }}
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
                       v-on:click="editTask">
                        Edit
                    </a>
                    <a id="task-menu-delete"
                       class="dropdown-item"
                       href="#"
                       v-if="this.$perms.delete_task"
                       v-on:click.prevent
                       v-on:click="deleteTask">
                        Delete
                    </a>
                </div>
            </template>
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
        saveTask(e) {
            let body = {
                name: this.name,
                hourly_rate: this.hourly_rate
            };
            this.$quickFetch(this.task.url, 'put', body).then(data => {
                if (data.id) {
                    this.task.name = data.name;
                    this.task.hourly_rate = data.hourly_rate;
                    this.edit = false;
                }
            }).catch(error => console.log(error));
        },
        deleteTask() {
            this.$quickFetch(this.task.url, 'delete').then(function(response) {
                if (response.status === 204) {
                    $.growl.notice({ message: 'Task deleted!' });
                    this.$emit('delete-task');
                } else {
                    $.growl.error({ message: 'Task delete failed ):' });
                }
            }.bind(this));
        },
        appendTask(task) {
            this.tasks.unshift(task);
        }
    }
};
</script>
