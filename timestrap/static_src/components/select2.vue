<template>
<select class="select2">
    <slot></slot>
</select>
</template>


<script>
export default {
    props: ['options', 'selected', 'placeholder'],
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
            $(this.$el)
                .select2({
                    data: this.options,
                    placeholder: this.placeholder,
                    width: '100%',
                    dropdownAutoWidth: true,
                    allowClear: true
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
