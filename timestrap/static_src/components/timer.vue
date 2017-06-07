<template>
<div id="timer">
    <span id="timer-hours">{{ hours }}</span> :
    <span id="timer-minutes">{{ minutes }}</span> :
    <span id="timer-seconds">{{ seconds }}</span>

    <div class="btn-group btn-group-sm" role="group">
        <button id="timer-start"
                class="btn btn-success"
                v-on:click="toggle"
                v-bind:disabled="this.running">Start</button>
        <button id="timer-stop"
                class="btn btn-success"
                v-on:click="toggle"
                v-bind:disabled="!this.running">Stop</button>
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
        };
    },
    mounted() {
        this.bus.$on('toggleTimer', () => {
            this.toggle();
        });
    },
    methods: {
        tick: function () {
            ++this.total;
            this.hours = pad(Math.floor(this.total / 3600));
            this.minutes = pad(Math.floor(this.total % 3600 / 60));
            this.seconds = pad(this.total % 3600 % 60);
        },
        toggle: function () {
            this.running = !this.running;
            if (this.running) {
                this.interval = setInterval(this.tick, 1000, this);
            }
            else {
                clearInterval(this.interval);
            }
        },
        reset: function() {
            this.total = 0;
            this.hours = '00';
            this.minutes = '00';
            this.seconds = '00';
        }
    }
}
</script>
