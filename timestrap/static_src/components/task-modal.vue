<template>
<modal>
    <h5 slot="header">
        <i class="fa fa-tasks mr-1" aria-hidden="true"></i>
        {{ config.task ? 'Edit: ' + config.task.name : 'New Task' }}
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
        <button name="task-modal-cancel"
                type="button"
                class="btn btn-secondary"
                @click="$emit('close')">
            Close
        </button>
        <button name="task-modal-submit"
                type="submit"
                class="btn btn-primary"
                @click="submit">
            {{ config.task ? 'Save Changes' : 'Add Task' }}
        </button>
    </div>
</modal>
</template>

<script>
const Modal = require('./modal.vue');

export default {
    props: ['config'],
    data() {
        return {
            name: this.config.task ? this.config.task.name : null,
            hourly_rate: this.config.task ? this.config.task.hourly_rate : null
        };
    },
    methods: {
        submit() {
            let body = {
                name: this.name,
                hourly_rate: this.hourly_rate
            };
            let url = timestrapConfig.API_URLS.TASKS;
            let method = 'post';
            if (this.config.task) {
                url = this.config.task.url;
                method = 'put'
            }
            this.$quickFetch(url, method, body).then(data => {
                this.name = '';
                this.hourly_rate = '';
                this.$emit('updateTask', data, this.config.index);
                this.$emit('close');
            }).catch(error => console.log(error));
        }
    },
    components: {
        Modal
    }
};
</script>
