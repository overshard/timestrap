<template>
<select class="select2">
</select>
</template>


<script>
export default {
    props: ['options', 'selected'],
    mounted: function () {
        $(this.$el)
            .select2({
                data: this.options,
                width: '100%',
                dropdownAutoWidth: true
            })
            .val(this.selected)
            .trigger('change')
            .on('change', function (e) {
                this.$emit('select2-select', e.target.value);
            }.bind(this));
    },
    watch: {
        options: function (options) {
            $(this.$el).select2({ data: options });
        }
    },
    destroyed: function () {
        $(this.$el).off().select2('destroy');
    }
};
</script>
