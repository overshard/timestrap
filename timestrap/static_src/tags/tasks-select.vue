<template>
<select id="entry-task"
        class="task-select"
        v-model="task">
    <option v-for="task in tasks" :value="task.url">
        {{ task.name }}
    </option>
</select>
</template>


<script>
export default {
    data() {
        return {
            tasks: null
        };
    },
    methods: {
        getTasks() {
            let tasks = quickFetch(timestrapConfig.API_URLS.TASKS);
            tasks.then(data => {
                this.tasks = data;
                $('.task-select').select2({
                    placeholder: 'Task',
                    width: '100%',
                    dropdownAutoWidth: true
                }).on('change', () => {
                    this.$emit('task-select', $('.task-select').val());
                });
            });
        }
    },
    mounted() {
        this.getTasks();
    }
};
</script>
