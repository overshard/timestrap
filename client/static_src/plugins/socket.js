import store from '../store';


export default {
  install: () => {
    let updateSocketProtocol = 'ws://';
    if (location.protocol == 'https:') updateSocketProtocol = 'wss://';
    let updateSocketUrl = updateSocketProtocol + window.location.host + '/socket/';

    let updateSocket = new WebSocket(updateSocketUrl);

    updateSocket.onclose = () => {
      console.error('Update socket closed unexpectedly.');
    };

    updateSocket.onerror = () => {
      console.error('Update socket errored unexpectedly.');
    };

    updateSocket.onmessage = e => {
      let updateData = JSON.parse(e.data);
      if (updateData.tasks != store.getters['tasks/getNumberOfTasks'])
        store.dispatch('tasks/getTasks');
      if (updateData.clients != store.getters['clients/getNumberOfClients'])
        store.dispatch('clients/getClients');
      if (updateData.projects != store.getters['clients/getNumberOfProjects'])
        store.dispatch('clients/getProjects');
    };

    function checkForUpdates() {
      setTimeout(() => {
        updateSocket.send('');
        checkForUpdates();
      }, 5000);
    }

    checkForUpdates();
  },
};
