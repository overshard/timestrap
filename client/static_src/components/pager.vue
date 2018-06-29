<template>
  <div class="pull-right">
    <button
      v-if="previous"
      class="btn btn-primary btn-sm mr-1"
      @click="$emit('previous-page')">
      <i class="fa fa-arrow-left"/>
      Previous
    </button>

    <button
      v-if="next"
      class="btn btn-primary btn-sm"
      @click="$emit('next-page')">
      Next
      <i class="fa fa-arrow-right"/>
    </button>
  </div>
</template>


<script>
export default {
  props: [
    'next',
    'previous',
  ],
};
</script>
