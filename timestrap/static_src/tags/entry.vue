<template>
<div class="row py-2 bg-faded small">
    <div class="col-sm-3 client-project">
        <div class="text-muted small">
            {{ project_details.client_details.name }}
        </div>
        {{ project_details.name }}
    </div>
    <div class="col-sm-5 d-flex flex-column align-self-end tasks">
        <div class="text-muted small"
                v-if="task">
            {{ task_details.name }}
        </div>
        {{ note }}
    </div>
    <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration">
        {{ duration }}
    </div>
</div>
</template>

<script>
export default {
    props: ['entry'],
    data() {
        return {
            project_details: this.entry.project_details,
            task: this.entry.task,
            task_details: this.entry.task_details,
            note: this.entry.note,
            duration: durationToString(this.entry.duration)
        };
    }
};
</script>
