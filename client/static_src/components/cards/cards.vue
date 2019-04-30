<template>
<div class="container-fluid">
  <div class="row row-background">
    <div class="col-md-7">
      <h1 class="cards-title">
        <slot name="cards-title"/>
      </h1>
    </div>
    <div class="col-md-5 d-flex align-items-end justify-content-end">
      <div class="form-control shadow-sm d-flex align-items-center">
        <icon :icon="['fas', 'search']" class="fa-sm mr-2"/>
        <input
          id="task-search"
          class="form-control-plaintext py-0 flex-grow-1"
          v-on:input="$emit('search', $event.target.value)"
          placeholder="Search"
          type="text"/>
      </div>
    </div>
  </div>

  <div class="row p-3">
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
    <slot name="cards-new"/>
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


<style lang="scss" scoped>
.row-background {
  background-image: url('/static/imgs/background.jpg');
  background-size: cover;
  background-position: center center;
  padding-top: 3rem;
  padding-bottom: 3rem;
  margin-bottom: 15px;
}

.cards-title {
  margin-bottom: 0;
  color: #fff;
  text-shadow: 1px 1px 0 #000;
  font-weight: bold;

  .fa-sm {
    filter: drop-shadow(1px 1px 0 #000);
  }
}

.form-control {
  border: none;
  opacity: .75;
  width: 200px;
  transition: opacity 300ms, width 300ms;

  &:focus-within {
    opacity: 1;
    width: 100%;
  }
}
</style>
