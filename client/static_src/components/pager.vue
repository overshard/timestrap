<template>
<div class="pull-right">
    <button class="btn btn-primary btn-sm mr-1"
            v-if="previous" @click="$emit('previous-page')">
        <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
    </button>

    <button class="btn btn-primary btn-sm"
            v-if="next" @click="$emit('next-page')">
        Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
    </button>
</div>
</template>


<script>
export default {
    props: [
        'next',
        'previous'
    ]
};
</script>
