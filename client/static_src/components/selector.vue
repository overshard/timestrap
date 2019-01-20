<template>
<div class="selector">
  <div
    class="focuser"
    v-if="edit"
    @click="toggleEdit()"/>

  <div
    class="select border shadow rounded w-100"
    v-if="edit"
    @keydown.esc.prevent="toggleEdit()"
    @keydown.tab.prevent="toggleEdit()"
    @keydown.up.prevent="selectedUp()"
    @keydown.down.prevent="selectedDown()"
    @keydown.enter.prevent="activeUpdate()">
    <div class="form-control d-flex rounded-0 border-0 rounded-top bg-light">
      <span class="badge badge-dark d-block-inline mr-2">
        {{ selectedObject.text }}
      </span>
      <input
        type="text"
        v-model="search"
        ref="search"
        class="form-control-plaintext flex-fill"
        placeholder="Type to filter...">
    </div>
    <div class="options list-group list-group-flush w-100 shadow">
      <template v-if="optionsFiltered(search).length">
        <a
          v-for="(option, index) in optionsFiltered(search)"
          :key="option.id"
          href="#"
          :class="['option', 'list-group-item', 'list-group-item-action', active === option.id ? 'active' : '']"
          @click.prevent="clickUpdate(option.id)">
          {{ option.text }}
        </a>
      </template>
      <template v-else>
        <div class="list-group-item text-muted">Nothing matches your filter.</div>
      </template>
    </div>
  </div>

  <div
    :class="['selected', 'form-control', 'shadow-sm', 'overflow-hidden', small ? 'form-control-sm' : '']"
    tabindex="0"
    ref="selected"
    @click.prevent="toggleEdit()"
    @keydown.up.prevent="toggleEdit()"
    @keydown.down.prevent="toggleEdit()"
    @keydown.enter.prevent="toggleEdit()">
    {{ selectedObject.text }}
  </div>
</div>
</template>


<script>
import Vue from 'vue';


export default {
  data() {
    return {
      search: '',
      edit: false,
      active: null,
    }
  },
  props: {
    options: {
      type: Array,
      default: [
        {
          id: '',
          text: 'Empty',
        }
      ],
    },
    selected: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: 'Empty',
    },
    small: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
    selectedObject: function() {
      if (this.selected) {
        return this.options.find(option => {
          return option.id === this.selected;
        });
      } else {
        return {
          text: this.placeholder,
        }
      }
    },
    activeObject: function() {
      return this.options.find(option => {
        return option.id === this.active;
      });
    },
  },
  watch: {
    search: function() {
      if (this.optionsFiltered(this.search).length && this.optionsFiltered(this.search).indexOf(this.activeObject) === -1)
        this.active = this.optionsFiltered(this.search)[0].id;
    },
  },
  methods: {
    optionsFiltered: function(search) {
      return this.options.filter(option => {
        return option.text.toLowerCase().includes(search);
      });
    },
    clickUpdate: function(id) {
      this.toggleEdit();
      this.$emit('input', id);
    },
    activeUpdate: function() {
      this.toggleEdit();
      this.$emit('input', this.active);
    },
    toggleEdit: function() {
      if (this.edit == true) {
        this.edit = false;
        this.search = '';
        Vue.nextTick(() => {
          this.$refs.selected.focus();
        });
      } else {
        this.edit = true;
        Vue.nextTick(() => {
          this.$refs.search.focus();
        });
      }
    },
    selectedUp: function() {
      const up = this.optionsFiltered(this.search).indexOf(this.activeObject) - 1;
      if (up > -1) this.active = this.optionsFiltered(this.search)[up].id;
    },
    selectedDown: function() {
      const down = this.optionsFiltered(this.search).indexOf(this.activeObject) + 1;
      if (down < this.optionsFiltered(this.search).length)
        this.active = this.optionsFiltered(this.search)[down].id;
    },
  },
  mounted() {
    this.active = this.selected;
  },
};
</script>


<style lang="scss">
.focuser {
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}

.select {
  position: absolute;
  z-index: 2;
  min-width: 400px;

  .badge {
    align-items: center;
    display: flex;
  }
}

.options {
  max-height: 200px;
  overflow-y: scroll;
  background-color: #fff;
}

.list-group-item {
  padding: .25rem .5rem;
}
</style>
