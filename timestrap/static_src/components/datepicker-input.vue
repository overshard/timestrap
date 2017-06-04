<template>
<input name="entry-date"
       type="text"
       class="form-control form-control-sm date-input"
       v-model="date"
       placeholder="Date" />
</template>


<script>
export default {
    mounted() {
        let vm = this;
        $(this.$el).pickadate({
            format: 'yyyy-mm-dd',
            onStart: function() {
                let currentDate = new Date();
                this.set('select', currentDate);
                vm.$emit('date-select', moment(currentDate).format('YYYY-MM-DD'));
            },
            onSet: function() {
                vm.$emit('date-select', $(vm.$el).val());
            }
        });
    }
};
</script>
