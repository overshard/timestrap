<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header bg-secondary text-white">
            <slot name="header"/>
          </div>

          <div class="modal-body">
            <slot name="body"/>
          </div>

          <div class="modal-footer bg-light">
            <slot name="footer"/>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>


<script>
export default {
  data() {
    return {};
  },
};
</script>


<style lang="scss">
.modal-mask {
  position: fixed;
  z-index: 999;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 300px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header {
  border-top-left-radius: 2px;
  border-top-right-radius: 2px;

  h5 {
      margin-bottom: 0;
      font-weight: bold;
  }
}

.modal-body {
  margin: 0;
}

.modal-default-button {
  float: right;
}

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
