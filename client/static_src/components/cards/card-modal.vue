<template>
<div class="modal">
  <div class="modal-dialog modal-dialog-centered">
    <form @submit.prevent="submit" class="modal-content border-0 shadow">
      <div class="modal-body">
        <slot name="modal-body"/>
      </div>
      <div class="modal-footer">
        <button
          id="modal-submit"
          class="btn btn-success shadow-sm"
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
