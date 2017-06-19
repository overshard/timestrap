<template>
<div class="modal fade" id="newTaskModal">
    <div class="modal-dialog">
        <form name="task-add"
                class="modal-content"
                v-on:submit.prevent
                v-on:submit="submitTask">
            <div class="modal-header">
                <h5 class="modal-title">
                    <i class="fa fa-tasks mr-1" aria-hidden="true"></i>
                    New Task
                </h5>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <input name="task-name"
                           placeholder="Task Name"
                           type="text"
                           class="form-control"
                           v-model.trim="name"
                           required />
                </div>
                <div class="form-group">
                    <input name="task-hourly-rate"
                           placeholder="Hourly Rate"
                           type="text"
                           class="form-control"
                           v-model.number="hourly_rate"
                           required />
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">
                    Close
                </button>
                <button type="submit" class="btn btn-primary">
                    Add Task
                </button>
            </div>
        </form>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {};
    },
    methods: {
        submitTask() {
            let body = {
                name: this.name,
                hourly_rate: this.hourly_rate
            };
            this.$quickFetch(timestrapConfig.API_URLS.TASKS, 'post', body).then(data => {
                $('#newTaskModal').modal('hide');
                this.name = '';
                this.hourly_rate = '';
                this.$emit('appendTask', data);
            }).catch(error => console.log(error));
        }
    }
};
</script>
