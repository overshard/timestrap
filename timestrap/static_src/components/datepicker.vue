<template>
<input class="datepicker" />
</template>


<script>
export default {
    props: ['default'],
    mounted() {
        let vm = this;
        $(this.$el).pickadate({
            format: 'yyyy-mm-dd',
            onStart: function() {
                let defaultDate = new Date();
                if (vm.default) {
                    defaultDate = vm.default;
                }
                this.set('select', defaultDate);
                vm.$emit('datepicker-select', moment(defaultDate).format('YYYY-MM-DD'));
            },
            onSet: function() {
                vm.$emit('datepicker-select', $(vm.$el).val());
            }
        });
    }
};
</script>
