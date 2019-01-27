<template>
  <div class="row chartjs-wrapper bg-secondary pt-4 pb-2">
    <canvas
      id="chartjs-1"
      class="chartjs"/>
  </div>
</template>


<script>
import Chart from 'chart.js';


export default {
  props: [
    'entries',
  ],
  data() {
    return {
      renderedChart: false,
    };
  },
  watch: {
    entries() {
      this.destroy();
      this.update();
    },
  },
  mounted() {
    this.update();
  },
  destroyed() {
    this.destroy();
  },
  methods: {
    update() {
      let chartDates = [];
      let chartDurations = [];
      let entryBlock;
      for (entryBlock in this.entries) {
        chartDates.push(this.$moment(this.entries[entryBlock].date).format('MMMM Do'));
        let entry;
        let totalTime = 0;
        for (entry in this.entries[entryBlock].entries) {
          totalTime = totalTime + this.entries[entryBlock].entries[entry].duration;
        }
        totalTime = Math.round(totalTime * 10) / 10;
        chartDurations.push(totalTime);
      }

      this.renderedChart = new Chart(document.getElementById('chartjs-1'), {
        type: 'bar',
        data: {
          labels: chartDates,
          datasets: [{
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
            ],
            borderColor: [
              'rgba(255,99,132,1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
            ],
            borderWidth: 1,
            data: chartDurations,
          }],
        },
        options: {
          maintainAspectRatio: false,
          legend: {
            display: false,
          },
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
                fontColor: 'rgba(255, 255, 255, 1)',
              },
              gridLines: {
                color: 'rgba(255, 255, 255, .2)',
                zeroLineColor: 'rgba(255, 255, 255, .6)',
              },
            }],
            xAxes: [{
              ticks: {
                fontColor: 'rgba(255, 255, 255, 1)',
              },
              gridLines: {
                color: 'rgba(255, 255, 255, .2)',
              },
            }],
          },
        },
      });
    },
    destroy() {
      if (this.renderedChart) this.renderedChart.destroy();
    },
  },
};
</script>


<style lang="scss" scoped>
.chartjs-wrapper {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/static/imgs/background.jpg');
  background-size: cover;
  background-position: center center;
  height: 250px;
}
</style>
