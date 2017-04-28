<clients>
    <p class="mb-4 clearfix">
        <pager update={ getClients }/>
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
        getClients(url) {
            url = (typeof url !== 'undefined') ? url : clientsApiUrl
            quickFetch(url).then(function(data) {
                this.update({
                    clients: data.results,
                    next: data.next,
                    previous: data.previous
                })
            }.bind(this))
        }


        submitClient(e) {
            e.preventDefault()
            let body = {
                name: this.refs.name.value
            }
            quickFetch(clientsApiUrl, 'post', body).then(function(data) {
                this.refs.name.value = ''
                this.clients.unshift(data)
                this.update()
            }.bind(this));
        }

        this.on('mount', function() {
            this.getClients()
        }.bind(this))
    </script>
</clients>
