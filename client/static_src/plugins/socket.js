import store from '../store';


export default {
  install: () => {
    let updateSocketProtocol = 'ws://';
    if (location.protocol == 'https:') updateSocketProtocol = 'wss://';
    let updateSocketUrl = updateSocketProtocol + window.location.host + '/socket/';

    let updateSocket = new WebSocket(updateSocketUrl);

    updateSocket.onopen = () => {
      console.info('Update socket opened.');
    }

    updateSocket.onclose = () => {
      console.info('Update socket closed.');
    };

    updateSocket.onerror = () => {
      console.info('Update socket errored.');
    };

    updateSocket.onmessage = e => {
      let updateData = JSON.parse(e.data);
      if (updateData.model == 'Task')
        store.dispatch('tasks/fetchTasks');
      if (updateData.model == 'Client')
        store.dispatch('clients/fetchClients');
      if (updateData.model == 'Client')
        store.dispatch('projects/fetchProjects');
      if (updateData.model == 'Project')
        store.dispatch('projects/fetchProjects');
    };
  },
};
