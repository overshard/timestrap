<template>
<div class="task row py-2 bg-faded rounded mb-2">

    <template v-if="edit && global.perms.change_task">
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
                v-on:click="saveTask">
            Save
        </button>
    </div>
    </template>

    <template v-else>
    <div v-bind:class="[[global.perms.change_task ? 'col-8' : 'col-10'], 'd-flex', 'align-items-center']">
        <span class="font-weight-bold">{{ task.name }}</span>
    </div>
    <div class="col-2 d-flex align-items-center">
        <i class="fa fa-clock-o text-muted mr-2" aria-hidden="true"></i>
        <span class="mb-1">${{ task.hourly_rate }}</span>
    </div>
    <div class="col-2" v-if="global.perms.change_task">
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
            let body = {
                name: this.name,
                hourly_rate: this.hourly_rate
            };
            quickFetch(this.task.url, 'put', body).then(data => {
                if (data.id) {
                    this.task.name = data.name;
                    this.task.hourly_rate = data.hourly_rate;
                    this.edit = false;
                }
            }).catch(error => console.log(error));
        },
    }
};
</script>
