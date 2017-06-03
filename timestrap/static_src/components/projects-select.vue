<template>
<select id="entry-project"
        class="project-select"
        v-model="project"
        required>
    <option><!-- select2 placeholder --></option>
    <optgroup v-for="client in clients" :label="client.name">
        <option v-for="project in client.projects"
                :value="project.url">
            {{ project.name }}
        </option>
    </optgroup>
</select>
</template>


<script>
const Vue = require('vue');

export default {
    props: ['selected'],
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
                Vue.nextTick(() => {
                    $(this.$el)
                        .select2({
                            placeholder: 'Project',
                            width: '100%',
                            dropdownAutoWidth: true
                        })
                        .val(this.selected)
                        .trigger('change')
                        .on('change', () => {
                            this.$emit('project-select', $(this.$el).val());
                        });
                });
            });
        }
    },
    mounted() {
        this.getClients();
    }
};
</script>
