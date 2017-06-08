<template>
<select class="select2">
</select>
</template>


<script>
export default {
    props: ['options'],
    mounted: function () {
        $(this.$el)
        // init select2
            .select2({
                data: this.options,
            })
            .val(this.value)
            .trigger('change')
            .on('change', function (e) {
                this.$emit('select2-select', e.target.value);
            }.bind(this))
    },
    watch: {
        options: function (options) {
            $(this.$el).select2({ data: options })
        }
    },
    destroyed: function () {
        $(this.$el).off().select2('destroy')
    }
};
</script>
