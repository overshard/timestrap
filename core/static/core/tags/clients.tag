<clients>
    <p class="mb-4 clearfix">
        <pager update="{ getClients }" />
    </p>

    <form onsubmit={ submitClient }>
        <div class="row bg-primary form-row mb-2">
            <div class="col-9">
                <input type="text" class="form-control form-control-lg bg-primary" ref="name" placeholder="New Client Name">
            </div>
            <div class="col-3">
                <button type="submit" class="btn btn-primary btn-lg">
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
