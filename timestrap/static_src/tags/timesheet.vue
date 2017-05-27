<template>
<div class="content">
    <div class="container">
        <div v-for="entry in entries">
            {{ entry.id }} {{ entry.note }}
        </div>
    </div>
</div>
</template>

<script>
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
    }
}
</script>
