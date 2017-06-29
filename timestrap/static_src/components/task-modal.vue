<template>
<transition name="modal">
    <div class="modal-mask">
        <div class="modal-wrapper">
            <div class="modal-container">
                <form id="task-add"
                   class="modal-content"
                   v-on:submit.prevent
                   v-on:submit="submitTask">
                <div class="modal-header">
                    <slot name="header">
                        <h5 class="modal-title">
                        <i class="fa fa-tasks mr-1" aria-hidden="true"></i>
                        New Task
                        </h5>
                    </slot>
                </div>

                <div class="modal-body">
                    <slot name="body">
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
                    </slot>
                </div>

                <div class="modal-footer">
                    <slot name="footer">
                        <button name="task-add-cancel"
                                type="button"
                                class="btn btn-secondary"
                                @click="$emit('close')">
                            Close
                        </button>
                        <button name="task-add-submit"
                                type="submit"
                                class="btn btn-primary">
                            Add Task
                        </button>
                    </slot>
                </div>
                </form>
            </div>
        </div>
    </div>
</transition>
</template>

<script>
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
    }
};
</script>
