<template>
  <div class="row mb-4">
    <div class="col-md-7">
      <h1 class="mb-0">
        <icon :icon="['fas', 'briefcase']" class="text-muted mr-2"/>
        Projects
      </h1>
    </div>
    <div class="col-md-5 d-flex flex-column align-items-end justify-content-center">
      <input
        id="task-search"
        v-model="search"
        placeholder="Type to filter projects..."
        class="form-control shadow-sm"
        type="text">
    </div>
  </div>
</template>


<script>
import {mapGetters, mapActions} from 'vuex';


export default {
  data() {
    return {
      search: '',
    };
  },
};
</script>
