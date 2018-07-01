<template>
  <div class="float-right">
    <button
      v-if="previous"
      class="btn btn-primary btn-sm mr-1"
      @click="$emit('previous-page')">
      <icon
        :icon="['fas', 'arrow-left']"
        class="mr-1"/>
      Previous
    </button>

    <button
      v-if="next"
      class="btn btn-primary btn-sm"
      @click="$emit('next-page')">
      Next
      <icon
        :icon="['fas', 'arrow-right']"
        class="mr-1"/>
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
