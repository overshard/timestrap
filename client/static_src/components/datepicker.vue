<template>
  <input class="datepicker" >
</template>


<script>
import $ from 'jquery';

import 'picker';
import 'picker-date';

import 'pickadate/lib/themes/default.css';
import 'pickadate/lib/themes/default.date.css';


export default {
  props: [
    'default',
  ],
  mounted() {
    let vm = this;
    $(this.$el).pickadate({
      format: 'yyyy-mm-dd',
      onStart: function() {
        $('.picker').appendTo('body');
        if (vm.default) {
          this.set('select', vm.default);
          vm.$emit('input', vm.$moment(vm.default).format('YYYY-MM-DD'));
        }
      },
      onSet: function() {
        vm.$emit('input', $(vm.$el).val());
      },
    });
  },
  destroyed() {
    $(this.$el).stop();
  },
};
</script>
