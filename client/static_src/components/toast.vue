<template>
<div class="toast float-right" role="alert" aria-live="assertive" aria-atomic="true" data-delay="5000">
  <div class="toast-header">
    <strong class="mr-auto">{{ toast.title }}</strong>
    <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
  <div class="toast-body">
    {{ toast.message }}
  </div>
</div>
</template>


<script>
import $ from 'jquery';


export default {
  data() {
    return {
      toast: {
        title: null,
        message: null,
      }
    }
  },
  mounted() {
    const self = this;
    this.$bus.$on('toast', function(data) {
      self.toast = data;
      setTimeout(function() {
        $(self.$el).toast('show');
      }, 2000);
    })
  },
};
</script>


<style lang="scss">
.toast {
  position: absolute;
  top: 25px;
  right: 25px;
  z-index: 100;
}
</style>
