<template>
<select id="entry-project"
        class="project-select"
        v-model="project"
        required>
    <option><!-- select2 placeholder --></option>
    <optgroup v-for="client in clients" :label="client.name">
        <option v-for="project in client.projects" :value="project.url">
            {{ project.name }}
        </option>
    </optgroup>
</select>
</template>


<script>
export default {
    data() {
        return {
            clients: null
        };
    },
    methods: {
        getClients() {
            let clients = quickFetch(timestrapConfig.API_URLS.CLIENTS);
            clients.then(data => {
                this.clients = data;
                $('.project-select').select2({
                    placeholder: 'Project',
                    width: '100%',
                    dropdownAutoWidth: true
                }).on('change', () => {
                    this.$emit('project-select', $('.project-select').val());
                });
            });
        }
    },
    mounted() {
        this.getClients();
    }
};
</script>
