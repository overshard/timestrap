<template>
<div class="modal" data-keyboard="false">
  <div class="modal-dialog modal-lg modal-dialog-centered">
    <form @submit.prevent="submit" class="modal-content border-0 shadow">
      <div class="modal-body">
        <slot name="modal-body"/>
        <button
          id="modal-submit"
          class="btn btn-lg btn-dark shadow-sm mt-5"
          type="submit">
          Save
        </button>
      </div>
    </form>
  </div>
</div>
</template>


<script>
import $ from 'jquery';


export default {
  props: [
    'edit',
    'create',
    'data',
  ],
  methods: {
    submit() {
      if (this.data.id) this.edit(this.data);
      else this.create(this.data);
      $(this.$el).modal('hide');
    },
  },
  mounted() {
    $(this.$el).modal('show');
    $(this.$el).on('hidden.bs.modal', function() {
      this.$emit('close');
    }.bind(this));
  },
};
</script>


<style lang="scss" scoped>
.modal-body {
  padding: 4rem;
}

.form-control-title {
  font-size: 2rem;
  font-weight: bold;
}
</style>
