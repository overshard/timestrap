<clients>
    <p class="mb-4 clearfix">
        <button class="btn btn-primary btn-sm"
                data-url="{ previous }"
                if={ previous }
                onclick={ clientsPage }>
            <i class="fa fa-arrow-left" aria-hidden="true"></i> Previous
        </button>

        <button class="btn btn-primary btn-sm pull-right"
                data-url="{ next }"
                if={ next }
                onclick={ clientsPage }>
            Next <i class="fa fa-arrow-right" aria-hidden="true"></i>
        </button>
    </p>

    <form onsubmit={ submitClient }>
        <div class="row mb-2 py-2 bg-success">
            <div class="col-10">
                <input type="text" class="form-control" ref="name" placeholder="Name">
            </div>
            <div class="col-2 text-right">
                <button type="submit" class="btn btn-primary">
                    <i class="fa fa-plus" aria-hidden="true"></i> Add
                </button>
            </div>
        </div>
    </form>

    <div class="row mb-2 py-2 bg-faded" each={ clients } data-is="client"></div>

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


        clientsPage(e) {
            self.getClients(e.currentTarget.getAttribute('data-url'));
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
