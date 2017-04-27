<clients>
    <pager update="{ getClients }"/>

    <form onsubmit={ submitClient }>
        <table class="clients-table table table-striped table-sm w-100 d-none">
            <thead class="thead-inverse">
                <tr>
                    <th>Name</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr class="table-info">
                    <td>
                        <input type="text" class="form-control form-control-sm" ref="name" placeholder="Name">
                    </td>
                    <td class="text-right">
                        <button type="submit" class="btn btn-primary btn-sm">Add</button>
                    </td>
                </tr>
                <tr each={ clients } data-is="client">
                </tr>
            </tbody>
        </table>
    </form>

    <p class="loading text-center my-5">
        <i class="fa fa-spinner" aria-hidden="true"></i>
    </p>

    <script>
        var self = this;


        getClients(url) {
            url = (typeof url !== 'undefined') ? url : clientsApiUrl;
            $('.loading, .clients-table').toggleClass('d-none');
            quickFetch(url).then(function(data) {
                self.update({
                    clients: data.results,
                    next: data.next,
                    previous: data.previous
                });
                $('.loading, .clients-table').toggleClass('d-none');
            });
        }


        submitClient(e) {
            e.preventDefault();
            let body = {
                name: self.refs.name.value
            }
            quickFetch(clientsApiUrl, 'post', body).then(function(data) {
                self.refs.name.value = '';
                self.clients.unshift(data);
                self.update();
            });
        }

        self.getClients();
    </script>
</clients>
