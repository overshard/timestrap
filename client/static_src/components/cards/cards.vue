<template>
<div class="container my-4">
  <div class="row mb-4">
    <div class="col-md-7">
      <h1 class="mb-0 font-weight-bold">
        <slot name="cards-title"/>
      </h1>
    </div>
    <div class="col-md-5 d-flex flex-column align-items-end justify-content-center">
      <input
        id="task-search"
        v-on:input="$emit('search', $event.target.value)"
        placeholder="Type to filter..."
        class="form-control shadow-sm"
        type="text">
    </div>
  </div>

  <div class="row">
    <template v-if="numberOfElements !== 0 && view_perm">
      <slot name="cards-list"/>
    </template>
    <template v-else>
      <div class="col-mb-4 col-lg-3 mb-4">
        <div class="task card shadow-sm border-danger" style="height: 15rem;">
          <div class="card-body">
            <div class="card-title h5 font-weight-bold">
              Nothing here
            </div>
            <div class="card-subtitle h6 text-muted mb-2">
              Nothing matched your filter or has been added yet
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>

  <slot name="cards-modal"/>
</div>
</template>


<script>
export default {
  props: {
    numberOfElements: {
      type: Number,
      default: 0,
    },
    view_perm: {
      type: Object,
      default: null,
    }
  },
}
</script>
