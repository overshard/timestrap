<template>
<div class="popover__container">
  <div
    class="focuser"
    v-if="show"
    @click="popoverHide()"/>

  <button
    class="btn btn-light popover__button w-100 text-nowrap"
    @click="popoverShow()">
    <slot name="popover-button"/>
  </button>

  <div :class="['popover__content', 'bg-white', 'border', 'rounded', 'p-4', show ? 'd-block' : 'd-none']">
    <slot name="popover-content"/>
  </div>
</div>
</template>


<script>
export default {
  data() {
    return {
      show: false,
    }
  },
  methods: {
    popoverShow() {
      this.show = true;
    },
    popoverHide() {
      this.show = false;
    },
  },
};
</script>


<style lang="scss">
.focuser {
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}

.popover__container {
  position: relative;
}

.popover__content {
  position: absolute;
  z-index: 2;
  width: 400px;
  margin-top: 0.5rem;
  right: 0;
  left: auto;
}
</style>
