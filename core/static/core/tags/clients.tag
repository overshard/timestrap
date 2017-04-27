<clients>
    <p class="mb-4 clearfix">
        <pager update="{ getClients }" />
    </p>

    <form onsubmit={ submitClient }>
        <div class="row mb-2 py-2 bg-primary">
            <div class="col-10">
                <input type="text" class="form-control form-control-sm" ref="name" placeholder="Name">
            </div>
            <div class="col-2 text-right">
                <button type="submit" class="btn btn-success btn-sm">
                    <i class="fa fa-plus" aria-hidden="true"></i> Add
                </button>
            </div>
        </div>
    </form>

    <client each={ clients } />

    <script>
        var self = this;


        getClients(url) {
            url = (typeof url !== 'undefined') ? url : clientsApiUrl;
            quickFetch(url).then(function(data) {
                self.update({
                    clients: data.results,
                    next: data.next,
                    previous: data.previous
                });
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
