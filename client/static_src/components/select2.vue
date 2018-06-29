<template>
  <select class="select2">
    <slot/>
  </select>
</template>


<script>
export default {
  props: [
    'options',
    'selected',
    'placeholder',
    'allowclear',
  ],
  watch: {
    options: function () {
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
      $(this.$el)
        .select2({
          data: this.options,
          placeholder: this.placeholder,
          width: '100%',
          dropdownAutoWidth: true,
          allowClear: this.allowclear !== undefined ? true : false,
        })
        .val(this.selected)
        .trigger('change')
        .on('change', function (e) {
          this.$emit('input', e.target.value);
        }.bind(this));
    },
    destroy() {
      $(this.$el).off().select2('destroy');
      $(this.$el).empty();
    },
  },
};
</script>


<style lang="scss">
.select2-container--default .select2-selection--single {
  border: 1px solid #d2d2d2;
  height: 31px;
}

.select2-container--default .select2-selection--single .select2-selection__rendered {
  line-height: 28px;
  font-size: .875rem;
}

.select2-container--default .select2-selection--single .select2-selection__placeholder {
  color: #636c72;
}

.select2-container--default .select2-selection--single .select2-selection__arrow {
  height: 31px;
}
</style>
