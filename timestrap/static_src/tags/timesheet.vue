<template>
<div class="container">
    <div class="row py-2 mb-4 bg-faded rounded">
        <div class="col-12">
            <router-link to="/reports/" class="btn btn-primary btn-sm">
                <i class="fa fa-book" aria-hidden="true"></i>
                Create Reports
            </router-link>
        </div>
    </div>

    <div class="row py-1 bg-inverse text-white font-weight-bold rounded-top">
        <div class="col-sm-3 mb-2">
            Date
        </div>
        <div class="col-sm-3 mb-2">
            Task
        </div>
        <div class="col-sm-6">
        </div>
        <div class="col-sm-3">
            Project
        </div>
        <div class="col-sm-5">
            Note
        </div>
        <div class="col-sm-2">
            Duration
        </div>
        <div class="col-sm-2">
        </div>
    </div>


    <form name="entry-add"
          class="row mb-4 py-2 bg-faded rounded-bottom"
          v-on:submit.prevent="onSubmit"
          v-on:submit="submitEntry">
        <div class="col-sm-3 mb-2">
            <input name="entry-date"
                   type="text"
                   class="form-control form-control-sm date-input"
                   v-model="date"
                   placeholder="Date" />
        </div>
        <div class="col-sm-3">
            <select id="entry-task"
                    class="task-select"
                    v-model="task">
            </select>
        </div>
        <div class="col-sm-6">
        </div>
        <div class="col-sm-3">
            <select id="entry-project"
                    class="project-select"
                    v-model="project"
                    required>
            </select>
        </div>
        <div class="col-sm-5">
            <input name="entry-note"
                   type="text"
                   class="form-control form-control-sm"
                   v-model="note"
                   placeholder="Note" />
        </div>
        <div class="col-sm-2">
            <input name="entry-duration"
                   type="text"
                   class="form-control form-control-sm text-right font-weight-bold"
                   v-model="duration"
                   placeholder="0:00"
                   required />
        </div>
        <div class="col-sm-2">
            <button name="entry-add-submit"
                    type="submit"
                    class="btn btn-success btn-sm w-100"
                    v-on:click="submitEntry">
                Add
            </button>
        </div>
    </form>


    <div class="mb-4">
        <div class="entry-rows rounded">
            <div v-for="entry in entries" class="row py-2 bg-faded small">
                <div class="col-sm-3 client-project">
                    <div class="text-muted small">
                        {{ entry.project_details.client_details.name }}
                    </div>
                    {{ entry.project_details.name }}
                </div>
                <div class="col-sm-5 d-flex flex-column align-self-end tasks">
                    <div class="text-muted small"
                         v-if="entry.task">
                        {{ task_details.name }}
                    </div>
                    {{ entry.note }}
                </div>
                <div class="col-sm-2 d-flex align-self-center justify-content-end display-4 duration">
                    {{ entry.duration }}
                </div>
            </div>
        </div>
    </div>

    <div class="row bg-success text-white py-2 mb-4 rounded">
        <div class="offset-sm-6 col-sm-2 text-right">
            Subtotal<br>
            <strong>Total</strong>
        </div>
        <div class="col-sm-2 text-right">
            {{ subtotal }}<br>
            <strong>{{ total }}</strong>
        </div>
    </div>
</div>
</template>


<script>
export default {
    data() {
        return {
            entries: null,
            subtotal: null,
            total: null
        };
    },
    methods: {
        getEntries(url) {
            let userEntries = timestrapConfig.API_URLS.ENTRIES + '?user=' + timestrapConfig.USER.ID;
            url = (typeof url !== 'undefined') ? url : userEntries;

            let entries = quickFetch(url);

            entries.then(data => {
                let entries = data.results.map(entry => {
                    entry.duration = durationToString(entry.duration);
                    return entry;
                });

                this.entries = entries;
                this.subtotal = durationToString(data.subtotal_duration);
                this.total = durationToString(data.total_duration);
            });

            return this.entries;
        },
        submitEntry() {
            console.log(this.note);
            console.log(this.date);
            console.log(this.project);
            console.log(this.duration);
        }
    },
    mounted() {
        return this.getEntries();
    }
};
</script>
