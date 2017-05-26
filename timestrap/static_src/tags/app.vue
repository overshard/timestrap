<template>
<div class="content">
    <navigation></navigation>
    <div class="container">
        <div v-for="entry in entries">
            {{ entry.id }} {{ entry.note }}
        </div>
    </div>
</div>
</template>

<script>
import navigation from './navigation.vue';

export default {
    data() {
        return {
            entries: null
        }
    },
    methods: {
        getEntries(url) {
            let userEntries = timestrapConfig.API_URLS.ENTRIES + '?user=' + timestrapConfig.USER.ID;
            url = (typeof url !== 'undefined') ? url : userEntries;

            let entries = quickFetch(url);

            entries.then(data => {
                this.entries = data.results;
            });

            return this.entries;
        }
    },
    mounted() {
        return this.getEntries();
    },
    components: {
        navigation
    }
}
</script>
