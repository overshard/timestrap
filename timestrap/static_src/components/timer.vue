<template>
<div id="timer" class="text-center">
    <div v-if="entry" class="small">
        <div v-if="entry.project_details" class="text-muted">{{ entry.project_details.client_details.name }}</div>
        <div v-if="entry.project_details">{{ entry.project_details.name }}</div>
        <div v-if="entry.task_details" class="text-muted">{{ entry.task_details.name }}</div>
    </div>
    <div id="timer-value"
         v-bind:class="['h2', [this.running ? 'text-success' : '']]">
        {{ hours }}:{{ minutes }}:{{ seconds }}
    </div>
    <div class="btn-group btn-group-sm" role="group">
        <button id="timer-start"
                class="btn btn-success"
                v-if="!this.running"
                v-on:click="toggle">Start</button>
        <button id="timer-stop"
                class="btn btn-success"
                v-if="this.running"
                v-on:click="toggle">Stop</button>
        <button id="timer-entry-save"
                class="btn btn-primary"
                v-if="!this.running && entry"
                v-on:click="saveEntry">Save</button>
        <button id="timer-reset"
                class="btn btn-danger"
                v-on:click="reset"
                v-bind:disabled="this.total === 0">Reset</button>
    </div>
</div>
</template>


<script>
export default {
    data() {
        return {
            running: false,
            total: 0,
            hours: '00',
            minutes: '00',
            seconds: '00',
            entry: false
        };
    },
    methods: {
        tick: function() {
            ++this.total;
            this.hours = pad(Math.floor(this.total / 3600));
            this.minutes = pad(Math.floor(this.total % 3600 / 60));
            this.seconds = pad(this.total % 3600 % 60);
        },
        toggle: function() {
            this.running = !this.running;
            if (this.running) {
                this.hours = pad(Math.floor(this.total / 3600));
                this.minutes = pad(Math.floor(this.total % 3600 / 60));
                this.seconds = pad(this.total % 3600 % 60);
                this.interval = setInterval(this.tick, 1000, this);
            }
            else {
                clearInterval(this.interval);
            }
        },
        reset: function() {
            // TODO: Add some sort of warning/option to cancel.
            if (this.running) {
                this.toggle();
            }
            this.total = 0;
            this.offset = 0;
            this.hours = '00';
            this.minutes = '00';
            this.seconds = '00';
            this.entry = false;
        },
        saveEntry(e) {
            toggleButtonBusy(e.target);
            let body = {
                user: this.entry.user,
                project: this.entry.project,
                note: this.entry.note,
                duration: secondsToDurationString(this.total)
            };
            this.$quickFetch(this.entry.url, 'put', body).then(data => {
                if (data.id) {
                    $.growl.notice({ message: 'New entry duration saved!' });
                    this.reset();
                }
                toggleButtonBusy(e.target);
            }).catch(error => console.log(error));
        },
    },
    created() {
        this.bus.$on('timerToggle', function(entry) {
            if (this.running) {
                // TODO: Add some sort of warning/option to cancel.
                this.toggle();
            }
            if (entry) {
                this.entry = entry;
                // Entry's duration should be in _decimal_ format.
                if (entry.duration && typeof entry.duration === 'number') {
                    this.total = durationToSeconds(entry.duration);
                }
            }
            this.toggle();
        }.bind(this));
    }
};
</script>
