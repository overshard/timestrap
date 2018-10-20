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
      if (updateData.model == 'Task')
        store.dispatch('tasks/getTasks');
      if (updateData.model == 'Client')
        store.dispatch('clients/getClients');
      if (updateData.model == 'Project')
        store.dispatch('clients/getProjects');
    };
  },
};
