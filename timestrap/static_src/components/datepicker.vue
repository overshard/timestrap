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
                if (vm.default) {
                    this.set('select', vm.default);
                    vm.$emit('datepicker-select', moment(vm.default).format('YYYY-MM-DD'));
                }
            },
            onSet: function() {
                vm.$emit('datepicker-select', $(vm.$el).val());
            }
        });
    }
};
</script>
