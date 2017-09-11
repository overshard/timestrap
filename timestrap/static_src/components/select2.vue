<template>
<select class="select2">
    <slot></slot>
</select>
</template>


<script>
export default {
    props: ['options', 'selected', 'placeholder', 'allowclear'],
    mounted() {
        this.update();
    },
    watch: {
        options: function () {
            this.update();
        },
    },
    methods: {
        update() {
            if (this.allowclear == 'true') {
                this.allowclear = true;
            } else {
                this.allowclear = false;
            }
            $(this.$el)
                .select2({
                    data: this.options,
                    placeholder: this.placeholder,
                    width: '100%',
                    dropdownAutoWidth: true,
                    allowClear: this.allowclear
                })
                .val(this.selected)
                .trigger('change')
                .on('change', function (e) {
                    this.$emit('input', e.target.value);
                }.bind(this));
        }
    },
    destroyed() {
        $(this.$el).off().select2('destroy');
    }
};
</script>
