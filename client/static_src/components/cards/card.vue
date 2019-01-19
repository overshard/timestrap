<template>
<div :id="[index ? 'card-' + index : '']" class="col-md-4 col-lg-3 mb-4">
  <div v-if="index !== null" class="card shadow-sm">
    <div class="card-body">
      <div class="float-right ml-2">
        <button
          id="card-menu"
          class="btn btn-light btn-sm btn-icon shadow-sm dropdown-toggle text-muted"
          type="button"
          data-toggle="dropdown">
          <icon :icon="['fas', 'ellipsis-h']"/>
        </button>
        <div class="dropdown-menu dropdown-menu-right shadow">
          <button
            id="card-menu-change"
            class="dropdown-item"
            @click.exact="$emit('modal')">
            Edit
          </button>
          <button
            id="card-menu-delete"
            class="dropdown-item"
            @click.exact="$emit('delete')">
            Delete
          </button>
        </div>
      </div>

      <slot name="card-body"/>
    </div>
  </div>
  <div v-else class="card new" @click="$emit('modal')">
    <div class="card-body d-flex justify-content-center align-items-center">
      <div class="text-muted">
        <icon :icon="['fas', 'plus']" class="mr-1"/>
        New
      </div>
    </div>
  </div>
</div>
</template>


<script>
export default {
  data() {
    return {
      modal: false,
    }
  },
  props: {
    index: {
      type: Number,
      default: null,
    }
  },
};
</script>


<style lang="scss">
.card {
  height: 15rem;

  &.new {
    cursor: pointer;
    opacity: .7;
    transition: opacity 300ms, transform 300ms;

    &:hover, &.edit {
      opacity: 1;
    }
  }
}
</style>
