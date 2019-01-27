<template>
<div
  :id="[index ? 'card-' + index : '']"
  class="col-md-4 col-lg-3 mb-4"
  @dblclick="$emit('modal')">
  <div v-if="index !== null" class="card shadow-sm">
    <div v-if="delete_perm || change_perm" class="card-options">
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
          v-if="change_perm"
          @click.exact="$emit('modal')">
          Edit
        </button>
        <button
          id="card-menu-delete"
          class="dropdown-item"
          v-if="delete_perm"
          @click.exact="$emit('delete')">
          Delete
        </button>
      </div>
    </div>

    <div class="card-body">
      <slot name="card-body"/>
    </div>
  </div>
  <div v-else-if="add_perm" class="card new" @click="$emit('modal')">
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
    },
    delete_perm: {
      type: Object,
      default: null,
    },
    change_perm: {
      type: Object,
      default: null,
    },
    add_perm: {
      type: Object,
      default: null,
    },
  },
};
</script>


<style lang="scss" scoped>
.card {
  height: 15rem;
  cursor: pointer;
  -webkit-user-select: none;  // TODO: Not being added automatically?
  -moz-user-select: none;  // TODO: Not being added automatically?
  user-select: none;

  .card-options {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
  }

  .dropdown-toggle {
    opacity: 0;
    transition: opacity 300ms;
  }

  &:hover {
    background-color: #f8f9fa;

    .dropdown-toggle {
      opacity: 1;
    }
  }

  &.new {
    opacity: .5;
    transition: opacity 300ms, transform 300ms;

    &:hover, &.edit {
      opacity: 1;
    }
  }
}
</style>
