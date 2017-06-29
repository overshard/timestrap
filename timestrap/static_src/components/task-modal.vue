<template>
<modal>
    <h5 slot="header">
        <i class="fa fa-tasks mr-1" aria-hidden="true"></i>New Task
    </h5>

    <div slot="body">
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

    <div slot="footer">
        <button name="task-add-cancel"
                type="button"
                class="btn btn-secondary"
                @click="$emit('close')">
            Close
        </button>
        <button name="task-add-submit"
                type="submit"
                class="btn btn-primary"
                @click="submitTask">
            Add Task
        </button>
    </div>
</modal>
</template>

<script>
const Modal = require('./modal.vue');

export default {
    props: ['task'],
    data() {
        return {
            name: null,
            hourly_rate: null
        };
    },
    methods: {
        submitTask() {
            let body = {
                name: this.name,
                hourly_rate: this.hourly_rate
            };
            this.$quickFetch(timestrapConfig.API_URLS.TASKS, 'post', body).then(data => {
                this.name = '';
                this.hourly_rate = '';
                this.$emit('appendTask', data);
                this.$emit('close');
            }).catch(error => console.log(error));
        }
    },
    components: {
        Modal
    }
};
</script>
